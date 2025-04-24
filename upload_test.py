import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class InputFieldTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--headless")  # run without opening a browser window
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get("http://the-internet.herokuapp.com/inputs")
        cls.input_field = cls.driver.find_element(By.TAG_NAME, "input")

    def test_numeric_input(self):
        """Test that numeric input is accepted."""
        self.input_field.clear()
        self.input_field.send_keys("12345")
        value = self.input_field.get_attribute("value")
        self.assertEqual(value, "12345", f"Expected '12345' but got '{value}'")

    def test_non_numeric_input(self):
        """Test that non-numeric input is not accepted."""
        self.input_field.clear()
        self.input_field.send_keys("abcd")
        value = self.input_field.get_attribute("value")
        self.assertEqual(value, "", f"Expected empty string but got '{value}'")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
