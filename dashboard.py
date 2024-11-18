import streamlit as st
from datetime import datetime, timedelta
import json
import os
import pytz
from streamlit.components.v1 import html
import pandas as pd
from auth import login_and_fetch_html
from html_parsing import inspect_html_sections
from homework_scraping import fetch_and_save_homework
from html_parsing import fetch_and_save_ds_evals
from utils import save_json, load_json

from utils import save_data, load_data, make_timezone_aware, human_typing, events_are_equal

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from datetime import datetime
# import time

# def login_and_fetch_marks():
#     # Step 1: Login to Pronote
#     driver = login_and_fetch_html()  # Assuming this function logs in and returns a driver instance
    
#     try:
#         # Step 2: Navigate to Marks page by clicking the button
#         # Wait until the button is clickable and then click it
#         marks_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.ID, "id_521id_45"))
#         )
#         marks_button.click()
#         time.sleep(3)  # Wait for the page to load; adjust as needed based on loading times

#         # Step 3: Extract marks data
#         marks_data = []
#         index = 0
#         while True:
#             try:
#                 # Locate each grid entry
#                 date_element = driver.find_element(By.XPATH, f"//div[@id='GInterface.Instances[2].Instances[1]_0_{index}_fdz_2']/time")
#                 subject_element = driver.find_element(By.XPATH, f"//div[@id='GInterface.Instances[2].Instances[1]_0_{index}_fdz_4']")
#                 class_average_element = driver.find_element(By.XPATH, f"//div[@id='GInterface.Instances[2].Instances[1]_0_{index}_fdz_5']/span")
#                 user_mark_element = driver.find_element(By.XPATH, f"//div[@id='GInterface.Instances[2].Instances[1]_0_{index}_fdz_6']/span[@class='note-devoir']")

#                 # Extract text from each element
#                 date = date_element.get_attribute("datetime")  # ISO format
#                 subject = subject_element.text
#                 class_average = class_average_element.text.split(":")[1].strip()  # "Moyenne classe : 8,17" -> "8,17"
#                 user_mark = user_mark_element.text.replace(",", ".")  # Convert to "7.5" format if needed

#                 # Append to list
#                 marks_data.append({
#                     "date": date,
#                     "subject": subject,
#                     "class_average": class_average,
#                     "user_mark": user_mark
#                 })
                
#                 # Print extracted data for debugging
#                 print(f"Date: {date}, Subject: {subject}, Class Average: {class_average}, User Mark: {user_mark}")
                
#                 # Increment index to move to the next entry
#                 index += 1
#             except Exception as e:
#                 # If no further entries are found, break out of the loop
#                 print(f"No more marks found or an error occurred: {e}")
#                 break

#     finally:
#         # Close the driver after completion
#         driver.quit()

#     return marks_data  # Returning the data if needed for further processing

st.set_page_config(page_title="Accueil", page_icon="📚", layout="wide")

# Define the path to the JSON file for storing DS and Evaluations
MOOD_DATA_FILE = "mood_data.csv"
CONFIG_PATH = "config.json"
DATA_FILE = "/Users/mbm/Desktop/Web-Scrapping/Dashboard-pronote/ds_evals.json"
CASABLANCA_TZ = pytz.timezone('Africa/Casablanca')



def load_config():
    """Load configuration from config.json, handling cases where the file may be empty or malformed."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}  # Return an empty dictionary if JSON is invalid or empty
    return {}

def save_config(data):
    """Save configuration data to config.json."""
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)

def is_user_registered():
    """Check if user data is already in config.json."""
    config = load_config()
    return "user_id" in config and "key" in config
def signup_page():
    st.title("Sign Up")
    st.write("Please register your ID and Pronote credentials.")
    
    # Collect data for the config.json
    user_id = st.text_input("User ID")
    key = st.text_input("Key (Password)", type="password")
    pronote_username = st.text_input("Pronote Username")
    pronote_password = st.text_input("Pronote Password", type="password")

    if st.button("Sign Up"):
        if user_id and key and pronote_username and pronote_password:
            # Save data to config.json
            save_config({
                "user_id": user_id,
                "key": key,
                "USERNAME": pronote_username,
                "PASSWORD": pronote_password
            })
            st.success("Sign-up successful! Please log in.")
            st.rerun()
        else:
            st.warning("Please fill in all fields.")

def login_page():
    st.title("Login")
    st.write("Please enter your ID and key to access the dashboard.")

    # Collect login credentials
    user_id = st.text_input("User ID")
    key = st.text_input("Key (Password)", type="password")

    if st.button("Login"):
        config = load_config()
        if user_id == config.get("user_id") and key == config.get("key"):
            st.success("Login successful!")
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid ID or key. Please try again.")

def make_timezone_aware(dt):
    """Convert naive datetime to timezone-aware using the Casablanca timezone."""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    if dt.tzinfo is None:
        return CASABLANCA_TZ.localize(dt)
    return dt

def save_ds_evals(data):
    """Save all DS and Evaluations to a JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, default=str)

