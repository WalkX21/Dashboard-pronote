from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from calendar_utils import create_calendar_with_ds
import pytz
import re

def parse_date_time(ds_date_str):
    """Parse the date and time from strings like 'Le jeudi 7 nov. de 11h00 à 12h00'."""
    pattern = r"Le (\w+) (\d+) (\w+)\.? de (\d+h\d+) à (\d+h\d+)"
    match = re.search(pattern, ds_date_str)

    if match:
        day_name, day, month_name, start_time_str, end_time_str = match.groups()

        # Corrected month map to handle both "nov." and "nov"
        month_map = {
            'janv.': 1, 'févr.': 2, 'mars.': 3, 'avr.': 4,
            'mai.': 5, 'juin.': 6, 'juil.': 7, 'août.': 8,
            'sept.': 9, 'oct.': 10, 'nov.': 11, 'déc.': 12,
            'janv': 1, 'févr': 2, 'mars': 3, 'avr': 4,
            'mai': 5, 'juin': 6, 'juil': 7, 'août': 8,
            'sept': 9, 'oct': 10, 'nov': 11, 'déc': 12
        }
        month = month_map.get(month_name.lower(), None)

        if month is None:
            raise ValueError(f"Unknown month name: {month_name}")

        year = datetime.now().year  # Use current year dynamically

        # Convert time strings into datetime objects
        start_time = datetime.strptime(start_time_str, "%Hh%M").replace(year=year, month=month, day=int(day))
        end_time = datetime.strptime(end_time_str, "%Hh%M").replace(year=year, month=month, day=int(day))

        return start_time, end_time
    else:
        raise ValueError(f"Date string did not match the expected format: {ds_date_str}")

def inspect_html_sections(page_source):
    """Inspect the HTML to parse DS and Evaluations and generate an .ics calendar."""
    soup = BeautifulSoup(page_source, 'html.parser')
    ds_list = []
    timezone = pytz.timezone('Africa/Casablanca')  # Set to Morocco's time zone

    # Parse DS Section (id_73 for Devoirs sur table)
    ds_section = soup.find("div", {"id": "id_73"})
    if ds_section:
        ds_items = ds_section.find_all("li")
        for ds_item in ds_items:
            ds_title = ds_item.find("h3").get_text() if ds_item.find("h3") else "No title"
            ds_date = ds_item.find("span", class_="date").get_text() if ds_item.find("span", class_="date") else "No date"
            ds_room = ds_item.find_all("span")[1].get_text() if len(ds_item.find_all("span")) > 1 else "No room"

            start_time, end_time = parse_date_time(ds_date)
            start_time = timezone.localize(start_time)
            end_time = timezone.localize(end_time)

            # Add DS to list
            ds_list.append({
                'subject': ds_title,
                'start_time': start_time,
                'end_time': end_time,
                'location': ds_room,
                'type': 'DS'  # Label as DS
            })

    # Parse Evaluation de Compétence Section (id_74)
    eval_section = soup.find("div", {"id": "id_74"})
    if eval_section:
        eval_items = eval_section.find_all("li")
        for eval_item in eval_items:
            eval_title = eval_item.find("h3").get_text() if eval_item.find("h3") else "No title"
            eval_date = eval_item.find("span", class_="date").get_text() if eval_item.find("span", class_="date") else "No date"
            eval_room = eval_item.find_all("span")[1].get_text() if len(eval_item.find_all("span")) > 1 else "No room"

            start_time, end_time = parse_date_time(eval_date)
            start_time = timezone.localize(start_time)
            end_time = timezone.localize(end_time)

            # Add Evaluation to list
            ds_list.append({
                'subject': eval_title,
                'start_time': start_time,
                'end_time': end_time,
                'location': eval_room,
                'type': 'Evaluation'  # Label as Evaluation
            })

    # Create the .ics calendar with all exams (DS + Evaluations)
    if ds_list:
        create_calendar_with_ds(ds_list)

    return ds_list
