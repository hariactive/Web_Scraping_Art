import requests
from bs4 import BeautifulSoup
import csv

base_url = 'https://www.hubballionline.in/city-guide/medical-stores-in-hubli'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

response = requests.get(base_url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Finding all <div> elements containing medical store information
    divs = soup.find_all('div')
    
    data = []  # To store extracted data
    
    for div in divs:
        # Extracting text from the div tag
        div_text = div.get_text(separator='|')
        
        # Split the text using separator to get individual parts
        parts = div_text.split('|')
        
        # Ensure the parts list has enough elements
        if len(parts) >= 2:
            # Extracting name and address
            name = parts[0].strip()  # Name of the medical store
            address = parts[1].split(',')[0].strip() if ',' in parts[1] else parts[1].strip()  # Address excluding pincode
            
            data.append([name, address])  # Append data to list for CSV
            
    # Writing data to a CSV file
    with open('medical_stores.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Name', 'Address'])  # Write header
        csv_writer.writerows(data)  # Write data rows
        
    print("Data exported to medical_stores.csv")
        
else:
    print('Failed to fetch the content. Status code:', response.status_code)
