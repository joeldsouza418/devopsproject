from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Your VM public IP
URL = "http://<VM_PUBLIC_IP>:8080"

def test_exam_form():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(URL)
    time.sleep(2)

    # Fill form
    driver.find_element("name", "name").send_keys("Test User")
    driver.find_element("name", "email").send_keys("test@example.com")
    driver.find_element("name", "exam_date").send_keys("2025-12-25")

    driver.find_element("tag name", "button").click()

    time.sleep(2)

    # Validate success message
    assert "email sent instantly" in driver.page_source.lower()

    print("Selenium Test Passed ✔")
    driver.quit()


if __name__ == "__main__":
    test_exam_form()
