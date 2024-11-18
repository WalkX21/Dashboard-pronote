import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re

# URL of the Pronote site
URL = 'https://3500044w.index-education.net/pronote/eleve.html'

def login_and_fetch_html():
    """Login to Pronote and return the driver for further navigation."""

    # Set up undetected-chromedriver with DevTools Protocol enabled
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1920,1080")

    # Initialize the Chrome driver with undetected-chromedriver
    driver = uc.Chrome(options=options)

    try:
        # Navigate to the login page
        driver.get(URL)
        time.sleep(3)  # Wait for page to load

        # Load credentials from JSON file
        with open('/Users/mbm/Desktop/Web-Scrapping/Dashboard-pronote/config.json') as configFile:
            credentials = json.load(configFile)
        
        # Perform login
        username_input = driver.find_element(By.ID, 'id_29')
        password_input = driver.find_element(By.ID, 'id_30')
        username_input.send_keys(credentials['USERNAME'])
        time.sleep(1)
        password_input.send_keys(credentials['PASSWORD'])
        login_button = driver.find_element(By.ID, 'id_18')
        login_button.click()

        # Wait for login to complete
        time.sleep(5)
        return driver
    
    except Exception as e:
        print("An error occurred during login:", e)
        driver.quit()
        return None

def capture_network_after_button_click(driver):
    """Click necessary elements and capture network traffic."""
    if driver is None:
        print("Driver is not initialized.")
        return

    try:
        # Enable network logging
        driver.execute_cdp_cmd("Network.enable", {})

        # Click on the main "marks" button
        print("Attempting to locate the marks button...")
        marks_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_87id_45"))
        )
        marks_button.click()
        time.sleep(3)

        # Click the "Tous Voir" button
        print("Attempting to locate and click the 'Tous Voir' button...")
        tous_voir_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_87id_45"))
        )
        tous_voir_button.click()
        time.sleep(3)

        # Capture network logs after clicking the "Tous Voir" button
        print("Capturing network requests...")
        time.sleep(5)  # Adjust if needed for network traffic to load

        logs = driver.get_log("performance")
        file_counter = 1

        for entry in logs:
            log_message = json.loads(entry["message"])["message"]
            if log_message["method"] == "Network.responseReceived":
                request_id = log_message["params"]["requestId"]
                url = log_message["params"]["response"]["url"]
                response = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
                body = response.get("body", "")
                
                # Save each response to a text file
                filename = f"network_response_{file_counter}.txt"
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(body)
                
                print(f"Saved response from {url} to {filename}")
                file_counter += 1

    except Exception as e:
        print("An error occurred while capturing network data or saving responses:", e)

def login_and_fetch_marks():
    """Login, navigate to marks page, and capture network data after clicks."""
    # Login and initialize the driver with undetected-chromedriver
    driver = login_and_fetch_html()

    if not driver:
        print("Failed to initialize driver.")
        return

    # Capture network data after clicking buttons
    capture_network_after_button_click(driver)
    driver.quit()

# Run the function to test
if __name__ == "__main__":
    login_and_fetch_marks()
