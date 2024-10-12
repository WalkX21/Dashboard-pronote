from icalendar import Calendar, Event
from datetime import datetime
import os
import uuid
import pytz
from utils import events_are_equal

def load_existing_events():
    """Load existing events from the .ics file to avoid duplication."""
    if not os.path.exists("ds_calendar.ics"):
        return []

    with open("ds_calendar.ics", 'rb') as f:
        calendar = Calendar.from_ical(f.read())

    existing_events = []
    for component in calendar.walk():
        if component.name == "VEVENT":
            existing_events.append({
                'subject': str(component.get('summary')),
                'start_time': component.get('dtstart').dt,
                'end_time': component.get('dtend').dt,
                'location': str(component.get('location'))
            })
    return existing_events

def create_calendar_with_ds(ds_list):
    """Create an .ics file with all DS (Devoir Surveillé) exams."""
    existing_events = load_existing_events()
    cal = Calendar()
    modified = False

    for ds in ds_list:
        event = Event()
        subject = ds['subject']
        start_time = ds['start_time']
        end_time = ds['end_time']
        location = ds['location']
        new_event = {'subject': subject, 'start_time': start_time, 'end_time': end_time, 'location': location}

        if not any(events_are_equal(existing_event, new_event) for existing_event in existing_events):
            event.add('summary', subject)
            event.add('dtstart', start_time)
            event.add('dtend', end_time)
            event.add('location', location)
            event.add('uid', str(uuid.uuid4()) + "@pronote_ds")
            event.add('dtstamp', datetime.now())
            cal.add_component(event)
            modified = True

    if modified:
        with open("ds_calendar.ics", 'wb') as f:
            f.write(cal.to_ical())
        print("DS Calendar saved as 'ds_calendar.ics'.")
    else:
        print("No changes detected. DS Calendar is up to date.")

def open_ics_with_calendar():
    """Open the .ics file automatically with Apple Calendar."""
    ics_file_path = os.path.abspath("ds_calendar.ics")
    os.system(f'osascript -e \'tell application "Calendar" to open POSIX file "{ics_file_path}"\'')
