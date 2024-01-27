import os
import time
from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import unquote

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')


browser = webdriver.Chrome(options=chrome_options)

with open('jio.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    try:
        components = line.strip().split('\t')
        filename = components[0] 
        # Remove '%' symbol and replace it with a blank space
        keyword = ' '.join(components[1:]).replace('%', ' ')
        keyword = unquote(keyword)  # Decode URL-encoded characters if any
        
        print(filename)
        output_folder = 'images'
        os.makedirs(output_folder, exist_ok=True)
        
        url = f"https://www.google.com/search?q={keyword}&tbm=isch"
        
        # if "docmitra.com" in url:
        #     continue  # Skip processing this URL
        
        browser.get(url)
        
        image_elements = browser.find_elements(By.XPATH, '//div[@id="islrg"]//img')
        count_images = 0
        for i, image_element in enumerate(image_elements):
            try:
                if count_images >= 4:
                    break  # Break the loop once 5 images are saved
                
                image_element.click()  

                full_size_image = WebDriverWait(browser, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//div[@class="p7sI2 PUxBg"]//img[@class="sFlh5c pT0Scc iPVvYb"]'))
                )

                image_url = full_size_image.get_attribute('src')
                if not image_url:
                    browser.back()
                    continue

                browser.get(image_url)
                time.sleep(2)  

                screenshot = browser.get_screenshot_as_png()
                img = Image.open(BytesIO(screenshot))
                
                img.save(os.path.join(output_folder, f"{filename}_{i+1}.png"))
                count_images += 1  # Increment the image count after saving an image

                # Close newly opened tabs
                if len(browser.window_handles) > 1:
                    for handle in browser.window_handles[1:]:
                        browser.switch_to.window(handle)
                        browser.close()
                    browser.switch_to.window(browser.window_handles[0])

                browser.back()

            except Exception as e:
                print(f"Error capturing image {i + 1} for '{filename}': {e}")

    except Exception as e:
        print(f"Error processing '{filename}': {e}")

browser.quit()





#-------------------








# import os
# import time
# from selenium import webdriver
# from PIL import Image
# from io import BytesIO
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options

# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# chrome_options = Options()
# chrome_options.add_argument(f'user-agent={user_agent}')

# browser = webdriver.Chrome(options=chrome_options)

# url = "https://www.google.com/search?q=pharmacy+&tbm=isch&ved=2ahUKEwjXu_3t1YCDAxW-6DgGHa4yCbkQ2-cCegQIABAA&oq=pharmacy+&gs_lcp=CgNpbWcQAzIECCMQJzIICAAQgAQQsQMyCggAEIAEEIoFEEMyCggAEIAEEIoFEEMyBQgAEIAEMggIABCABBCxAzIFCAAQgAQyCggAEIAEEIoFEEMyBQgAEIAEMgUIABCABFCEG1jTIGCqRWgAcAB4AIABlwKIAeEKkgEFMC41LjKYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=Z3tzZZfsG77R4-EPruWkyAs&bih=767&biw=1536"
# browser.get(url)

# SCROLL_PAUSE_TIME = 2

# last_height = browser.execute_script("return document.body.scrollHeight")

# while True:
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
#     time.sleep(SCROLL_PAUSE_TIME)
    
#     new_height = browser.execute_script("return document.body.scrollHeight")
    
#     if new_height == last_height:
#         break
#     last_height = new_height

# image_elements = browser.find_elements(By.XPATH, '//div[@id="islrg"]//img')

# output_folder = 'images'
# os.makedirs(output_folder, exist_ok=True)

# for i, image_element in enumerate(image_elements):
#     try:
#         image_url = image_element.get_attribute('src')
        
#         if not image_url:
#             continue
        
#         browser.get(image_url)
#         screenshot = browser.get_screenshot_as_png()
#         img = Image.open(BytesIO(screenshot))

#         width, height = img.size
#         zoom_factor = 0.4 # Adjust zoom factor as needed
#         new_width = int(width * zoom_factor)
#         new_height = int(height * zoom_factor)
#         left = (width - new_width) / 2
#         top = (height - new_height) / 2
#         right = (width + new_width) / 2
#         bottom = (height + new_height) / 2
#         cropped_img = img.crop((left, top, right, bottom))
       
#         cropped_img.save(os.path.join(output_folder, f"image_{i+1}_cropped.png"))
#         # cropped_img.save(os.path.join(output_folder, f"image_{i+1}_cropped.jpg"), format='JPEG')

#         browser.back()
        
#     except Exception as e:
#         print(f"Error capturing image {i+1}: {e}")


# browser.quit()
