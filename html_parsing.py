from datetime import datetime
from bs4 import BeautifulSoup
from utils import save_data, load_data, make_timezone_aware
from datetime import datetime
import pytz
import re


def parse_date_time(ds_date_str):
    """Parse the date and time from strings like 'Le jeudi 7 nov. de 11h00 à 12h00'."""
    pattern = r"Le (\w+) (\d+) (\w+)\.? de (\d+h\d+) à (\d+h\d+)"
    match = re.search(pattern, ds_date_str)

    if match:
        day_name, day, month_name, start_time_str, end_time_str = match.groups()

        # Corrected month map for French abbreviations
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
    """Inspect the HTML to parse DS and Evaluations."""
    soup = BeautifulSoup(page_source, 'html.parser')
    ds_list = []
    timezone = pytz.timezone('Africa/Casablanca')  # Set to Morocco's time zone

    # Parse DS Section (id_73 for Devoirs sur table)
    ds_section = soup.find("div", {"id": "id_235"})
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
    # eval_section = soup.find("div", {"id": "id_74"})
    eval_section = soup.find("div", {"id": "id_236"})
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

    return ds_list

DS_EVAL_FILE = "ds_evals.json"

def scrape_ds_evals(page_source):
    """Scrape DS and Evaluations from Pronote HTML."""
    soup = BeautifulSoup(page_source, 'html.parser')
    ds_evals_list = []

    # Locate the DS section and Evaluation section in the HTML (adjust IDs if necessary)
    ds_section = soup.find("section", {"id": "id_235"})  # Adjust the ID if needed for DS
    if ds_section:
        ds_items = ds_section.find_all("li")
        for ds_item in ds_items:
            subject = ds_item.find("h3").get_text(strip=True)
            date_str = ds_item.find("span", class_="date").get_text(strip=True)
            room = ds_item.find("span", class_=False).get_text(strip=True)
            
            # Assume parse_date_time function parses date/time info from the string
            start_time, end_time = parse_date_time(date_str)
            start_time = make_timezone_aware(start_time)
            end_time = make_timezone_aware(end_time)

            ds_evals_list.append({
                'subject': subject,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'location': room,
                'type': 'DS'  # Label as DS
            })

    # Do the same for Evaluations if they have a separate section
    eval_section = soup.find("section", {"id": "id_236"})  # Adjust the ID if needed for Evaluations
    if eval_section:
        eval_items = eval_section.find_all("li")
        for eval_item in eval_items:
            subject = eval_item.find("h3").get_text(strip=True)
            date_str = eval_item.find("span", class_="date").get_text(strip=True)
            room = eval_item.find("span", class_=False).get_text(strip=True)

            start_time, end_time = parse_date_time(date_str)
            start_time = make_timezone_aware(start_time)
            end_time = make_timezone_aware(end_time)

            ds_evals_list.append({
                'subject': subject,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'location': room,
                'type': 'Evaluation'  # Label as Evaluation
            })

    return ds_evals_list

# def fetch_and_save_ds_evals(page_source):
#     """Fetch DS and Evaluations and save to ds_evals.json."""
#     ds_evals_list = scrape_ds_evals(page_source)

#     # Load existing data to avoid overwriting
#     current_ds_evals = load_data(DS_EVAL_FILE)

#     # Add new DS/Evaluations entries, avoid duplicates
#     for ds in ds_evals_list:
#         if ds not in current_ds_evals:
#             current_ds_evals.append(ds)

#     # Save updated DS/Evaluations data
#     save_data(DS_EVAL_FILE, current_ds_evals)


def fetch_and_save_ds_evals(page_source):
    """Fetch DS and Evaluations and save to ds_evals.json."""
    
    # Check if page_source is valid
    if page_source is None:
        print("Error: No page source received for DS/Evaluations parsing.")
        return  # Stop further processing if page source is invalid

    try:
        # Attempt to parse DS/Evaluations
        ds_evals_list = scrape_ds_evals(page_source)
    except Exception as e:
        print(f"An error occurred while parsing DS/Evaluations: {e}")
        return

    # Load existing data to avoid overwriting
    current_ds_evals = load_data(DS_EVAL_FILE)

    # Add new DS/Evaluations entries, avoiding duplicates
    for ds in ds_evals_list:
        if ds not in current_ds_evals:
            current_ds_evals.append(ds)

    # Save updated DS/Evaluations data
    save_data(DS_EVAL_FILE, current_ds_evals)
