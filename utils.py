import time
import random
import json
import os
from datetime import datetime
import pytz

def human_typing(element, text):
    """Simulate human typing with random delays between keystrokes."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

def events_are_equal(event1, event2):
    """Check if two events are equal."""
    return (event1['subject'] == event2['subject'] and
            event1['start_time'] == event2['start_time'] and
            event1['end_time'] == event2['end_time'] and
            event1['location'] == event2['location'])

def save_data(filename, data):
    """Save data to a JSON file."""
    try:
        with open(filename, "w") as file:
            json.dump(data, file, default=str)
        print(f"Data successfully saved to {filename}.")
    except Exception as e:
        print(f"Error saving data to {filename}: {str(e)}")

def load_data(filename):
    """Load data from a JSON file."""
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading data from {filename}: {str(e)}")
    return []

def make_timezone_aware(dt, timezone='Africa/Casablanca'):
    """Convert a naive datetime object to a timezone-aware one."""
    tz = pytz.timezone(timezone)
    if dt.tzinfo is None:
        return tz.localize(dt)
    return dt

def parse_datetime_string(date_str):
    """Parse a string date (isoformat) to a datetime object."""
    try:
        return datetime.fromisoformat(date_str)
    except ValueError as e:
        print(f"Error parsing date string: {e}")
        return None


import json

def load_json(filename):
    """Load data from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_json(filename, data):
    """Save data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)