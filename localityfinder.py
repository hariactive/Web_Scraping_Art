import requests
from bs4 import BeautifulSoup

url = 'https://www.magicbricks.com/mbutility/localitySearchPage'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    # Add any other necessary headers here
}

city_name = 'hubli'   # Only change the city name

with open(f'loc_titles_{city_name}.txt', 'w', encoding='utf-8') as file:
    for page_number in range(1, 30):  # Loop through pages from 1 to 20
        payload = {
            'autoLoad': 'Y',
            'page': str(page_number),
            'sortBy': 'demand',
            'cityName': city_name
        }

        response = requests.get(url, params=payload, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')  # Parse HTML content using BeautifulSoup
            loc_titles = soup.find_all('a', class_='loc-card__title')  # Find all <a> tags with class 'loc-card__title'

            for title in loc_titles:
                # Remove content after the comma in each title
                modified_title = title.text.strip().split(',')[0]
                print(modified_title)
                file.write(modified_title + '\n')  # Write the modified title to the file
        else:
            print(f"Request failed for page {page_number} with status code {response.status_code}")
