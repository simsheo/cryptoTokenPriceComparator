import logging
import requests

# Function to fetch price data from a given endpoint
def fetch_dia_price(api_endpoint):
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        data = response.json()
        logging.info(f"dia_rest_api:fetch_dia_price-->{data}")
        return data
    else:
        logging.info(f"dia_rest_api:fetch_dia_price-->Error fetching price data:{response.status_code}")
        return None


