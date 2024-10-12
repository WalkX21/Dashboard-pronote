from auth import login_and_fetch_html
from calendar_utils import open_ics_with_calendar
from html_parsing import inspect_html_sections

def main():
    # Step 1: Log in and fetch the HTML (update the file each time)
    page_source = login_and_fetch_html()

    # Step 2: Inspect the HTML and create the .ics calendar
    inspect_html_sections(page_source)

    # Step 3: Automatically open the .ics file in Apple Calendar
    open_ics_with_calendar()

if __name__ == "__main__":
    main()
