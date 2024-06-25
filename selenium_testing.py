
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open a webpage
driver.get("https://www.recipe4share.com/")

# Print the title of the page
print("Title: ", driver.title)

# Find an element by its name attribute and print its text
element = driver.find_element(By.CLASS_NAME, "website-title")
print("Element text: ",  element.is_displayed())

# Close the browser
driver.quit()