'''We want to create a "surprise me" function where you only need to input the departure airport and it gives a list 
   of possible destinations + dates'''

import pandas as pd
from df_integrations import flights
import random
import difflib

def randomize_destination(departure, df):
    """
    Generate a list of possible destinations and available dates based on the departure airport.

    Parameters:
    - departure (str): The user's selected departure airport.
    - df (DataFrame): The flight data, such as "flights" DataFrame.

    Returns:
    - dict: A dictionary containing "give_output" and "arrivalcity".
    """
    departure = departure.upper()

    if df.empty:
        return "Data are not available for this dataset"
    else:
        possible_destinations = df[df['Departure'] == departure]['Arrival'].unique()

        if possible_destinations.size > 0:
            chosen_destination = random.choice(possible_destinations)

            def give_output(destination, df):
                available_dates = df[(df['Departure'] == departure) & (df['Arrival'] == destination)]['Travel Date']
                available_dates = ', '.join(available_dates.astype(str))
                return f'{destination}', f'AVAILABLE DATES: {available_dates}'
        else:
            return "We are sorry, but we don't have any flights from this departure"

    def arrivalcity():
        return chosen_destination

    return {
        'give_output': give_output(chosen_destination, df),
        'arrivalcity': arrivalcity()
    }






