import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
from utils import human_typing

URL = 'https://3500044w.index-education.net/pronote/eleve.html'

def login_and_fetch_html():
    """Login to Pronote and save the page HTML to a file."""
    options = webdriver.ChromeOptions()
    
    # Enable headless mode
    # options.add_argument("--headless")
    
    # Optional: Other configurations for headless mode
    options.add_argument("--window-size=1920,1080")  # Set the window size (since no UI will be rendered)
    options.add_argument("--disable-gpu")  # Disable GPU, often recommended for headless
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(URL)

    time.sleep(random.uniform(3, 5))
    with open('/Users/mbm/Desktop/Web-Scrapping/Web-scrapping-basics/config.json') as configFile:
        credentials = json.load(configFile)
        username_input = driver.find_element(By.ID, 'id_29')
        password_input = driver.find_element(By.ID, 'id_30')
        human_typing(username_input, credentials['USERNAME'])
        time.sleep(random.uniform(1, 2))
        human_typing(password_input, credentials['PASSWORD'])
        login_button = driver.find_element(By.ID, 'id_18')
        login_button.click()

    time.sleep(random.uniform(5, 7))
    page_source = driver.page_source
    driver.quit()
    return page_source
