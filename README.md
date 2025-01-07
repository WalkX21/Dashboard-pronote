<!DOCTYPE html>
<html lang="en">

<body>

<div class="announcement">
    🚨 <strong>Important Announcement:</strong><br>
    This project has been discontinued due to the emergence of similar applications like <i>Papillon</i>. 
    While <i>Papillon</i> lacks AI capabilities, it fulfills the core functionalities I envisioned for this app.
    Additionally, the frequent updates required made it unviable to maintain. Thank you for your support and interest!
</div>

<div class="section">
    <h1>📘 Dashboard-Pronote</h1>
    <p>Are you struggling to stay organized with your academic tasks? This <strong>AI/Webscraping powered app</strong> aims to simplify your life by organizing your schedule and improving over time through <strong>machine learning</strong>!</p>
</div>

<div class="section">
    <h2>🔩 Project Structure</h2>
    <div class="code-block">
<pre>app/
├── main.py                # Main file to run the application
├── auth.py                # Handles authentication (e.g., login)
├── utils.py               # Utility functions (e.g., human typing, event comparison)
├── dashboard.py           # Dashboard rendering logic
├── homework_scraping.py   # Homework scraping functionality
├── html_parsing.py        # HTML parsing and data extraction
└── config.json            # Configuration file for credentials</pre>
    </div>
</div>

<div class="section">
    <h2>✅ Features & Progress</h2>
    
#### 📂 Completed Tasks
- Selenium bot for Pronote login and HTML scraping (auth.py & utils.py).
- Parsing HTML for exam (DS) data (html_parsing.py).
- Website for viewing scraped data (dashboard.py).
- Scraping and storing evaluations (ID_70) and exams (ID_69).
- Adding manual events to the dashboard and sorting by date.
- Homework scraping and manual additions.
- Improved dashboard layout: Separate columns for DS and homework.

#### 🚧 Work in Progress
- Deployment: Investigate Docker or multi-machine setup for deployment.
- Notifications: Set up alerts for new homework, DS, or grades (email or Discord).
- Dynamic Dashboard: Enhance UX/UI for a smoother user experience.

#### 💡 Ideas
- Multipage app with dedicated sections for DS and Homework.
- AI-based insights: Predict time required for tasks based on past performance.
- Suggest task priorities and schedules based on AI analysis.
</div>

<div class="section">
    <h2>🎯 Objectives</h2>
    <p>This app is designed to <strong>help students</strong> stay organized with a personalized dashboard for:</p>
    <ul>
        <li>Scraping academic data (DS, evaluations, homework).</li>
        <li>Displaying these in a clean, dynamic interface.</li>
        <li>Allowing manual additions for custom events.</li>
        <li>AI-driven analysis for time estimation and task prioritization.</li>
        <li>Notifications via <strong>email/Discord</strong> for updates.</li>
    </ul>
</div>

<div class="section">
    <h2>📝 Checklist View</h2>
    <h3>🟢 Core Features</h3>
    <ul class="checklist">
        <li>Pronote Login (Selenium Bot).</li>
        <li>Scrape DS/evaluation data.</li>
        <li>Scrape homework data.</li>
        <li>Manual addition support for DS/homework.</li>
    </ul>

#### 🔧 Enhancements
- AI time estimation for tasks.
- Dynamic dashboard with charts and navigation.
- User-friendly UI/UX improvements.
- Notifications for updates (email/Discord).

#### 🌐 Deployment
- Research Docker/Multi-machine deployment.
- Explore scheduled launches or Codespace integration.
</div>

</body>
</html>
