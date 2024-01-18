# WePole README file 

WePole software project for the Lab Of Software Project Development exam. 

# What does WePole Software do? 

Our Software presents some features typical of flights serach engines on the web. The dataset that we used stores data 
from past flights, especially centered around the UK and departing from London Airports. 

From this dataset we used details about Departure and Arrival airports, Airline Companies, Dates, Price and Classes. 

From the web interface you can navigate through some features, like calculating average price for a specific connection, 
get a random destination from a departure place, and getting information about the airline company. 

# Development of the application 

Our web application uses FastApi as the backend and Flask in the frontend. All the development
was carried out using Docker containers. 

The graphics and layout of the webpage was modified through the html files in the frontend of the application. 
We integrated some images regarding the cities on the dataset. A folder names 'static' contains files of the images 
that appear on the website. Then we implemented some css features to design the graphic of the website in order 
for it to be similar to a true flight search engine website. 


*Run the application* 

Our dataset is called 'flights.csv' and is stored in the backend part. It must be present in order for the software to work. 

We got the dataset from the European Data Portal. This is the link:
https://data.europa.eu/data/visualisation/?file=https%3A%2F%2Fwww.gov.uk%2Fgovernment%2Fuploads%2Fsystem%2Fuploads%2Fattachment_data%2Ffile%2F236265%2Fdft-flights-data-2011.csv
The dataset inludes flights from 2011, mostly with departures form England aiports. The main columns are about the price, the departure and arrival destination, travel date, travel class and ari carrier. 


Once master branch is opened, run and debug first backend and then frontend in Docker containers. 

Port localhost:8080 should then be opened on a browser. 

If the application doesn't run on first try, check backend status. If the backend 
shows a problem in the formatting of the csv file, specifically while trying to work on the column that 
present the '£' symbol, try to load the csv again from github again, as it occured to us that it may corrupt. 

In the top bar of the homepage are shown the features that have been developed.

For the feature 'Average Price for Connection' we suggest to select one of Departure Airport 
between the London ones, as the dataset mainly includes flights departing from London. 
Otherwise other connections might not be available. 

# BACKEND 

In the backend/mymodues folder are stored all the modules that we created for developing the features of the app. 
Each feature has a specific module that is connected with the main.py file. 

main.py
Purpose: Frontend module for the Flask application.
Functionality: Manages web requests, template rendering, and integrates other modules.

cleaning.py
Purpose: Data cleaning for flight datasets.
Functionality: Reads and cleans data, focusing on formatting and removing irrelevant information.

df_integrations.py
Purpose: Dataset creation and refinement.
Functionality: Enhances data by creating return tickets, sorting, and deduplication.

feat_1_avg_price.py
Purpose: Average flight price calculation.
Functionality: Computes average flight prices for specific routes.

feat_2_random.py
Purpose: "Surprise me" destination feature.
Functionality: Suggests random travel destinations based on user input.

feat_3_class_price.py
Purpose: Average price calculation for flight classes.
Functionality: Analyzes and calculates average prices for different flight classes.

feat_4_cheapest.py
Purpose: Cheapest flight finder.
Functionality: Identifies the most affordable flights to a given destination.

Tests were tried in the test_main.py stored in the tests folders and coverage is 100%. 


# FRONTEND 

In the frontend part of the project the main.py file is connected with the backend part. 
We used Queryform for all the inputs that are necessary to activate the features in the backend part. 

The graphics and layout of the webpage was modified through the html files in the frontend of the application. 
We integrated some images regarding the cities on the dataset. A folder names 'static' contains files of the images 
that appear on the website. Then we implemented some css features to design the graphic of the website in order 
for it to be similar to a true flight search engine website. 

The 'main.py' file is the central module of a Flask-based web application. 
It is responsible for initializing and configuring the Flask server, defining routes, and managing web interactions.

*HTML File Descriptions*

airlines.html
Purpose: Part of the "Destination Randomizer" feature.
Details: Extends base.html with custom styles and layout.

base.html
Purpose: Base template for the application.
Details: Includes Bootstrap CSS, meta tags, and standard HTML elements.

cheap_result.html
Purpose: Displaying results for cheap flight options.
Details: Extends base.html with a focus on results presentation.

cheapest.html
Purpose: Showcasing cheapest flight options.
Details: Similar to airlines.html, focuses on budget-friendly destinations.

flights1.html
Purpose: Displaying airline price information.
Details: Extends base.html with airline pricing focus.

index.html
Purpose: Homepage of the web application.
Details: Main landing page with custom styles and layout.

my_form.html
Purpose: User input form.
Details: Contains a custom form for data submission or queries.

randomize.html
Purpose: Part of the "Destination Randomizer" feature.
Details: Focuses on displaying random flight destinations.

result_avg.html, results_air-html and result.html
Purpose: Displaying various results.
Details: Generic results pages, possibly for average prices and other data outputs.

# Docstrings 

Docstring documentation in htlm of the modules of the features are created outside the app folder. 

# END

WePole software developed by: 

Lorenzo Campolo 890531
Alessandro Gardenal 891882
Marco Scuccato 891694
Pietro Paloschi 890743