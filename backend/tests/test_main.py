import os
import sys
from fastapi.testclient import TestClient
import pandas as pd

# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Now you can do the relative import
from app.main import app
from app.mymodules.Destination_random import randomize_destination
from app.mymodules.df_integrations import flights


"""
Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
 """

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_success_read_item():
    response = client.get("/query/Albert Einstein")
    assert response.status_code == 200
    assert response.json() == {"person_name": 'Albert Einstein', 
                               "birthday": '03/14/1879'}


""" def test_fail_read_item():
    response = client.get("/query/Pippo")
    assert response.status_code == 200
    assert response.json() == {"error": "Person not found"} """


# The following will generate an error in pycheck
""" def test_success_read_item_module():
    response = client.get("/module/search/Albert Einstein")
    assert response.status_code == 200
    assert response.json() == {"Albert Einstein's birthday is 03/14/1879."} """


# The following is correct, can you spot the diffence?
def test_success_read_item_module():
    response = client.get("/module/search/Albert Einstein")
    assert response.status_code == 200
    assert response.json() == ["Albert Einstein's birthday is 03/14/1879."]

def test_cheapest_to_fly():
    response = client.get('/arrival-LONDON - LGW')
    assert response.status_code == 200
    assert response.json() == {'Air Carrier': 'EASYJET', 'Price in £': 77.0}

def test_randomize_destination_empty_df():
    # Test with an empty dataframe
    empty_df = pd.DataFrame()
    departure = 'ROME'
    response = randomize_destination(departure, empty_df)
    assert response == 'data are not available for this dataset'

def test_average_class_price():
    # Test with valid input
    response = client.get('/FLYBE')
    assert response.status_code == 200
    assert response.json() == 'Average Price ECONOMY: 114.62 £Average Price FIRST: 46.95 £'

def test_average_one_class():
    # Test 
    response = client.get('/AEROMEXICO')
    assert response.status_code == 200
    assert response.json() == 'Average Price ECONOMY: 128.10 £ The airline only has ECONOMY class flights'


def test_combined_endpoint_valid_departure():
    # Test with a valid departure airport
    response = client.get('/random/LONDON - LGW')
    assert response.status_code == 200
    data = response.json()  # or the expected data type
    assert data['arrivalcity'] in data['give_output']

