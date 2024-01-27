import csv
import time
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import keyboard

class WebScraper(ABC):
    def __init__(self, city):
        self.city = city
        self.output_file_name = f"{self.city.lower()}.csv"
        self.driver = None
        self.unique_check = set()
        self.current_area = None

    @abstractmethod
    def config_driver(self):
        pass

    @abstractmethod
    def save_data(self, data):
        pass

    @abstractmethod
    def get_business_info(self, business):
        pass

    @abstractmethod
    def load_companies(self, url, area):
        pass

    @abstractmethod
    def search_in_area(self, area):
        pass

    @abstractmethod
    def perform_search(self, areas):
        pass

class GoogleMapScraper(WebScraper):
    def config_driver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        driver_path = r"C:\Program Files\Driver\chromedriver"
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

    def save_data(self, data):
        with open(self.output_file_name, 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            if tuple(data) not in self.unique_check:
                writer.writerow(data)
                self.unique_check.add(tuple(data))

    def get_business_info(self, business):
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
            phone = contact if "+1" not in contact else ''
        except:
            phone = ''

        return [name, phone, address, self.current_area, self.city]

    def load_companies(self, url, area):
        print(area)
        self.driver.get(url)
        div_side_bar = self.driver.find_element(By.CSS_SELECTOR, f"div[aria-label='{area}']")
        print("oh", div_side_bar)
        keep_scrolling = True
        while keep_scrolling:
            div_side_bar.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.0001)
            div_side_bar.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.0001)

            html = self.driver.find_element(By.TAG_NAME, "html").get_attribute('outerHTML')

            if "You've reached the end of the list." in html:
                keep_scrolling = False

            for business in self.driver.find_elements(By.CLASS_NAME, 'THOPZb'):
                data = self.get_business_info(business)
                print(data)
                self.save_data(data)

    def search_in_area(self, area):
        self.current_area = area
        url = f"https://www.google.com/maps/search/pharmacies+in+{area}"
        if area.lower() in self.current_area.lower():
            custom_result = f"Results for pharmacies in {area}"
        else:
            custom_result = ""
        self.load_companies(url, custom_result)

    def perform_search(self, areas):
        try:
            self.config_driver()

            keyboard.add_hotkey('e', lambda: keyboard.press_and_release('ctrl+c'))

            for area in areas:
                self.search_in_area(area)
        except KeyboardInterrupt:
            print("Program interrupted by user.")
        finally:
            try:
                if self.driver:
                    self.driver.quit()
                keyboard.unhook_all()  # Unhook all keyboard listeners
            except Exception as e:
                print(f"Error while closing the browser: {e}")


if __name__ == "__main__":
    with open('areas.txt', 'r') as file:
        areas = file.read().splitlines()

    scraper = GoogleMapScraper(city='test1')
    scraper.perform_search(areas)
