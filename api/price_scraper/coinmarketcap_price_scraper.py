import requests
from bs4 import BeautifulSoup
import logging

#function to scrape coinmarketcap and get aggregated token price
def fetch_coinmarketcap_price(url):
   
    # Send a GET request to the URL
    response = requests.get(url)
    # Checking the response status code
    if response.status_code == 200:  
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find element with the class containing token price
        price_element = soup.find(class_='sc-16891c57-0 dxubiK base-text')
        if price_element:
            #convert string to float
            token_price = float(price_element.get_text().replace('$', ''))          
            logging.info(f"coinmarketcap_price_scraper:fetch_coinmarketcap_price-->Current token Price: {token_price}")
            return token_price
        else:
            logging.error(f"coinmarketcap_price_scraper:fetch_coinmarketcap_price-->Token price not found on the page {url}.")             
    else:
        logging.error(f"coinmarketcap_price_scraper:fetch_coinmarketcap_price-->Error fetching token price from CoinMarketCap using scraping: {response.status_code}")
        return None   
