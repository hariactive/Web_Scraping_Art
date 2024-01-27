import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class GoogleMapScraper:
    city = 'test1'

    def __init__(self):
        self.panel_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]'
        self.output_file_name = f"{self.city.lower()}.csv"  
        self.driver = None
        self.unique_check = set()
        self.current_area = None

    def config_driver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        driver_path = r"C:\Program Files\Driver\chromedriver"
        driver = webdriver.Chrome(executable_path=driver_path, options=options)
        self.driver = driver

    def save_data(self, data):
        with open(self.output_file_name, 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            if tuple(data) not in self.unique_check:
                writer.writerow(data)
                self.unique_check.add(tuple(data))
        

    def get_business_info(self):
        for business in self.driver.find_elements(By.CLASS_NAME, 'THOPZb'):
            try:
                name = business.find_element(By.CLASS_NAME, 'qBF1Pd').text
            except:
                name = ''
            try:
                address_block = business.find_elements(By.CLASS_NAME, "W4Efsd")[2].text.split("·")
                if len(address_block) >= 2:
                    address = address_block[1].strip()
                elif len(address_block) == 1:
                    address = address_block[0]
            except:
                address = ""
            try:
                contact = business.find_element(By.CLASS_NAME, 'UsdlK').text
                if "+1" not in contact:
                    phone = contact
                else:
                    phone = ''
            except:
                phone = ''

            data = [name, phone, address, self.current_area, self.city]
            print(data)
            self.save_data(data)

    def load_companies(self, url,area):
        print(area)
        self.driver.get(url)
        divSideBar = self.driver.find_element(By.CSS_SELECTOR, f"div[aria-label='{area}']")
        print("oh",divSideBar)
        keepScrolling = True
        while keepScrolling:
            divSideBar.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.0001)
            divSideBar.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.0001)

            html = self.driver.find_element(By.TAG_NAME, "html").get_attribute('outerHTML')

            if "You've reached the end of the list." in html:
                keepScrolling = False
      
            self.get_business_info()

    def search_in_area(self, area):
        self.current_area = area
        url = f"https://www.google.com/maps/search/pharmacies+in+{area}"
        if area.lower() in self.current_area.lower():
            custom_result = f"Results for pharmacies in {area}"
        else:
            custom_result = ""
        self.load_companies(url,custom_result)

    def perform_search(self, areas):
        self.config_driver()
        for area in areas:
            self.search_in_area(area)
        self.driver.quit()  

with open('areas.txt', 'r') as file:
    areas = file.read().splitlines()

scraper = GoogleMapScraper()
scraper.perform_search(areas)





# def config_driver(self):
    #     options = webdriver.ChromeOptions()
    #     driver_path = 'C:\Program Files\Driver\chromedriver'
    #     driver = webdriver.Chrome(executable_path=driver_path, options=options)
    #     # Set device metrics using CDP
    #     device_metrics = {
    #         'width': 390,
    #         'height': 844,
    #         'deviceScaleFactor': 0,
    #         'mobile': True
    #     }
    #     driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', device_metrics)
    #     self.driver = driver
    

    # def is_stale(self, element):
    #     try:
    #         # Check if the element is stale (not present in DOM)
    #         element.is_enabled()
    #     except StaleElementReferenceException:
    #         return False
    #     return True
