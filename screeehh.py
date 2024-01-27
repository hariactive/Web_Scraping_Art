import os
import time
from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



output_folder = 'images'
os.makedirs(output_folder, exist_ok=True)
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')

browser = webdriver.Chrome(options=chrome_options)

url = "https://www.google.com/search?q=pharmacy+&tbm=isch&ved=2ahUKEwjXu_3t1YCDAxW-6DgGHa4yCbkQ2-cCegQIABAA&oq=pharmacy+&gs_lcp=CgNpbWcQAzIECCMQJzIICAAQgAQQsQMyCggAEIAEEIoFEEMyCggAEIAEEIoFEEMyBQgAEIAEMggIABCABBCxAzIFCAAQgAQyCggAEIAEEIoFEEMyBQgAEIAEMgUIABCABFCEG1jTIGCqRWgAcAB4AIABlwKIAeEKkgEFMC41LjKYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=Z3tzZZfsG77R4-EPruWkyAs&bih=767&biw=1536"
browser.get(url)

SCROLL_PAUSE_TIME = 2

last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    time.sleep(SCROLL_PAUSE_TIME)
    
    new_height = browser.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        break
    last_height = new_height


image_elements = browser.find_elements(By.XPATH, '//div[@id="islrg"]//img')
for i, image_element in enumerate(image_elements):
    try:
        image_element.click()  # Clicking on the image to view in full-size

        # Wait for the full-size image container to load
        full_size_image = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="p7sI2 PUxBg"]//img[@class="sFlh5c pT0Scc iPVvYb"]'))
        )

        image_url = full_size_image.get_attribute('src')
        if not image_url:
            browser.back()
            continue

        browser.get(image_url)
        time.sleep(2)  # Adjust this wait time as needed for the image to load

        screenshot = browser.get_screenshot_as_png()
        img = Image.open(BytesIO(screenshot))

        # Save the screenshot as it is without applying any zoom or cropping
        img.save(os.path.join(output_folder, f"image_{i + 1}_screenshot.png"))

        browser.back()

    except Exception as e:
        print(f"Error capturing image {i + 1}: {e}")

browser.quit()