def load_ds_evals():
    """Load DS and Evaluations from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def is_duplicate_entry(new_entry, current_data):
    """Check if the new entry is a duplicate."""
    for entry in current_data:
        if (entry['subject'] == new_entry['subject'] and
            entry['start_time'] == new_entry['start_time'] and
            entry['end_time'] == new_entry['end_time'] and
            entry['location'] == new_entry['location'] and
            entry['type'] == new_entry['type']):
            return True
    return False

def fetch_and_update_ds_evals():
    """Fetch DS and Evaluations from the web and update the JSON file."""
    page_source = login_and_fetch_html()  # Web scraping
    ds_list = inspect_html_sections(page_source)  # Process the HTML

    # Load current data from JSON
    current_data = load_ds_evals()

    # Add scraped DS and Evaluations to the current data, avoiding duplicates
    for ds in ds_list:
        ds['start_time'] = ds['start_time'].isoformat()
        ds['end_time'] = ds['end_time'].isoformat()

        if not is_duplicate_entry(ds, current_data):
            current_data.append(ds)

    # Save the updated data back to JSON
    save_ds_evals(current_data)

    # Update session state
    st.session_state['ds_evals'] = current_data


def add_manual_homework():
    """Form to manually add a homework."""
    st.write("### Add New Homework")

    # Subject, title, due date input
    subject = st.text_input("Subject")
    title = st.text_input("Title")
    due_date = st.date_input("Due Date", datetime.now().date())
    # importance = st.slider("Importance (1-5)", 1, 5, 1)
    importance = st.selectbox("Importance", options=["High", "Normal", "Low"])
    if st.button("Add Homework"):
        # New homework entry with status 'Pending'
        new_homework = {
            'subject': subject,
            'title': title,
            'due_date': due_date.isoformat(),
            'importance': importance,
            'status': 'Pending'  # All homework starts as Pending
        }

        # Load existing homework data
        homework_data = load_json("homework.json")

        # Append the new homework and save back to the file
        homework_data.append(new_homework)
        save_json("homework.json", homework_data)

        st.success(f"Homework '{title}' added successfully!")


def display_ds_evals(show_week_only=False):
    """Display upcoming DS and Evaluations only."""
    if 'ds_evals' not in st.session_state:
        st.session_state['ds_evals'] = load_ds_evals()

    # Ensure datetimes are timezone-aware
    timezone = pytz.timezone('Africa/Casablanca')
    current_time = datetime.now(timezone)
    end_of_week = current_time + timedelta(days=7) if show_week_only else None

    # Filter and sort by start time
    upcoming_ds_evals = []
    for ds in st.session_state['ds_evals']:
        ds['start_time'] = make_timezone_aware(ds['start_time'])
        ds['end_time'] = make_timezone_aware(ds['end_time'])
        if ds['start_time'] >= current_time and (end_of_week is None or ds['start_time'] <= end_of_week):
            upcoming_ds_evals.append(ds)

    # Sort the filtered list by start time
    upcoming_ds_evals.sort(key=lambda x: x['start_time'])

    # Display filtered DS and Evaluations
    if upcoming_ds_evals:
        st.write("### Upcoming Exams (DS and Evaluations):")
        for ds in upcoming_ds_evals:
            ds_type = ds['type']
            ds_title = ds['subject']
            ds_start = ds['start_time'].strftime("%Y-%m-%d %H:%M")
            ds_end = ds['end_time'].strftime("%Y-%m-%d %H:%M")
            ds_room = ds['location']

            st.write(f"**[{ds_type}] {ds_title}**")
            st.write(f"🗓 Start: {ds_start}")
            st.write(f"🕔 End: {ds_end}")
            st.write(f"📍 Location: {ds_room}")
            st.write("---")
    else:
        st.warning("No upcoming exams (DS or Evaluations) found.")



def add_manual_entry():
    """Form to manually add DS or Evaluation."""
    st.write("## Add New DS or Evaluation")

    # Type selector (DS or Evaluation)
    ds_type = st.selectbox("Type", ["DS", "Evaluation"])

    # Date and time picker
    start_date = st.date_input("Start Date", datetime.now().date())
    start_time = st.time_input("Start Time", datetime.now())
    duration = st.slider("Duration (hours)", 1, 6, 1)  # Slider for duration

    # Title and location input
    title = st.text_input("Title")
    location = st.text_input("Location")

    # Button to submit and add the entry
    if st.button("Add Entry"):
        # Combine the start date and time into a single datetime object
        start_datetime = datetime.combine(start_date, start_time)
        start_datetime = make_timezone_aware(start_datetime)  # Make start time timezone-aware
        end_datetime = start_datetime + timedelta(hours=duration)

        # Create the new DS or Evaluation entry
        new_entry = {
            'subject': title,
            'start_time': start_datetime.isoformat(),
            'end_time': end_datetime.isoformat(),
            'location': location,
            'type': ds_type
        }

        # Load current data from JSON
        current_data = load_ds_evals()

        # Add the new entry to the current data, avoiding duplicates
        if not is_duplicate_entry(new_entry, current_data):
            current_data.append(new_entry)

            # Save the updated data back to JSON
            save_ds_evals(current_data)

            # Update session state
            st.session_state['ds_evals'] = current_data

            # Success message
            st.success(f"{ds_type} '{title}' added successfully!")
            st.rerun()  # Re-run to update the page
        else:
            st.warning(f"{ds_type} '{title}' already exists in the system!")



def display_homework(show_week_only=False):
    """Display upcoming homework from 'homework.json', optionally limited to the current week."""
    homework = load_data("homework.json")

    # Get the current date and timezone-aware time
    timezone = pytz.timezone('Africa/Casablanca')
    current_time = datetime.now(timezone)
    end_of_week = current_time + timedelta(days=7) if show_week_only else None

    # Remove duplicates and add 'Not Done' default status
    unique_homework = []
    seen_entries = set()
    for hw in homework:
        identifier = (hw['subject'], hw['title'], hw['due_date'])
        if identifier not in seen_entries:
            seen_entries.add(identifier)
            hw['status'] = hw.get('status', 'Not Done')
            unique_homework.append(hw)

    # Filter and sort homework by due date and status
    filtered_homework = []
    for hw in unique_homework:
        hw_due = make_timezone_aware(hw['due_date'])
        if hw_due >= current_time and (end_of_week is None or hw_due <= end_of_week):
            filtered_homework.append(hw)

    if filtered_homework:
        filtered_homework.sort(key=lambda hw: (hw['status'] == 'Done', hw_due))

        st.write("### Upcoming Homework (Sorted by Date and Status)")
        for i, hw in enumerate(filtered_homework):
            is_done = hw['status'] == 'Done'
            checkbox_label = f"{hw['subject']} - {hw['title']}"
            if st.checkbox(checkbox_label, value=is_done, key=f"homework_{hw['title']}_{i}"):
                hw['status'] = 'Done'
            else:
                hw['status'] = 'Not Done'

            st.write(f"📅 Due: {hw_due.strftime('%Y-%m-%d')}")
            st.write(f"Importance: {hw['importance']}")
            st.write("---")

        save_data("homework.json", unique_homework)
    else:
        st.warning("No upcoming homework found.")


if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

    


def main():
    st.title("Pronify beta ver 2.0")

    # Check authentication status
    if not st.session_state.get("authenticated", False):
        if is_user_registered():
            login_page()
        else:
            signup_page()
    else:
        if 'scraped' not in st.session_state:
            st.session_state['scraped'] = False  # To track if scraping was done

        # Check if scraping is done
        if not st.session_state['scraped']:
            st.write("Scraping data...")
            # page_source = login_and_fetch_html() 
            #  # Perform web scraping (logging into Pronote)
            page_source, driver = login_and_fetch_html()
            # Scrape DS and Evaluations
            fetch_and_save_ds_evals(page_source)

            # Scrape Homework
            fetch_and_save_homework(page_source)

            # Mark that scraping has been done in this session
            st.session_state['scraped'] = True

        # Create two columns for layout
        col1, col2 = st.columns(2)

        # Column 1: DS and Evaluations
        with col1:
            st.write("## DS and Evaluations (This Week)")
            display_ds_evals(show_week_only=True)  # Display only the DS/Evals for the next 7 days
            
            # Uncomment the line below to enable manual DS/Eval entries
            # add_manual_entry()

        # Column 2: Homework
        with col2:
            st.write("## Homework (This Week)")
            display_homework(show_week_only=True)  # Display only the homework for the next 7 days
            
            # Uncomment the line below to enable manual homework entries
            # add_manual_homework()



if __name__ == "__main__":
    main()