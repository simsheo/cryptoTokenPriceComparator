import requests

# Function to fetch MiMatic price data from a given endpoint
def fetch_dia_price(api_endpoint):
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print("Error fetching price data:", response.status_code)
        return None


