import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

GRUYERE_URL = (
    "https://google-gruyere.appspot.com/377691518057699612282348493247076654690/"
)
IMAGE_PATH = os.path.abspath("C:\Users\александър\OneDrive\Работен плот\budgetApp (1).jpg")

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280,800")

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=options
)
wait = WebDriverWait(driver, 10)

try:
    logging.info("Starting Gruyere automation")
    driver.get(GRUYERE_URL)
    logging.info(f"Opened Gruyere start page: {GRUYERE_URL}")

    start_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Agree & Start")))
    start_link.click()
    logging.info("Clicked 'Agree & Start'")

    upload_url = (
        driver.current_url + "/upload.gtl"
    ) 
    driver.get(upload_url)
    logging.info(f"Navigated to: {upload_url}")

    upload_input = wait.until(EC.presence_of_element_located((By.NAME, "file")))
    upload_input.send_keys(IMAGE_PATH)
    logging.info(f"Uploaded image: {IMAGE_PATH}")

    submit_button = driver.find_element(By.NAME, "upload")
    submit_button.click()
    logging.info("Submitted the upload form")

    time.sleep(2)
    print("Test Passed: File uploaded successfully.")

except (NoSuchElementException, TimeoutException) as e:
    logging.error(f"[FAIL] Element issue: {e}")
    print(f"[FAIL] Test Failed: {e}")

except Exception as ex:
    logging.error(f"[FAIL] Unexpected error: {ex}")
    print(f"[FAIL] Test Failed: {ex}")

finally:
    driver.quit()
    logging.info("Browser closed.")
