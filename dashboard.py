import streamlit as st
from datetime import datetime, timedelta
import json
import os
import pytz
from auth import login_and_fetch_html
from html_parsing import inspect_html_sections

# Define the path to the JSON file for storing DS and Evaluations
DATA_FILE = "ds_evals.json"
CASABLANCA_TZ = pytz.timezone('Africa/Casablanca')

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

def display_ds_evals():
    """Display all DS and Evaluations."""
    if 'ds_evals' not in st.session_state:
        st.session_state['ds_evals'] = load_ds_evals()

    # Ensure all datetimes are timezone-aware
    for ds in st.session_state['ds_evals']:
        ds['start_time'] = make_timezone_aware(ds['start_time'])
        ds['end_time'] = make_timezone_aware(ds['end_time'])

    # Sort by start time
    st.session_state['ds_evals'].sort(key=lambda x: x['start_time'])

    # Display DS and Evaluations
    if st.session_state['ds_evals']:
        st.write("### Exams (DS and Evaluations) Found:")
        for ds in st.session_state['ds_evals']:
            ds_type = ds['type']  # 'DS' or 'Evaluation'
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
        st.warning("No exams (DS or Evaluations) found.")

def add_manual_entry():
    """Form to manually add DS or Evaluation."""
    st.sidebar.title("Add New DS or Evaluation")

    # Type selector
    ds_type = st.sidebar.selectbox("Type", ["DS", "Evaluation"])

    # Date and time picker
    start_date = st.sidebar.date_input("Start Date", datetime.now().date())
    start_time = st.sidebar.time_input("Start Time", datetime.now())
    duration = st.sidebar.slider("Duration (hours)", 1, 6, 1)  # Slider for duration

    # Title and location input
    title = st.sidebar.text_input("Title")
    location = st.sidebar.text_input("Location")

    # We only update the DS list when the user clicks "Add Entry"
    if st.sidebar.button("Add Entry"):
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
            st.sidebar.success(f"{ds_type} '{title}' added successfully!")
        else:
            st.sidebar.warning(f"{ds_type} '{title}' already exists in the system!")

def main():
    st.title("Pronote DS and Evaluation Dashboard")
    st.write("Welcome to the Pronote Dashboard!")

    # Automatically load and display DS and Evaluations without needing a button
    display_ds_evals()

    # Form for adding a new DS or Evaluation
    add_manual_entry()

if __name__ == "__main__":
    main()
