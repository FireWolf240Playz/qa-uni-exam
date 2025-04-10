import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait for the element to be present
wait = WebDriverWait(driver, 10)
upload_input = wait.until(EC.presence_of_element_located((By.ID, "input")))


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


IMAGE_PATH = os.path.abspath("test_image.jpg")  # Make sure the image exists

chrome_options = Options()

chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1280,800")


driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=chrome_options
)
logging.info("Browser started successfully")

try:
    test_url = "https://mdn.mozillademos.org/files/3698/image_upload_preview.html"
    driver.get(test_url)
    logging.info(f"Opened URL: {test_url}")

    upload_input = driver.find_element(By.ID, "input")
    assert upload_input is not None, "Upload input field not found"

    upload_input.send_keys(IMAGE_PATH)
    logging.info(f"Image uploaded: {IMAGE_PATH}")

    time.sleep(2)
    image_preview = driver.find_element(By.ID, "output")
    assert image_preview.get_attribute("src") != "", "Image did not load in preview"
    logging.info("Image preview loaded successfully")

    print("✅ Test Passed: Image upload and preview successful.")

except AssertionError as ae:
    logging.error(f"[FAIL] Assertion failed: {ae}")
    print(f"[FAIL] Test Failed: {ae}")

except NoSuchElementException as ne:
    logging.error(f"[FAIL] Element not found: {ne}")
    print(f"[FAIL] Test Failed: {ne}")

finally:
    driver.quit()
    logging.info("Browser closed.")
