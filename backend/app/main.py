

from fastapi import FastAPI
import sys

sys.path.append('app')
from mymodules.Cleaning import df_clean
from mymodules.df_integrations import flights
from mymodules.feat_1_avg_price import calculate_average_price
from mymodules.feat_3_class_price import calculate_average_price_airline
from mymodules.feat_2_random import randomize_destination
from mymodules.feat_4_cheapest import cheapest_to_fly
from mymodules.Cleaning import clean_cost

app = FastAPI()


@app.get('/')
def read_root():
    """
    Root endpoint for the backend.
    Returns:
        dict: A simple greeting.
    """
    return {"Hello": "World"}


@app.get("/random/{departure}")
def combined_endpoint(departure: str):
    """
    Endpoint to generate random flight information based on
    the selected departure.

    Args:
        departure (str): The departure airport code.

    Returns:
        dict: Randomized flight information.
    """
    result = randomize_destination(departure, flights)
    return {
        "give_output": result['give_output'],
        "arrivalcity": result['arrivalcity']
    }


@app.get('/get_departure')
def get_departure_from_csv():
    """
    Endpoint to retrieve a list of unique departure airports from
    the flights dataset.

    Returns:
        str: JSON representation of unique departure airports.
    """
    results = flights['Departure'].drop_duplicates().to_json(orient='records')
    return results


@app.get('/get_airline')
def airlines():
    """
    Endpoint to retrieve a list of unique airlines from the cleaned dataset.

    Returns:
        str: JSON representation of unique airlines.
    """
    tt = df_clean['Air Carrier'].drop_duplicates().to_json(orient='records')
    return tt


@app.get('/airlines-{AIRLINES}')
def average_web(AIRLINES):
    """
    Endpoint to calculate the average flight price for a specific airline.

    Args:
        AIRLINES (str): The selected airline.

    Returns:
        dict: Result of the average price calculation for the airline.
    """
    result = calculate_average_price_airline(flights, AIRLINES)
    return result


@app.get('/avg/{Departure}/{Arrival}')
def avg_price(Departure: str, Arrival: str):
    """
    Endpoint to calculate the average flight price between two airports.

    Args:
        Departure (str): The departure airport code.
        Arrival (str): The arrival airport code.

    Returns:
        str: Result of the average price calculation.
    """
    result = calculate_average_price(flights, Departure, Arrival)
    if result is not None:
        result = round(result, 2)
        result = "{:.2f}".format(result)
        return result
    else:
        return None


@app.get('/arrival-{Arrival}')
def cheapest(Arrival):
    """
    Endpoint to find the cheapest flights to a specific destination.

    Args:
        Arrival (str): The arrival airport code.

    Returns:
        dict: Result of the cheapest flights calculation.
    """
    result = cheapest_to_fly(flights, Arrival)
    return result


@app.get('/Cleaning/{Value}')
def clean(Value):
    """
    Endpoint to clean a cost value.

    Args:
        Value: The cost value to be cleaned.

    Returns:
        str: Result of the cost cleaning operation.
    """
    result = clean_cost(Value)
    return result
