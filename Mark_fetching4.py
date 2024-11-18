from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
from Mark_fetching import fetch_marks_page_source

def fetch_coefficients(driver):
    """Click each compartment and fetch coefficients."""
    coefficients_data = []

    try:
        # Locate all mark compartments
        print("Fetching coefficients...")
        compartments = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "liste_celluleGrid"))
        )

        for index, compartment in enumerate(compartments):
            try:
                print(f"Processing compartment [{index + 1}]...")
                driver.execute_script("arguments[0].scrollIntoView();", compartment)
                compartment.click()

                # Wait for the detail section to load
                detail_section = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "Zone-DetailsNotes"))
                )

                # Parse the detail section to extract the coefficient
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")
                detail_section_soup = soup.find("section", class_="Zone-DetailsNotes")

                coefficient_element = detail_section_soup.find("span", string="Coefficient :")
                coefficient = coefficient_element.find_next("span").text.strip() if coefficient_element else "N/A"

                coefficients_data.append(coefficient)

                print(f"Compartment [{index + 1}] Coefficient: {coefficient}")

            except Exception as e:
                print(f"Error processing coefficient for compartment [{index + 1}]: {e}")

        return coefficients_data

    except Exception as e:
        print("An error occurred while fetching coefficients:", e)
        return []


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

    return mark_entries


def combine_marks_and_coefficients(marks_data, coefficients_data):
    """Combine marks and coefficients into a single dataset."""
    combined_data = []

    for index, mark_entry in enumerate(marks_data):
        coefficient = coefficients_data[index] if index < len(coefficients_data) else "N/A"
        combined_data.append({**mark_entry, "coefficient": coefficient})

    # Save the combined data to JSON
    with open("combined_marks.json", "w", encoding="utf-8") as file:
        json.dump(combined_data, file, ensure_ascii=False, indent=4)

    # Print the combined data
    print("\nCombined Marks and Coefficients:")
    for entry in combined_data:
        print(entry)


def login_and_fetch_marks_with_coefficients():
    """Login, navigate to marks page, and fetch marks with coefficients."""
    from auth import login_and_fetch_html  # Ensure your auth logic is intact
    page_source, driver = login_and_fetch_html()  # Get the initial page source and driver

    if not driver:
        print("Failed to initialize driver.")
        return

    try:
        # Step 1: Fetch marks page source
        print("Fetching marks page...")
        marks_page_source = fetch_marks_page_source(driver)

        # Step 2: Parse marks
        marks_data = parse_marks_from_html(marks_page_source)

        # Step 3: Fetch coefficients
        coefficients_data = fetch_coefficients(driver)

        # Step 4: Combine marks and coefficients
        combine_marks_and_coefficients(marks_data, coefficients_data)

    finally:
        driver.quit()  # Quit the driver


if __name__ == "__main__":
    login_and_fetch_marks_with_coefficients()
