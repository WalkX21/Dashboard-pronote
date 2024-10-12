from bs4 import BeautifulSoup
from calendar_utils import create_calendar_with_ds
from datetime import datetime, timedelta
import pytz
import re

def parse_date_time(ds_date_str):
    """Parse the date and time from strings like 'Aujourd'hui de 08h00 à 10h00' or 'Le mercredi 16 oct. de 08h00 à 10h00'."""
    today = datetime.now()
    
    if "Aujourd'hui" in ds_date_str:
        # Replace 'Aujourd'hui' with today's date
        date_str = today.strftime("%d %b")
        ds_date_str = ds_date_str.replace("Aujourd'hui", f"Le {date_str}")
    elif "Demain" in ds_date_str:
        # Replace 'Demain' with tomorrow's date
        tomorrow = today + timedelta(days=1)
        date_str = tomorrow.strftime("%d %b")
        ds_date_str = ds_date_str.replace("Demain", f"Le {date_str}")

    pattern = r"Le (\w+) (\d+) (\w+)\.? de (\d+h\d+) à (\d+h\d+)"
    match = re.search(pattern, ds_date_str)

    if match:
        day_name, day, month_name, start_time_str, end_time_str = match.groups()

        month_map = {
            'janv.': 1, 'févr.': 2, 'mars': 3, 'avr.': 4,
            'mai': 5, 'juin': 6, 'juil.': 7, 'août': 8,
            'sept.': 9, 'oct': 10, 'nov': 11, 'déc.': 12
        }
        month = month_map.get(month_name.lower(), None)
        
        if month is None:
            raise ValueError(f"Unknown month name: {month_name}")

        year = today.year  # Set the year based on the current year

        # Convert time strings into datetime objects
        start_time = datetime.strptime(start_time_str, "%Hh%M").replace(year=year, month=month, day=int(day))
        end_time = datetime.strptime(end_time_str, "%Hh%M").replace(year=year, month=month, day=int(day))

        return start_time, end_time
    else:
        raise ValueError(f"Date string did not match the expected format: {ds_date_str}")

def inspect_html_sections(page_source):
    """Inspect the HTML to parse DS and generate an .ics calendar."""
    from bs4 import BeautifulSoup
    from calendar_utils import create_calendar_with_ds
    import pytz
    
    soup = BeautifulSoup(page_source, 'html.parser')
    ds_list = []
    timezone = pytz.timezone('Africa/Casablanca')  # Set to Morocco's time zone

    ds_section = soup.find("section", {"id": "id_73id_42"})  # Adjusted DS section ID
    if ds_section:
        ds_items = ds_section.find_all("li")  # Find all DS items
        for ds_item in ds_items:
            ds_title = ds_item.find("h3").get_text() if ds_item.find("h3") else "No title"
            ds_date = ds_item.find("span", class_="date").get_text() if ds_item.find("span", class_="date") else "No date"
            ds_room = ds_item.find("span", class_=False).get_text() if ds_item.find("span", class_=False) else "No room"

            try:
                # Parse the correct start and end times
                start_time, end_time = parse_date_time(ds_date)
                start_time = timezone.localize(start_time)
                end_time = timezone.localize(end_time)

                ds_list.append({
                    'subject': ds_title,
                    'start_time': start_time,
                    'end_time': end_time,
                    'location': ds_room
                })
            except ValueError as e:
                print(f"Error parsing date: {e}")
    else:
        print("DS Section not found.")
    
    # Create the .ics calendar with all DS exams if any DS were found
    if ds_list:
        create_calendar_with_ds(ds_list)

    return ds_list  # Make sure to return the ds_list

