import os
import re
import shutil
import subprocess
import time
from bs4 import BeautifulSoup
import html2text
#from settings import SettingsHandler
import requests
import argparse
import pyperclip
class RequiresTelegram(Exception):
    "This post must be viewed via Telegram."
    pass
class TelegramScraper:
    def __init__(self):
        #self.settings = SettingsHandler().load_settings()
        self.workingURL = None
        self.date = ""
        self.auth = ""
        self.content = ""
        self.imgCt = 0
        self.videoCt = 0
    def html_to_text(self, html: str):
        h = html2text.HTML2Text()
        h.body_width = 0  # Disable line wrapping
        h.ignore_links = True  # Ignore hyperlinks
        h.ignore_emphasis = True  # Ignore bold and italic formatting
        h.ignore_images = True  # Ignore images
        h.protect_links = True  # Protect hyperlinks from being stripped out
        h.unicode_snob = True  # Use Unicode characters instead of ASCII
        h.wrap_links = False  # Disable link wrapping
        h.wrap_lists = False  # Disable list wrapping
        h.decode_errors = 'ignore'  # Ignore Unicode decoding errors

        text = h.handle(html)
        text = re.sub(r'\*+', '', text)  # Remove asterisks
        text = re.sub(r'^[ \t]*[\\`]', '', text, flags=re.MULTILINE)  # Remove leading \ or `
        return text 
    def get_author(self, input: str):
        """
        Takes a stringified HTML input and parses out the author of the content.
        """
        try:
            author = self.html_to_text(str(input.find('div', {'class': 'tgme_widget_message_author accent_color'}).find('a', {'class': 'tgme_widget_message_owner_name'}).find('span', {'dir': 'auto'})))
            return author
        except:
            return None
    def get_content(self, input: str):
        """
        Takes a stringified HTML input and parses out the content of the post.
        """
        try:
            content = self.html_to_text(str(input.find('div', {'class': 'tgme_widget_message_text js-message_text', 'dir': 'auto'})))
            return content
        except:
            return None
    def get_post_date(self, input: str):
        """
        Takes a stringified HTML input and parses out the date/time of the post.
        """
        try:
            date = self.html_to_text(str(input.find('span', {'class': 'tgme_widget_message_meta'}).find('time', {'class': 'datetime'})))
            return date
        except:
            return None
    def get_images(self, input: str):
        """
        Utilizes regex to find the image urls.
        """
        try:
            images = input.findAll('a', {'class': 'tgme_widget_message_photo_wrap'})
            image_urls = []
            for div in images:
                style = div['style']
                match = re.search(r"background-image:url\('(.*)'\)", style)
                if match:
                    bg_image_url = match.group(1)
                    image_urls.append(bg_image_url)
            return image_urls
        except:
            return None
    def get_videos(self, input: str):
        """
        Utilizes HTML parsing to find the video urls.
        """
        try:
            video_urls = []
            video_tags = input.find_all('video')
            for video in video_tags:
                src = video.get('src')
                if src:
                    video_urls.append(src)
            return video_urls
        except:
            return None
    def get_post_data(self, url: str):
        """
        Simple HTTP request to obtain the posts' HTML text.
        """
        with requests.Session() as cl:
            getreq = cl.get(url, headers={
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36 TelegramBot (like TwitterBot)'
            })
            cl.close()
            linkHTML = BeautifulSoup(getreq.text, 'html.parser'
            )
            if('Please open Telegram to view this post' in getreq.text 
               or 'tgme_widget_message_error' in getreq.text):
                raise RequiresTelegram
            else:
                return linkHTML
    def parse_args(self):
        """
        Arguement parsing for links. Added for my CLI enjoyers.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('--link', '-link', help='Link(s) to scrape. Seperate links via commas. Example: Link1,Link2,Link3')
        args = parser.parse_args()
        if (args.link):
            return args.link
        else:
            return None
    def get_links(self):
        """
        Link sanitizing and parsing.
        """
        pullLink = self.parse_args()
        if pullLink:
            link_arg = pullLink.replace('?single', '')
            return [link + '?embed=1&mode=tme' for link in link_arg.split(',')]
        if pullLink is None:
            links = input(' > [TG Scraper]\n > Please enter the Telegram post URL(s):\n > Split multiple links with a comma\n >>> ').replace('?single', '')
            links = [link + '?embed=1&mode=tme' for link in links.split(',')]
            return links
    def copy_content(self, textToCopy):
        try:
            return pyperclip.copy(textToCopy)
        except Exception as e:
            print(f"An error occurred: {e}")
            return False  # Return False if an error occurred
    def media_download_handler(self, postData: str):
        match(input('[TG Scraper] Do you want to download the media from the post? [Y/N]\n > ').lower()):
            case 'y':
                match(input(f'[TG Scraper]\n1. Download Videos ({self.videoCt})\n2. Download Images ({self.imgCt})\n3. Download All ({self.imgCt + self.videoCt})\n > ').lower()):
                    case '1':
                        urls = self.get_videos(postData)
                    case '2':
                        urls = self.get_images(postData)
                    case '3':
                        urls = self.get_images(postData) + self.get_videos(postData)
                        urls = list(set(urls))
                self.downloadMedia(urls)
                self.textHandler(postData)
            case 'n':
                print('[TG Scraper] Skipping media handler! Proceeding to the text handler.')
                self.textHandler(postData)
            case _:
                print('[TG Scraper] Invalid selection!')
                time.sleep(1)
                os.system('cls')
                self.media_download_handler(postData)
    def parseInfoViaUrl(self, urlInput):
        url_data = urlInput.split('/')
        main_name = url_data[-2]
        post_id = url_data[-1]
        return main_name, post_id

    def downloadMedia(self, urlList):
        for _ in urlList:
            url = self.workingURL.replace('?embed=1&mode=tme', '')
            url_data = url.split('/')
            main_folder = url_data[-2]
            post_id = url_data[-1]
            
            if not os.path.exists(main_folder):
                os.makedirs(main_folder)

            for file_num, url in enumerate(urlList, start=1):
                path_and_query = url.split("?")[0]
                path_parts = path_and_query.split("/")
                value_after_file = path_parts[path_parts.index("file") + 1].split('.')
                content_id = value_after_file[0]
                extension = value_after_file[1]
                if len(value_after_file[0]) > 5:
                    content_id = value_after_file[0].split('_')[0]
                file_path = os.path.join(main_folder, f"{main_folder}-{post_id}", f"{content_id}-{file_num}.{extension}")
                if(os.path.exists(file_path)):
                    return

                response = requests.get(url)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'wb') as f:
                    f.write(response.content)

                print(f"File {file_num} downloaded to {os.path.abspath(file_path)}")
    
    def print_centered_text(self, text):
        terminal_width = shutil.get_terminal_size().columns
        lines = text.splitlines()
        for line in lines:
            padding = (terminal_width - len(line)) // 2
            print(" " * padding + line)

    def textHandler(self, postinput):
        date = self.get_post_date(postinput)
        author = self.get_author(postinput)
        content = self.get_content(postinput)
        self.print_centered_text(f"""
        {date}
        {author}
        {content}
                            """)
        match(input('[TG Scraper] Would you like to:\n1. Copy Text\n2. Save Text\n > ')):
            case '1':
                self.copy_content(f'{date}\n{author}\n{content}')
            case '2':
                fn = input('Filename: ')
                with open(fn, 'w', encoding='utf-8') as f:
                    f.write(f'{date}\n{author}\n{content}')
                    print(f'[TG Scraper] Wrote post contents to "{fn}"')
    def run(self):
        urlList = self.get_links()
        for link in urlList:
            try:
                self.workingURL = link
                post_data = self.get_post_data(link)
                self.date = self.get_post_date(post_data)
                self.auth = self.get_author(post_data)
                self.content = self.get_content(post_data)
                self.videoCt = len(self.get_videos(post_data))
                self.imgCt = len(self.get_images(post_data))
                if self.get_videos(post_data) is not None or self.get_images(post_data) is not None:
                    self.media_download_handler(post_data)
                else:
                    print('[TG Scraper] No multi-media was found in the post.\n[TG Scraper] Continuing to the text handler.')
                    self.textHandler(post_data)
                del self.date, self.auth, self.content, self.videoCt, self.imgCt
            except RequiresTelegram:
                print('[TG Scraper] This post must be viewed via Telegram.')
            
if __name__ == '__main__':    
    TelegramScraper().run()