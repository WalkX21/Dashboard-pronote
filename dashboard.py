import streamlit as st
from auth import login_and_fetch_html
from html_parsing import inspect_html_sections

def fetch_and_display_ds_data():
    """Fetch and display DS and Evaluation data when the app launches."""
    st.info("Fetching DS and Evaluation data...")

    # Fetch the HTML
    page_source = login_and_fetch_html()
    ds_list = inspect_html_sections(page_source)

    if ds_list:
        st.write("### Exams (DS and Evaluations) Found:")
        for ds in ds_list:
            ds_type = ds['type']  # 'DS' or 'Evaluation'
            ds_title = ds['subject']
            ds_start = ds['start_time'].strftime("%Y-%m-%d %H:%M")
            ds_end = ds['end_time'].strftime("%Y-%m-%d %H:%M")
            ds_room = ds['location']

            # Display each DS or Evaluation
            st.write(f"**[{ds_type}] {ds_title}**")
            st.write(f"🗓 Start: {ds_start}")
            st.write(f"🕔 End: {ds_end}")
            st.write(f"📍 Location: {ds_room}")
            st.write("---")
    else:
        st.warning("No exams (DS or Evaluations) found.")

def main():
    st.title("Pronote DS and Evaluation Dashboard")
    st.write("Welcome to the Pronote Dashboard!")

    # Fetch and display data directly when the app launches
    fetch_and_display_ds_data()

if __name__ == "__main__":
    main()
