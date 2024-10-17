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
    
    # Setup Chrome options for headless mode
    options = webdriver.ChromeOptions()
    
    # Enable full headless mode
    options.add_argument("--headless")
    
    # Disable GPU and sandboxing for more efficient headless performance
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    # Disable images and unnecessary features for faster load times
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1920,1080")  # Optional: Set window size for page layout consistency
    
    # Initialize the Chrome driver with options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Navigate to the target URL
    driver.get(URL)

    # Wait for page to load randomly between 3-5 seconds
    time.sleep(random.uniform(3, 5))
    
    # Load credentials from a local JSON file
    with open('/Users/mbm/Desktop/Web-Scrapping/Web-scrapping-basics/config.json') as configFile:
        credentials = json.load(configFile)
        
        # Locate username and password input fields and perform "human-like" typing
        username_input = driver.find_element(By.ID, 'id_29')
        password_input = driver.find_element(By.ID, 'id_30')
        human_typing(username_input, credentials['USERNAME'])
        time.sleep(random.uniform(1, 2))
        human_typing(password_input, credentials['PASSWORD'])
        
        # Locate and click the login button
        login_button = driver.find_element(By.ID, 'id_18')
        login_button.click()

    # Wait for the page to load after login (random wait between 5-7 seconds)
    time.sleep(random.uniform(5, 7))
    
    # Get the HTML content of the page
    page_source = driver.page_source
    
    # Quit the browser after fetching the page source
    driver.quit()
    
    return page_source
