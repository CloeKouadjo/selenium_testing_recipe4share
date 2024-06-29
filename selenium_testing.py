import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import time
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tempmail import EMail
import re

def login(driver, email, password):

        # Navigate to home page
        driver.get("https://www.recipe4share.com/")

        # Wait up to 1 second for login button to become clickable
        login_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='item' and text()='Login']"))
        )

        # Click on login button
        login_button.click()

        # Wait up to 1 second for login modal to become visible
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.ui.modal.transition.visible.active"))
        )

        # Enter email
        email_field = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter email or username'][type='text']")
        email_field.send_keys(email)

        # Enter password
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_field.send_keys(password)

        # Click on login submit button
        login_submit = driver.find_element(By.CSS_SELECTOR, "button.ui.icon.positive.right.labeled.button")
        login_submit.click()

class Recipe4ShareTests(unittest.TestCase):

    def setUp(self):

        self.driver = webdriver.Chrome()

        # Get valid email and password from .env
        # Please enter your own valid Recipe4Share email and password into the .env file to test logging in with valid and invalid credentials.
        load_dotenv()
        self.email = os.getenv("RECIPE4SHARE_EMAIL")  
        self.password = os.getenv("RECIPE4SHARE_PASSWORD")  

        # Used for registration
        self.domain = "txcct.com"
        self.registration_password = "Registration Password" # At least 8 characters

    ## Verify "Profile" and "Logout" buttons present after login with valid credentials
    def test_TC001(self):

        driver = self.driver        

        # Login with valid credentials
        login(driver, self.email, self.password)

        # Wait up to 5 seconds to check that "Profile" button is visible after login with valid credentials
        profile_button = WebDriverWait(driver, 5).until(
             EC.presence_of_element_located((By.XPATH, "//a[@href='/profile']"))
        )     
        assert profile_button.is_displayed(), "'Profile' button is not visible after login with valid credentials"

        # Wait up to 5 seconds to check that "Logout" button is visible after login with valid credentials
        logout_button = WebDriverWait(driver, 5).until(
             EC.presence_of_element_located((By.XPATH, "//a[@class='item' and .//text()='Logout']"))
        )     
        assert logout_button.is_displayed(), "'Logout' button is not visible after login with valid credentials"

        driver.quit()

    ## Verify error message appears after login with invalid credentials
    def test_TC002(self):

        driver = self.driver        

        # Login with valid credentials
        wrong_password = self.password + 'L'
        login(driver, self.email, wrong_password)

        # Wait up to 1 second to check that error message is visible after login with invalid credentials
        error_message = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ui.error.message"))
        )     
        assert error_message.is_displayed(), "Error message is not visible after login with invalid credentials"

        driver.quit()

    ## Verify error message appears after login with invalid credentials
    def test_TC002(self):

        driver = self.driver        

        # Login with valid credentials
        wrong_password = self.password + 'L'
        login(driver, self.email, wrong_password)

        # Wait up to 1 second to check that error message is visible after login with invalid credentials
        error_message = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ui.error.message"))
        )     
        assert error_message.is_displayed(), "Error message is not visible after login with invalid credentials"

        driver.quit()

    ## Verify registration with new username and new email
    def test_TC003(self):

        # Navigate to home page
        driver = self.driver  
        driver.get("https://www.recipe4share.com/")

        # Wait up to 1 second for login button to become clickable
        login_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='item' and text()='Login']"))
        )  

        # Click login button
        login_button.click()

        # Wait up to 1 second for sign up link to be present
        sign_up_link = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//a[text()='Sign Up']"))
        )
        
        # Click the "Sign Up" link
        sign_up_link.click()    

        # Wait up to 1 second for Create account modal to be visible
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='column' and text()='Create a new account']"))
        )

        # Enter new username
        username = str(int(time.time() * 1000))
        username_field = driver.find_element(By.XPATH, "//input[@placeholder='Enter your username' and @type='text']")
        username_field.send_keys(username)

        # Enter new email
        email = EMail(username=username, domain=self.domain)
        email_field = driver.find_element(By.XPATH, "//input[@type='email']")
        email_field.send_keys(email.address)

        # Enter password
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.send_keys(self.registration_password)

        # Enter password for confirmation
        confirm_password_field = driver.find_element(By.XPATH, "//input[@placeholder='Re-enter password' and @type='password']")
        confirm_password_field.send_keys(self.registration_password)

        # Click on submit button
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Signup')]")
        submit_button.click()

        # Wait up to 5 seconds for "Profile" button to appear after registration
        profile_button = WebDriverWait(driver, 5).until(
             EC.presence_of_element_located((By.XPATH, "//a[@href='/profile']"))
        )

        # Click on "Profile" button
        profile_button.click()

        # Check presence of "Hi, <username>" to indicate new user automatically logged in after registration
        greeting = driver.find_element(By.CLASS_NAME, "greetingContainer")
        expected_greeting_text = "Hi, " + username
        assert expected_greeting_text == greeting.text, f"Expected '{expected_greeting_text}' but found '{greeting.text}'"

        driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
