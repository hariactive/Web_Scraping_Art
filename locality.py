from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        a = 'telangana'
        b = 'Nalgonda'
        places = [

    "Mothkur",
    "Munugode",
    "Nakrekal",
    "Nalgnda",
    "Nalgoda",
    "Nalgodna",
    "Nalgolnda",
    "Nalgonda",
    "Nalognda",
    "Narayanapur",
    "Pedda Adiserla Palle",
    "Peddavoora",
    "Pochampalle",
    "Ramannapeta So",
    "Suryapet",
    "Suryapet Ho",
    "Suryap-et",
    "Thungathurthi",
    "Thungathurthy",
    "Tirumalgiri",
    "Valigonda",
    "Vv",
    "Yadagarigutta",
    "Yadagirigutta"
]
        
        
        places = [tehsil.replace(' ', '-').replace('.', '-').replace('(', '-').replace(')', '-') for tehsil in places]

        
        b = b.strip().lower()

        for place in places:
            c = place.strip().lower()  # Convert each place in the list to lowercase

            url = f'https://www.delhimetrotimes.in/{a}/{b}/{c}/list-of-area-in-{c}.html'

            browser = p.firefox.launch()
            context = browser.new_context()
            custom_headers = {
                'Custom-Header-Name': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            }
            context.set_extra_http_headers(custom_headers)
            page = context.new_page()
            page.goto(url)

            # Wait for the table to load
            page.wait_for_selector('.table')

            # Wait for the table and select element to load
            page.wait_for_selector('#route_form table:nth-child(1) tbody:nth-child(1) tr:nth-child(3) td:nth-child(1) select:nth-child(2)')

            # Retrieve elements using JavaScript and execute XPath queries
            areas = page.evaluate('''Array.from(document.querySelectorAll('table.table tbody tr td:nth-child(2) strong')).map(elem => elem.textContent.trim())''')
            tehsils = page.evaluate('''Array.from(document.querySelectorAll('table.table tbody tr td:nth-child(3)')).map(elem => elem.textContent.trim())''')

            # Appending extracted data to areas.txt
            with open('areas.txt', 'a', encoding='utf-8') as file:
                for i in range(len(areas)):
                    data_line = f"{areas[i]}, {tehsils[i]}\n"
                    print(data_line.strip())
                    file.write(data_line)
                    
            browser.close()
            
if __name__ == '__main__':
    main()