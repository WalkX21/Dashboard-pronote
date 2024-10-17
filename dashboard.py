import streamlit as st
from datetime import datetime, timedelta
from auth import login_and_fetch_html
from html_parsing import inspect_html_sections
import pytz

# Use session state to store DS data and manual entries
if 'ds_data' not in st.session_state:
    st.session_state['ds_data'] = []
if 'manual_entries' not in st.session_state:
    st.session_state['manual_entries'] = []

# Define timezone (for example, Casablanca timezone)
CASABLANCA_TZ = pytz.timezone('Africa/Casablanca')

def make_timezone_aware(dt):
    """Convert naive datetime to timezone-aware using the Casablanca timezone."""
    if dt.tzinfo is None:
        return CASABLANCA_TZ.localize(dt)
    return dt

def fetch_and_display_ds_data():
    """Fetch and display DS and Evaluation data when the app starts."""
    if not st.session_state['ds_data']:  # Only fetch if not already fetched
        st.info("Fetching DS and Evaluation data...")
        page_source = login_and_fetch_html()  # Web scraping
        ds_list = inspect_html_sections(page_source)  # Process the HTML
        st.session_state['ds_data'] = ds_list  # Store data in session state
    
    # Combine web scraped data with manually added entries
    combined_list = st.session_state['ds_data'] + st.session_state['manual_entries']

    # Ensure all datetimes are timezone-aware
    for entry in combined_list:
        entry['start_time'] = make_timezone_aware(entry['start_time'])
        entry['end_time'] = make_timezone_aware(entry['end_time'])

    # Sort by start time
    combined_list.sort(key=lambda x: x['start_time'])

    # Display DS and Evaluations
    if combined_list:
        st.write("### Exams (DS and Evaluations) Found:")
        for ds in combined_list:
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
    start_date = st.sidebar.date_input("Start Date", datetime.now())
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

        # Add the entry to the manual_entries list in session state
        new_entry = {
            'subject': title,
            'start_time': start_datetime,
            'end_time': end_datetime,
            'location': location,
            'type': ds_type
        }

        # Store the new entry
        st.session_state['manual_entries'].append(new_entry)

        # Success message
        st.sidebar.success(f"{ds_type} '{title}' added successfully!")

        # Just show the updated DS/Evaluation data right away
        st.session_state['ds_data'] = st.session_state['ds_data']  # Force a refresh of data

def main():
    st.title("Pronote DS and Evaluation Dashboard")
    st.write("Welcome to the Pronote Dashboard!")

    # Form for adding a new DS or Evaluation
    add_manual_entry()

    # Fetch and display existing data
    fetch_and_display_ds_data()

if __name__ == "__main__":
    main()
