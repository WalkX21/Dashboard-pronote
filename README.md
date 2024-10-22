# Dashboard-pronote
Wanna do your academic comeback but you're not organized asf, this ai/webscrapping powered app will help get better by getting itself better and better with time (machine learning 😉)

app/
│
├── main.py                 # Main file to run the application
├── auth.py                 # Handles authentication (e.g., login)
├── utils.py                # Utility functions (e.g., human typing, event comparison)
├── dashboard.py 
├── calendar_utils.py       # Calendar creation and manipulation functions
├── html_parsing.py         # HTML parsing and data extraction
└── config.json             # Configuration file for credentials



Things done:
    -- Créer un bot selenium et se loger sur pronote pour récupérer le fichier html ==> auth.py & utils.py
    --parsing the html files to get the datas of ds ==> html_parsing.py
    -- using the parsed data to create a calendar file ==> calendar.ics
    --having a website to see all the datas ==> dashboard.py


things to get done:
    - webscrap evaluation(id_70) and ds (id_69) (both) and store in the same place DONE✅
    - being able to add new ds events, will also be stored in that same place ✅ but new ds stored manually are not shown if app is restarted ==> problem solved succesfully ✅
        ==> sidebar (add new events, scroll) + collonms in dashboard✅
        - champs à remplir:✅
            -type ✅
            - when ?✅
            -title✅
            -where✅
            - + add a date sorting in the dictionnary when added in it (new events should not be added at end but in function of time) ==>done ✅
    
    - how to deploy my application in the web
        - how to scrape using docker ?
        - une 2eme machine
    - homework part handling (scrapping + adding manually)
    - notifications when new homework/ ds
        - notification par mail
        -
    - working on a more dynamic dashboard 
    




    - id of conection, same as id of pronote

