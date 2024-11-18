from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import json
import time

def fetch_marks_and_coefficients(driver):
    """Click each compartment, fetch marks and coefficients."""
    marks_data = []

    try:
        # Locate all mark compartments
        print("Locating all mark compartments...")
        compartments = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "liste_celluleGrid"))
        )

        for index, compartment in enumerate(compartments):
            try:
                # Scroll to the compartment and simulate a click
                print(f"Processing compartment [{index + 1}]...")
                driver.execute_script("arguments[0].scrollIntoView();", compartment)  # Ensure visibility
                compartment.click()

                # Wait for the detail section to load
                detail_section = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "Zone-DetailsNotes"))
                )

                # Parse the detail section to extract data
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")

                # Find the relevant detail section
                detail_section_soup = soup.find("section", class_="Zone-DetailsNotes")
                if not detail_section_soup:
                    print(f"Detail section not found for compartment [{index + 1}].")
                    continue

                # Extract subject, mark, date, and coefficient
                subject_element = detail_section_soup.select_one(".ie-titre-couleur-lowercase")
                mark_element = detail_section_soup.select(".ie-texte")[0] if detail_section_soup.select(".ie-texte") else None
                date_element = detail_section_soup.select_one("time")
                coefficient_element = detail_section_soup.find("span", string="Coefficient :")

                # Safely extract values or use defaults
                subject = subject_element.text.strip() if subject_element else "Unknown Subject"
                mark = mark_element.text.strip() if mark_element else "Unknown Mark"
                date = date_element.text.strip() if date_element else "Unknown Date"
                coefficient = coefficient_element.find_next("span").text.strip() if coefficient_element else "N/A"

                # Append data
                marks_data.append({
                    "subject": subject,
                    "mark": mark,
                    "date": date,
                    "coefficient": coefficient
                })

                # Print the structured data
                print(f"Subject: {subject}, Mark: {mark}, Date: {date}, Coefficient: {coefficient}")

                # Pause briefly
                time.sleep(0.5)

            except Exception as e:
                print(f"Error processing compartment [{index + 1}]: {e}")

        # Save the final data to a JSON file
        with open("marks_with_coefficients.json", "w", encoding="utf-8") as file:
            json.dump(marks_data, file, ensure_ascii=False, indent=4)

        # Print summary
        print("\nSummary of Extracted Data:")
        for entry in marks_data:
            print(f"Subject: {entry['subject']}, Mark: {entry['mark']}, Date: {entry['date']}, Coefficient: {entry['coefficient']}")

    except Exception as e:
        print("An error occurred while fetching marks and coefficients:", e)


def fetch_marks_page_source(driver):
    """Navigate to the marks page and return the updated page source."""
    if driver is None:
        print("Driver is not initialized.")
        return None

    try:
        # Step 1: Click on the "Tous Voir" button
        print("Attempting to locate the marks button...")
        marks_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_87id_45"))  # Adjust ID if necessary
        )
        marks_button.click()

        # Allow the page to load
        time.sleep(2)

        return driver.page_source

    except Exception as e:
        print("An error occurred while fetching marks:", e)
        return None


def login_and_fetch_marks_with_coefficients():
    """Login, navigate to marks page, and fetch marks with coefficients."""
    from auth import login_and_fetch_html  # Ensure your auth logic is intact
    page_source, driver = login_and_fetch_html()  # Get the initial page source and driver

    if not driver:
        print("Failed to initialize driver.")
        return

    try:
        # Navigate to the marks page
        fetch_marks_page_source(driver)

        # Fetch marks and coefficients by clicking compartments
        fetch_marks_and_coefficients(driver)

    finally:
        driver.quit()  # Quit the driver


# Run the function to test
if __name__ == "__main__":
    login_and_fetch_marks_with_coefficients()


# def fetch_marks_and_coefficients(driver):
#     """Click each compartment, fetch marks and coefficients."""
#     marks_data = []

#     try:
#         # Locate all mark compartments
#         print("Locating all mark compartments...")
#         compartments = WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.CLASS_NAME, "liste_celluleGrid"))
#         )

#         for index, compartment in enumerate(compartments):
#             try:
#                 # Scroll to the compartment and simulate a click
#                 print(f"Processing compartment [{index + 1}]...")
#                 driver.execute_script("arguments[0].scrollIntoView();", compartment)  # Ensure visibility
#                 compartment.click()

#                 # Dynamically find the related `_detail` section
#                 detail_section = WebDriverWait(driver, 5).until(
#                     EC.presence_of_element_located((By.CLASS_NAME, "Zone-DetailsNotes"))
#                 )

#                 # Parse the updated page source for the specific `_detail` section
#                 page_source = driver.page_source
#                 soup = BeautifulSoup(page_source, "html.parser")

#                 # Locate the currently expanded detail section by its unique attribute
#                 detail_section_soup = soup.find("section", class_="Zone-DetailsNotes")
                
#                 # Extract subject, mark, and coefficient
#                 subject = detail_section_soup.select_one(".ie-titre-couleur-lowercase").text.strip()
#                 mark = detail_section_soup.select(".ie-texte")[0].text.strip()  # First mark
#                 coefficient_element = detail_section_soup.find("span", text="Coefficient :")
#                 coefficient = coefficient_element.find_next("span").text.strip() if coefficient_element else "N/A"

#                 # Save data
#                 marks_data.append({
#                     "subject": subject,
#                     "mark": mark,
#                     "coefficient": coefficient
#                 })
#                 print(f"Subject: {subject}, Mark: {mark}, Coefficient: {coefficient}")

#                 # Pause briefly before interacting with the next block
#                 time.sleep(0.5)

#             except Exception as e:
#                 print(f"Error processing compartment [{index + 1}]: {e}")

#         # Save marks and coefficients to a JSON file
#         with open("marks_with_coefficients.json", "w", encoding="utf-8") as file:
#             json.dump(marks_data, file, ensure_ascii=False, indent=4)

#         # Print summary in terminal
#         print("\nSummary of Extracted Data:")
#         for entry in marks_data:
#             print(f"Subject: {entry['subject']}, Mark: {entry['mark']}, Coefficient: {entry['coefficient']}")

#     except Exception as e:
#         print("An error occurred while fetching marks and coefficients:", e)


# def fetch_marks_page_source(driver):
#     """Navigate to the marks page and return the updated page source."""
#     if driver is None:
#         print("Driver is not initialized.")
#         return None

#     try:
#         # Step 1: Click on the "Tous Voir" button
#         print("Attempting to locate the marks button...")
#         marks_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.ID, "id_87id_45"))  # Adjust ID if necessary
#         )
#         marks_button.click()

#         # Allow the page to load
#         time.sleep(2)

#         return driver.page_source

#     except Exception as e:
#         print("An error occurred while fetching marks:", e)
#         return None


# def login_and_fetch_marks_with_coefficients():
#     """Login, navigate to marks page, and fetch marks with coefficients."""
#     from auth import login_and_fetch_html  # Ensure your auth logic is intact
#     page_source, driver = login_and_fetch_html()  # Get the initial page source and driver

#     if not driver:
#         print("Failed to initialize driver.")
#         return

#     try:
#         # Navigate to the marks page
#         fetch_marks_page_source(driver)

#         # Fetch marks and coefficients by clicking compartments
#         fetch_marks_and_coefficients(driver)

#     finally:
#         driver.quit()  # Quit the driver


# # Run the function to test
# if __name__ == "__main__":
#     login_and_fetch_marks_with_coefficients()
