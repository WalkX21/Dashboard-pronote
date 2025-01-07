<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard-Pronote</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }
        .announcement {
            background-color: #ffcccc;
            border: 1px solid #ff0000;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 5px;
            color: #660000;
            font-weight: bold;
        }
        .section {
            margin-bottom: 2rem;
        }
        h1, h2, h3 {
            color: #333333;
        }
        ul {
            margin: 0;
            padding-left: 1.5rem;
        }
        ul li {
            margin-bottom: 0.5rem;
        }
        .checklist li::before {
            content: "✅ ";
            color: green;
        }
        .in-progress li::before {
            content: "🟡 ";
            color: orange;
        }
        .ideas li::before {
            content: "💡 ";
            color: blue;
        }
        .code-block {
            background-color: #f4f4f4;
            border: 1px solid #ddd;
            padding: 1rem;
            border-radius: 5px;
            font-family: monospace;
            overflow-x: auto;
        }
    </style>
</head>
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
    <h3>📂 Completed Tasks</h3>
    <ul class="checklist">
        <li>Selenium bot for Pronote login and HTML scraping (auth.py & utils.py).</li>
        <li>Parsing HTML for exam (DS) data (html_parsing.py).</li>
        <li>Website for viewing scraped data (dashboard.py).</li>
        <li>Scraping and storing evaluations (ID_70) and exams (ID_69).</li>
        <li>Adding manual events to the dashboard and sorting by date.</li>
        <li>Homework scraping and manual additions.</li>
        <li>Improved dashboard layout: Separate columns for DS and homework.</li>
    </ul>

    <h3>🚧 Work in Progress</h3>
    <ul class="in-progress">
        <li>Deployment: Investigate Docker or multi-machine setup for deployment.</li>
        <li>Notifications: Set up alerts for new homework, DS, or grades (email or Discord).</li>
        <li>Dynamic Dashboard: Enhance UX/UI for a smoother user experience.</li>
    </ul>

    <h3>💡 Ideas</h3>
    <ul class="ideas">
        <li>Multipage app with dedicated sections for DS and Homework.</li>
        <li>AI-based insights: Predict time required for tasks based on past performance.</li>
        <li>Suggest task priorities and schedules based on AI analysis.</li>
    </ul>
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

    <h3>🔧 Enhancements</h3>
    <ul class="in-progress">
        <li>AI time estimation for tasks.</li>
        <li>Dynamic dashboard with charts and navigation.</li>
        <li>User-friendly UI/UX improvements.</li>
        <li>Notifications for updates (email/Discord).</li>
    </ul>

    <h3>🌐 Deployment</h3>
    <ul class="in-progress">
        <li>Research Docker/Multi-machine deployment.</li>
        <li>Explore scheduled launches or Codespace integration.</li>
    </ul>
</div>

</body>
</html>
