import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=service, options=options)


def test_purchase_flow():
    driver = setup_driver()

    def wait_for_element(driver, by, selector):
        print(f"Waiting for element: {selector}")
        print(f"Current URL: {driver.current_url}")
        print("Page Source:")
        print(driver.page_source[:500])
        return WebDriverWait(driver, 30).until(EC.presence_of_element_located((by, selector)))

    try:
        driver.get("https://www.saucedemo.com/")
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        username_input.send_keys("standard_user")

        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("secret_sauce")

        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

        backpack_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='add-to-cart-sauce-labs-backpack']"))
        )
        backpack_button.click()

        cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        )
        cart_button.click()

        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_button.click()

        first_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )
        first_name_input.send_keys("John")

        last_name_input = driver.find_element(By.ID, "last-name")
        last_name_input.send_keys("Doe")

        postal_code_input = driver.find_element(By.ID, "postal-code")
        postal_code_input.send_keys("12345")

        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "continue"))
        )
        continue_button.click()

        finish_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "finish"))
        )
        finish_button.click()

        thank_you_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Thank you for your order!')]"))
        )
        assert thank_you_text.is_displayed(), "Purchase not completed successfully"

    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    try:
        test_purchase_flow()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise
