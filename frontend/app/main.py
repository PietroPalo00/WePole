"""
Frontend module for the Flask application.

This module defines a simple Flask application
that serves as the frontend for the project.
"""


import json
from flask import Flask, render_template, redirect, url_for, request
import requests  # Import the requests library to make HTTP requests
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField

app = Flask(__name__)

# Replace with a secure secret key
app.config['SECRET_KEY'] = 'your_secret_key'

# Configuration for the FastAPI backend URL
# Replace with the actual URL of your FastAPI backend
FASTAPI_BACKEND_HOST = 'http://backend:80'


class QueryForm(FlaskForm):
    """
    Form for querying flight information.

    Attributes:
        - Departure (SelectField): Selection field for the departure city.
        - Arrival (SelectField): Selection field for the arrival city.
        - submit (SubmitField): Button to get the overall result.
        - departure (SelectField): Additional selection field for the departure
        city (optional).
        - submit1 (SubmitField): Button to get information about possible
        destinations.
        - airline (SelectField): Selection field for airlines (optional).
        - submit2 (SubmitField): Button to get information about airlines.
        - submit3 (SubmitField): Button to display the final result.
    """
    Departure = SelectField('Departure: ')
    Arrival = SelectField('Arrival: ')
    submit = SubmitField('Result: ')
    departure = SelectField('Departure:')
    submit1 = SubmitField('Where can i go?')
    airline = SelectField('Airlines:')
    submit2 = SubmitField('Get airlines')
    submit3 = SubmitField('Show Result')


@app.route('/')
def index():
    """
    Route handler for the home page.

    Returns:
        flask.Response: The rendered HTML template for the home page.
    """
    return render_template('index.html')


@app.route('/airlines_comparator', methods=['GET', 'POST'])
def airlines():
    """
    Route handler for the class comparator tool.

    Methods:
        - GET: Renders the airlines comparator page with a form for
        selecting airlines.
        - POST: Processes the form submission, retrieves data from
        the FastAPI backend,
        and renders the result on the page.

    Returns:
        flask.Response: The rendered HTML template for the airlines
        comparator page.
    """
    form = QueryForm()
    response = requests.get(f'{FASTAPI_BACKEND_HOST}/get_airline', timeout=5)
    air = json.loads(response.json())
    air = sorted(air)
    form.airline.choices = air
    backend_url = f'{FASTAPI_BACKEND_HOST}/{air}'
    if form.validate_on_submit():
        air = form.airline.data
        response = requests.get(f'{backend_url}/{air}', timeout=5)
        data = response.json()
        return render_template('airlines.html', form=form, result=data)
    return render_template('airlines.html', form=form, result='None')


