# Dashboard-pronote

Do you want to improve your academic organization but struggle to keep everything in order? This AI-powered, web-scraping app aims to help you get organized by automating the process of collecting, displaying, and managing your school tasks. As time goes on, the app will keep getting better, thanks to machine learning! 😉

## Application Overview

This app scrapes data from Pronote (your school management system) to help you manage DS (tests), evaluations, and homework assignments. It also provides a dashboard to help you track and organize your tasks in a user-friendly way.

### Folder Structure

```bash
app/
│
├── main.py                 # Main file to run the application
├── auth.py                 # Handles authentication (e.g., login to Pronote)
├── utils.py                # Utility functions (e.g., human typing simulation, event comparison)
├── dashboard.py            # Dashboard rendering logic
├── homework_scraping.py     # Homework scraping logic
├── html_parsing.py          # HTML parsing and data extraction from Pronote
└── config.json             # Configuration file for credentials

Features Completed
1. Pronote Authentication & Web Scraping

Selenium Bot: Created a Selenium bot to log into Pronote, retrieve the necessary HTML for authentication, and scrape data.
Files: auth.py, utils.py
Status: ✅ Completed

HTML Parsing: Successfully parsed the HTML files to extract DS (tests) and evaluation data.
File: html_parsing.py
Status: ✅ Completed

2. Dashboard for Displaying Data

Web Interface: A basic web dashboard is set up to display all the DS and evaluation data retrieved from Pronote.
File: dashboard.py
Status: ✅ Completed

3. Manual Event Input & Sorting

Add New Events: Users can manually add new DS events (type, date, title, location) through the dashboard, and these are automatically sorted based on time, not just added at the end.
Features: Sidebar navigation, input fields for DS events (type, date, title, location), automatic sorting
Status: ✅ Completed

4. Homework Management

Homework Scraping: Successfully scraped homework data from Pronote and stored it in a JSON file.
File: homework_scraping.py
Status: ✅ Completed

Manual Homework Entry: Users can also manually add new homework assignments, which will be displayed alongside the scraped data.
Status: ✅ Completed

5. Notifications (In Progress)

Discord Notifications: The goal is to notify users on Discord when new DS, homework, or evaluation results are available, either via a private message or in a Discord server.
Status: 🔄 In Progress

Features in Progress

1. Scraping Additional Data

Evaluations & DS: Extend the scraping functionality to capture both evaluation (id_70) and DS (id_69) data and store them in a unified structure.
Status: ✅ Completed

2. Dashboard Enhancements

Dynamic Dashboard: Improve the UI/UX by making the dashboard more dynamic, responsive, and user-friendly. This includes adding a main page that only shows the next upcoming DS and homework in a clean, concise format, with options to view more details.
Status: 🔄 In Progress

3. Homework Notifications

Email Notifications: Implement email notifications to alert users when new homework or DS is added or when a new mark is received.
Status: 🔄 Planned

Upcoming Features & To-Do

1. Further Deployment Considerations

Docker Integration: Explore deploying the application using Docker, potentially running on a second machine.

Automated Scraping: Look into scheduling the web scraping process, either through a programmatic launch or using GitHub Codespaces.

2. User Account & Login Management

Register & Login Pages: Set up account creation and login functionality, allowing users to manage their dashboards. Upon first login, users will input their Pronote credentials.
Pronote ID will serve as the login ID.
Humor Tracker: Upon login, the app will ask users to rate their mood (via sliders or emojis). This feature will help train the AI to give better productivity recommendations over time.
Status: 🔄 Planned

Ideas for Future Improvements:

1. Enhanced User Interface (UI)
Main Page (Accueil): Create a main page that shows the most relevant tasks (e.g., next DS and homework). This page will be minimalistic but include shortcuts for adding new events.
Multipage Navigation: Allow users to navigate between different pages (e.g., DS page, Homework page) using a sidebar.
DS Page: Display detailed information about upcoming DS and evaluations. Users can also manually add DS here.
Homework Page: Similar to the DS page, but focused on homework assignments.

2. Basic Analytics
Stats on Dashboard: Show simple, non-AI-powered statistics, such as the number of homework assignments due each week or the time taken for past assignments.
Database Restructuring: This feature will require reorganizing how data is stored.

3. AI-Powered Features (Planned)
Time Estimation & Task Management: Use machine learning to analyze your past performance and estimate how long it will take to complete upcoming tasks (DS, homework, evaluations).
AI will suggest an order for completing tasks based on time estimates and deadlines.
Work Session Tracking: Let users log time spent on DS/homework. Over time, the AI will refine its time estimates based on actual completion times.
The AI will incorporate humor-based analysis to make these estimates more personalized (e.g., humor might affect how much time the AI thinks you'll need).
Goals of the Application

This app aims to help students stay organized and improve their productivity by offering:

Automated Data Gathering: Web scraping for DS, evaluations, and homework assignments.

Manual Task Entry: Allowing users to manually input and manage their academic tasks.

Multipage Dashboard: A clean, organized interface that lets users navigate through different sections like DS, homework, and stats.

AI-Powered Insights: Personalized recommendations and time estimates to help users prioritize and plan their tasks.
