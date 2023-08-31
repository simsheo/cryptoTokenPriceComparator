import requests

# Function to fetch price data from CoinGecko using api rest points
def fetch_coingecko_price(url, chain, token_address):
    # Checking the chain and setting the URL and parameters accordingly
    if chain == 'polygon':        
        params = {            
            'ids': 'mimatic',
            'vs_currency': 'usd'
        }
    elif chain == 'fantom':
        params = {
            'contract_addresses': token_address,
            'vs_currencies': 'usd'
        }
    
    # Sending a GET request to the CoinGecko API
    response = requests.get(url, params=params)
    
    
    # Checking the response status code
    if response.status_code == 200:
        data = response.json()
        print(data);
        return data
    else:
        print(f"Error fetching token price from CoinGecko API: {response.status_code}")
        return None
