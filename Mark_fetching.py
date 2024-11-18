
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
# from auth import login_and_fetch_html
from auth import login_and_fetch_html
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import random
import json
from bs4 import BeautifulSoup


def fetch_marks_page_source(driver):
    """Navigate to the marks page, click necessary elements, and return the page source."""
    if driver is None:
        print("Driver is not initialized.")
        return None

    try:
        # Step 1: Click on the main "marks" button
        print("Attempting to locate the marks button with updated ID...")
        marks_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_87id_45"))
        )
        marks_button.click()
        # time.sleep(random.uniform(3, 5))
        time.sleep(1.5)

        # Step 2: Try to activate the "Par matière" filter
        print("Attempting to activate the 'Par matière' filter...")

        # Approach A: Click the input element directly
        try:
            par_matiere_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "cb-g8-gen-for"))
            )
            par_matiere_input.click()
            print("Clicked 'Par matière' input directly.")
        except Exception:
            print("Direct click on 'Par matière' input failed, trying JavaScript methods...")

            # Approach B: Use JavaScript to click on the label
            try:
                driver.execute_script("document.querySelector(\"label[for='cb-g8-gen-for']\").click()")
                print("Activated 'Par matière' via JavaScript on the label.")
            except Exception as js_label_error:
                print("JavaScript click on the label failed:", js_label_error)

            # Approach C: Use JavaScript to directly select the input
            try:
                driver.execute_script("document.getElementById('cb-g8-gen-for').checked = true;")
                driver.execute_script("document.getElementById('cb-g8-gen-for').dispatchEvent(new Event('change'));")
                print("Activated 'Par matière' via JavaScript on the input.")
            except Exception as js_input_error:
                print("JavaScript activation on the input failed:", js_input_error)

        # Step 3: Fetch and save the updated page source for marks
        time.sleep(1.5)  # Allow time for the page to update
        marks_page_source = driver.page_source
        with open("marks_page.html", "w", encoding="utf-8") as file:
            file.write(marks_page_source)  # Save HTML for inspection

        return marks_page_source

    except Exception as e:
        print("An error occurred while fetching marks:", e)
        return None


def parse_marks_from_html(html):
    """Parse the HTML page source to extract all marks data."""
    soup = BeautifulSoup(html, "html.parser")
    mark_entries = []

    # Use a flexible approach to iterate over marks
    mark_sections = soup.find_all("div", class_="liste_celluleGrid")
    for mark_section in mark_sections:
        try:
            date = mark_section.select_one("time.date-contain")["datetime"]
            subject = mark_section.select_one(".titre-principal .ie-ellipsis").text.strip()
            class_avg = mark_section.select_one(".infos-supp span").text.split(":")[-1].strip()
            user_mark = mark_section.select_one(".note-devoir").text.strip()

            # Save the parsed data
            mark_entries.append({
                "date": date,
                "subject": subject,
                "class_average": class_avg,
                "user_mark": user_mark
            })
            print(f"Date: {date}, Subject: {subject}, Class Average: {class_avg}, User Mark: {user_mark}")

        except AttributeError as e:
            print("Error parsing mark section:", e)

    # Save all entries to JSON file
    with open("marks_data.json", "w", encoding="utf-8") as file:
        json.dump(mark_entries, file, ensure_ascii=False, indent=4)

    return mark_entries



def login_and_fetch_marks():
    """Login, navigate to marks page, and fetch marks data."""
    page_source, driver = login_and_fetch_html()  # Get the initial page source and driver

    if not driver:
        print("Failed to initialize driver.")
        return

    # Fetch the marks page after navigation
    marks_page_source = fetch_marks_page_source(driver)
    driver.quit()  # Quit driver after fetching the page source

    if not marks_page_source:
        print("Failed to fetch marks page source.")
        return

    # Parse and print marks
    mark_data = parse_marks_from_html(marks_page_source)
    print("Final extracted mark data:", mark_data)

# Run the function to test
if __name__ == "__main__":
    login_and_fetch_marks()