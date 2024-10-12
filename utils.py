import time
import random

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
