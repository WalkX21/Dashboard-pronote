from bs4 import BeautifulSoup
from datetime import datetime
from utils import save_data, load_data, make_timezone_aware
import re

HOMEWORK_FILE = "/Users/mbm/Desktop/Web-Scrapping/Dashboard-pronote/homework.json"

def scrape_homework(page_source):
    """Scrape homework data from Pronote HTML."""
    soup = BeautifulSoup(page_source, 'html.parser')
    homework_list = []

    # Locate the homework section
    homework_section = soup.find("div", class_="conteneur-liste-CDT")

    last_valid_date = None  # Keep track of the most recent valid date

    if homework_section:
        # Find all homework items within the section
        homework_items = homework_section.find_all("li")

        for hw_item in homework_items:
            # Extract the due date (if available)
            due_date_tag = hw_item.find("h3")
            if due_date_tag:
                due_date_str = due_date_tag.get_text(strip=True)
                due_date = parse_homework_date(due_date_str)
                last_valid_date = due_date  # Update the most recent valid date
            else:
                # If no date is found, use the last valid date
                due_date = last_valid_date
                print("No date found, using the last valid date:", due_date)

            # Extract the subject (inside span with class "titre-matiere")
            subject_tag = hw_item.find("span", class_="titre-matiere")
            subject = subject_tag.get_text(strip=True) if subject_tag else "Unknown Subject"

            # Extract homework description (inside div with class "description")
            description_tag = hw_item.find("div", class_="description")
            description = description_tag.get_text(strip=True) if description_tag else "No Description"

            # Append the homework item to the list
            if due_date:
                homework_list.append({
                    'subject': subject,
                    'title': description,
                    'due_date': make_timezone_aware(due_date).isoformat(),
                    'importance': 'Normal'  # Default importance level
                })
            else:
                print(f"Missing or invalid date for {subject}, but adding to the list.")

    else:
        print("No homework section found.")
    
    return homework_list

def parse_homework_date(date_str):
    """Parse the due date string from Pronote."""
    month_map = {
        'janv.': 1, 'févr.': 2, 'mars': 3, 'avr.': 4, 'mai': 5, 'juin': 6,
        'juil.': 7, 'août': 8, 'sept.': 9, 'oct': 10, 'oct.': 10, 'nov': 11, 'nov.': 11, 'déc': 12, 'déc.': 12
    }

    print(f"Parsing date string: {date_str}")

    pattern = r"(\w+)\s(\d+)\s(\w+)"
    match = re.search(pattern, date_str)

    if match:
        day_name, day, month_str = match.groups()
        print(f"Matched day_name: {day_name}, day: {day}, month_str: {month_str}")

        # Normalize month string (handle both with and without period)
        month = month_map.get(month_str.lower().strip('.'))

        if month is None:
            print(f"Month '{month_str}' could not be found in month_map!")
            return None

        return datetime(2024, month, int(day))  # Adjust year as necessary
    else:
        print(f"Date string '{date_str}' did not match the expected pattern.")
        return None

def fetch_and_save_homework(page_source):
    """Fetch homework and save to homework.json with debugging."""
    homework_list = scrape_homework(page_source)

    # Debugging: Check if homework scraping is working
    if not homework_list:
        print("No homework found in the scraped HTML.")
    else:
        print(f"Homework found: {homework_list}")

    # Load existing homework data
    current_homework = load_data(HOMEWORK_FILE)

    # Add new homework entries, avoid duplicates
    for hw in homework_list:
        if hw not in current_homework:
            current_homework.append(hw)

    # Save updated homework data
    save_data(HOMEWORK_FILE, current_homework)

    # Debugging: Check the final homework list after saving
    print(f"Final homework list stored in {HOMEWORK_FILE}: {current_homework}")

