import requests
from bs4 import BeautifulSoup
import csv

MAX_PAGES = 3             #how many pages to scrap

def make_request(url, payload=None):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.text

def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    names = soup.select('div.listing ')

    for name in names:
        name_value = name.select_one('h3 a')
        address_value = name.select_one('p')

        # Check if the elements exist before calling get_text
        name_text = name_value.get_text(strip=True) if name_value else None
        address_text = address_value.get_text(strip=True) if address_value else None

        yield {
            'Name': name_text,
            'Address': address_text
        }

def save_to_csv(data, filename='scraped_data.csv'):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Address']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write headers only if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerows(data)

def scrape_first_url():
    url = 'https://www.healthfrog.in/chemists/medical-store/kerala/kottayam'
    html = make_request(url)
    results = list(parse_results(html))
    save_to_csv(results)

def main():
    # Scrape data from the first URL
    scrape_first_url()

    # Scrape data from the second URL
    page = 1
    while page <= MAX_PAGES:
        url = 'https://www.healthfrog.in/importlisting.html'
        payload = {
            'page': str(page),
            'mcatid': 'chemists',
            'keyword': 'medical-store',
            'state': 'kerala',          #change state name by inspecting
            'city': 'kottayam'                #change city as well 
        }

        html = make_request(url, payload)
        results = list(parse_results(html))

        for result in results:
            print(result)

        save_to_csv(results)
        page += 1

if __name__ == "__main__":
    main()
