import os
import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


class GruyereUploadTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,800")

        cls.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        cls.wait = WebDriverWait(cls.driver, 10)

        cls.GRUYERE_URL = "https://google-gruyere.appspot.com/594464600711147540234356220068201878075/"
        cls.IMAGE_PATH = os.path.abspath(
            r"C:\Users\александър\OneDrive\Работен плот\budgetApp (1).jpg"
        )
        cls.FAKE_FILE = os.path.abspath("not_an_image.txt")

    def test_image_upload_success(self):
        logging.info("Testing valid image upload to Gruyere")

        upload_url = self.GRUYERE_URL.rstrip("/") + "/upload.gtl"
        self.driver.get(upload_url)
        logging.info(f"Navigated to: {upload_url}")

        upload_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "file"))
        )
        upload_input.send_keys(self.IMAGE_PATH)

        self.driver.find_element(By.NAME, "upload").click()
        logging.info("Submitted image upload form")

        page_source = self.driver.page_source
        self.assertIn(
            "File uploaded",
            page_source or "budgetApp",
            "Upload confirmation not found in page",
        )

        self.driver.save_screenshot("screenshots/gruyere_upload_success.png")
        logging.info("Saved screenshot for image upload")

    def test_non_image_upload(self):
        logging.info("Testing non-image file upload to Gruyere")

        upload_url = self.GRUYERE_URL.rstrip("/") + "/upload.gtl"
        self.driver.get(upload_url)
        logging.info(f"Navigated to: {upload_url}")

        upload_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "file"))
        )
        upload_input.send_keys(self.FAKE_FILE)

        self.driver.find_element(By.NAME, "upload").click()
        logging.info("Submitted non-image upload form")

        page_source = self.driver.page_source
        self.assertTrue(
            "error" in page_source.lower() or "upload" in page_source.lower(),
            "Expected failure or message on non-image upload",
        )

        self.driver.save_screenshot("screenshots/gruyere_non_image_upload.png")
        logging.info("Saved screenshot for invalid file upload")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        logging.info("Browser closed.")


if __name__ == "__main__":
    unittest.main()