@app.route('/result-air', methods=['GET', 'POST'])
def show_results():
    """
    Route handler for displaying results related to the class comparator tool.

    Methods:
        - GET: Redirects to the 'airlines' route.
        - POST: Processes the form submission, retrieves data from
        the FastAPI backend,
        and renders the result on the 'results_air.html' template.

    Returns:
        flask.Response: The rendered HTML template for displaying
        airline-related results.
    """
    backend_url = f'{FASTAPI_BACKEND_HOST}'
    if request.method == 'POST':
        air = request.form['airline']
        try:
            response = requests.get(f'{backend_url}/airlines-{air}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data:  # Check if there is a result
                    return render_template('results_air.html', airline=air, result=data)
                return render_template('results_air.html', airline=air, message="No result")
            status = response.status_code
            message = f"App not responding, response status = {status}"
            return render_template('results_air.html', message=message)
        except requests.exceptions.ConnectionError as e:
            return render_template('results_air.html', message=f"Connection error: {str(e)}")
    return redirect(url_for('airlines'))


@app.route('/calculate_average_price', methods=['GET', 'POST'])
def calculate_average_price():
    """
    Route handler for calculating the average flight price between selected airports.

    Methods:
        - GET: Retrieves the list of available airports from the
        FastAPI backend and renders
        the 'flights1.html' template with a form for selecting
        departure and arrival airports.
        - POST: Processes the form submission, retrieves data
        from the FastAPI backend,
        and renders the result on the 'flights1.html' template.

    Returns:
        flask.Response: The rendered HTML template for displaying
        average flight prices.
    """
    form = QueryForm()
    response = requests.get(f'{FASTAPI_BACKEND_HOST}/get_departure', timeout=5)
    airports = json.loads(response.json())
    airports = [airport for airport in airports if airport is not None]
    airports = sorted(airports)
    form.Departure.choices = airports
    form.Arrival.choices = airports
    departure = airports
    arrival = airports
    backend_url = f'{FASTAPI_BACKEND_HOST}/avg/{departure}/{arrival}'
    if form.validate_on_submit():
        departure = form.Departure.data
        arrival = form.Arrival.data
        response = requests.get(f'{backend_url}/{departure}/{arrival}', timeout=5)
        data = response.json()
        return render_template('flights1.html', form=form, result=data)
    return render_template('flights1.html', form=form, data='None')


@app.route('/results-flights', methods=['GET', 'POST'])
def resultshow():
    """
    Route handler for displaying results related to average
    flight prices.

    Methods:
        - GET: Redirects to the 'calculate_average_price' route.
        - POST: Processes the form submission, retrieves data
        from the FastAPI backend,
        and renders the result on the 'result_avg.html' template.

    Returns:
        flask.Response: The rendered HTML template for displaying
        average flight price results.
    """
    backend_url = f'{FASTAPI_BACKEND_HOST}'
    if request.method == 'POST':
        departure = request.form['Departure']
        arrival = request.form['Arrival']
        try:
            response = requests.get(f'{backend_url}/avg/{departure}/{arrival}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return render_template('result_avg.html', result=data, departure=departure, arrival=arrival)
                message = f"Unfortunately there isn't a flight connection between {departure} and {arrival}"
                return render_template('result_avg.html', message=message)
            message = message = f'There is not a connection between {departure} and {arrival}'
            return render_template('result_avg.html', message=message)
        except requests.exceptions.ConnectionError as e:
            return render_template('result_avg.html', message=f'Connection error: {str(e)}')
    return redirect(url_for('calculate_average_price'))


@app.route('/randomize', methods=['GET', 'POST'])
def randomize():
    """
    Route handler for randomizing flight information based on selected departure.
    It is used for the Surprise me tool.

    Methods:
        - GET: Retrieves the list of available departure airports
        from the FastAPI backend and
        renders the 'randomize.html' template with a form for
        selecting a departure airport.
        - POST: Processes the form submission, retrieves random
        flight data from the FastAPI backend,
        and renders the result on the 'randomize.html' template.

    Returns:
        flask.Response: The rendered HTML template for displaying
        randomized flight information.
    """
    form = QueryForm()
    response = requests.get(f'{FASTAPI_BACKEND_HOST}/get_departure', timeout=5)
    departures = json.loads(response.json())
    departures = [departure for departure in departures if departure is not None]
    departures = sorted(departures)
    form.departure.choices = departures
    backend_url = f'{FASTAPI_BACKEND_HOST}/random'
    if form.validate_on_submit():
        departure = form.departure.data
        response = requests.get(f'{backend_url}/{departure}', timeout=5)
        data = response.json()
        return render_template('randomize.html', form=form, result=data)
    return render_template('randomize.html', form=form, result='None')


@app.route('/result', methods=['GET', 'POST'])
def show_result():
    """
    Route handler for displaying results related to randomized
    flight information.

    Methods:
        - GET: Redirects to the 'randomize' route.
        - POST: Processes the form submission, retrieves data
        from the FastAPI backend,
        and renders the result on the 'result.html' template.

    Returns:
        flask.Response: The rendered HTML template for displaying
        randomized flight information results.
    """
    backend_url = f'{FASTAPI_BACKEND_HOST}/random'
    if request.method == 'POST':
        departure = request.form['departure']
        try:
            # Chiamata per ottenere i dati di destinazione
            response = requests.get(f'{backend_url}/{departure}', timeout=5)
            # Chiamata per ottenere il nome dell'immagine
            if response.status_code == 200:
                data = response.json()
                give_output = ', '.join(data['give_output']) if 'give_output' in data else None
                arrivalcity_output = data['arrivalcity'] if 'arrivalcity' in data else None

                if give_output:
                    return render_template('result.html', departure=departure, result=give_output, image=arrivalcity_output)
                return render_template('result.html', departure=departure, message="No result")
            status = response.status_code
            return render_template('result.html', message="App not responding, response status = "f'{status}')
        except requests.exceptions.ConnectionError as e:
            return render_template('result.html', message=f"Connection error: {str(e)}")
    return redirect(url_for('randomize'))


@app.route('/cheapest', methods=['GET', 'POST'])
def cheapest():
    """
    Route handler for finding the cheapest company to fly with
    to a selected destination.

    Methods:
        - GET: Retrieves the list of available departure airports
        from the FastAPI backend
        and renders the 'cheapest.html' template with a form for
        selecting the arrival airport.
        - POST: Processes the form submission, retrieves data from
        the FastAPI backend,
        and renders the result on the 'cheapest.html' template.

    Returns:
        flask.Response: The rendered HTML template for displaying
        information about the cheapest flights.
    """
    form = QueryForm()
    response = requests.get(f'{FASTAPI_BACKEND_HOST}/get_departure', timeout=5)
    airports = json.loads(response.json())
    airports = [airport for airport in airports if airport is not None]
    airports = sorted(airports)
    form.Arrival.choices = airports
    backend_url = f'{FASTAPI_BACKEND_HOST}'
    if form.validate_on_submit():
        arrivals = form.Arrival.data
        response = requests.get(f'{backend_url}/{arrivals}', timeout=5)
        data = response.json()
        return render_template('cheapest.html', form=form, result=data)
    return render_template('cheapest.html', form=form, result='None')


@app.route('/cheap_result', methods=['GET', 'POST'])
def cheap_result():
    """
    Route handler for displaying results related to the cheapest flights to a selected destination.

    Methods:
        - GET: Redirects to the 'cheapest' route.
        - POST: Processes the form submission, retrieves data from the FastAPI backend,
        and renders the result on the 'cheap_result.html' template.

    Returns:
        flask.Response: The rendered HTML template for displaying information about the cheapest flights result.
    """
    backend_url = f'{FASTAPI_BACKEND_HOST}'
    if request.method == 'POST':
        arrivals = request.form['Arrival']
        try:
            response = requests.get(f'{backend_url}/arrival-{arrivals}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data:  # Check if there is a result
                    return render_template('cheap_result.html', arrival=arrivals, result=data, image=arrivals)
                return render_template('cheap_result.html', arrival=arrivals, message="No result")
            status = response.status_code
            message = "App not responding, response status = "f'{status}'
            return render_template('cheap_result.html', message=message)
        except requests.exceptions.ConnectionError as e:
            return render_template('cheap_result.html', message=f"Connection error: {str(e)}")
    return redirect(url_for('cheapest'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
