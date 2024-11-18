import requests

# Start a session to maintain cookies
session = requests.Session()

# Step 1: Get the login page to initiate cookies
login_page_url = 'https://3500044w.index-education.net/pronote/eleve.html'
login_page_response = session.get(login_page_url)
print("Login page accessed.")

# Step 2: Perform login with appropriate credentials (replace 'username' and 'password')
login_payload = {
    'username': 'your_username',
    'password': 'your_password',
    # Include any additional fields required by Pronote's login form
}
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': login_page_url,
}
login_response = session.post(login_page_url, data=login_payload, headers=headers)

# Step 3: Check for an XHR (AJAX) request that initializes session data
# If you identified an endpoint from the Network tab (e.g., '/auth' or '/initialize'):
session_init_url = 'https://3500044w.index-education.net/pronote/appelfonction/3/initialize'  # example URL
session_init_payload = {
    # Include any payload you captured from the Network tab in Developer Tools
}

# Make the session initialization request
session_init_response = session.post(session_init_url, headers=headers, json=session_init_payload)

if session_init_response.ok:
    print("Session initialized:", session_init_response.json())
    # Check if this response contains the session-specific URL or other session data
    dynamic_url = session_init_response.json().get("sessionUrl")  # Example extraction
    print("Dynamic URL obtained:", dynamic_url)
else:
    print("Failed to initialize session.")
