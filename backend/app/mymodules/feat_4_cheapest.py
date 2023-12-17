

'''
Feature 4 - Cheapest company to fly

This module offers a tool to find the cheapest company
to fly to a specified airport
'''

import pandas as pd
import sys
from df_integrations import flights
sys.path.append('app/mymodules')


def cheapest_to_fly(data, arrival):
    """
    Find the cheapest air carrier for a given arrival location.

    Parameters:
    - data (DataFrame): The DataFrame containing flight data
    with columns 'Arrival', 'Air Carrier', and 'Price in £'.
    - arrival (str): The arrival location
    for which to find the cheapest air carrier.

    Returns:
    - dict: A dictionary containing information about the cheapest air carrier,
    including 'Air Carrier' and 'Price in £'.
    If no data is available for the specified arrival or air carrier,
    returns an informative message.
    """
    arrivals = data[(data['Arrival'] == arrival)]

    avg_price = arrivals.groupby("Air Carrier")["Price in £"].mean().round(2)
    avg_price.reset_index(inplace=True)
    avg_price.sort_values(by="Price in £", inplace=True)

    cheapest = avg_price.iloc[0]

    return cheapest
