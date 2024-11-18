# Dashboard-pronote
Wanna do your academic comeback but you're not organized asf, this ai/webscrapping powered app will help get better by getting itself better and better with time (machine learning 😉)

app/
│
├── main.py                 # Main file to run the application
├── auth.py                 # Handles authentication (e.g., login)
├── utils.py                # Utility functions (e.g., human typing, event comparison)
├── dashboard.py 
├──homework_scraping.py
├── html_parsing.py         # HTML parsing and data extraction
└── config.json             # Configuration file for credentials



Things done:
    -- Créer un bot selenium et se loger sur pronote pour récupérer le fichier html ==> auth.py & utils.py✅
    --parsing the html files to get the datas of ds ==> html_parsing.py✅
    --having a website to see all the datas ==> dashboard.py✅


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
        - une 2eme machine ?
        -lancement programmé et/ou codespace ? 

    NOTIFICATION ON DISCORD, best in a server or en privé ==> to get the developper badge


    - homework part handling (scrapping + adding manually)✅
        - analyse class id of the homework in pronote✅
        - scrapping and handling that data to get a json maybe file with all the homework✅
        - same thing as for the ds, user must be able to add a homework manually.✅
        -puting all things in different collomn ✅

    WORK ON UI/UX 

    - notifications when new homework/ ds, when new mark (this may be cool if fast)
        - notification par mail
        -
    - working on a more dynamic dashboard 
    

    Ideas:
        -working on UI: work on getting a main page that shows the main ds and homework ect for the next days, for the others ds ect (some ds are written in pronote for in a lot of time) ==> work on a multipage app (see streamlit documentation)
            -page accueil with only the main shits, should not be that long, should be clear, small shortcut for adding manual ds or homework ==> button leads to a page to add things==> helps free up space in accueil page
            -ds page: shows the details of the nexts ds and evaluations, (maybe when showing things for a bit in acceuil show only the title and a button see more infos ==> leading to the ds page), shows infos, place to add ds if we want to
            -homework page: as the ds page, shows more infos about the homeworks ect + being able to add (same thinking as in ds)



Objectif of the app:
    -helping me getting more organized, having my own students dashboard that helps me get organized and tells me what to do with ai analysis:
        -WEB SCRAPPING of the ds, evaluation, homework
        -Display or the ds and evaluations
        -Being able to add manual ds or evaluation
        -Display the homeworks
        -Being able to add manual homework
        -Having a multipage app with: navigate through sidebar
            -an accueil page with the main next ds and homework in two collomns, being able to click a button 'see more' or 'get more infos' to see the details of the homework and ds/evaluation
            -Ds page for displaying details of the ds and evaluations + being able to add manual entries there
            -Homework page with the main homework ect + manual add ect
            -when you went to add a ds (add ds page) or a homework (add homework page) ==> open a page, kind of pop up, to add the things; Those pages are not shown in the sidebar
            -Basic Stat Analysis in the acceuil with non-ai-powered charts (just datas like number of homework per week ect) ==> needs to restructure the database or the way data is stored 💀
        -Ai part handling: 
            -time to get things done estimation from level analysis from marks and past homework (all the main analysis are going to be maid not each lauching time but just the first time (like a 'we're setting up your workspace))
            -lauching a work session (being able to check ds/evaluation revised and homework done, with setting the time it took you for each time) ==> machine learning, time estimation modification from what the ai learns
            -if enough information for the ia, order of things to get done, proposed by the ai
            -humor handling in time estimation
            ...
        -Account and connection handling:
            -register page + detect that it's your first time here to set up all the things, setting up the pronote ids here, if you have a doubt, maybe a button (i'm not sure if my pronote ids are good), that summon a bot to check things by trying to connect.
            -login page
                -when you connect, humor tracker as every new connection asking to check your humor with maybe 2/3 quesions with sliders or just emojies

    - id of conection, same as id of pronote when registering
        -think about ways to register/login
        -do not ask for humor without being registered/loged in


// si case 'deja fait' est coché, il n'ya plus d'objct à srape, aranger le code pr que si le travail a été coché sur pronote
les choses soit répercuté sur le dashboard (maybe work on l'inverse (à voir si je fais pas un bot qui va apuyer sur le bouton or idk))

