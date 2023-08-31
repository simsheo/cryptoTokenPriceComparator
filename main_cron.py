from tabulate import tabulate
from config import (
    COINGECO_POLYGON_URL, COINGECKO_FANTOM_URL, COINMARKETCAP_MIMATIC_URL,
    DIA_POLYGON_URL, DIA_FANTOM_URL, SLACK_URL, POLYGON_ADDR, FANTOM_ADDR,GRAPHQL_URL
)
from api.price_scraper import fetch_coinmarketcap_price
from api.graphql import fetch_graphql_price
from api import fetch_coingecko_price, fetch_dia_price
from utils import price_threshold_breached, price_variation, send_email, send_slack_notification,generate_price_html_report,generate_breach_html_report

def main():
    THRESHOLD = 10
    token = "Mimatic"
    
    dia_polygon_data = fetch_dia_price(DIA_POLYGON_URL)
    dia_fantom_data = fetch_dia_price(DIA_FANTOM_URL)
    coingecko_polygon_data = fetch_coingecko_price(COINGECO_POLYGON_URL, 'polygon', POLYGON_ADDR)
    coingecko_fantom_data = fetch_coingecko_price(COINGECKO_FANTOM_URL, 'fantom', FANTOM_ADDR)
    
    if dia_polygon_data and dia_fantom_data and coingecko_polygon_data and  coingecko_fantom_data:      
    #Get all the prices from DIA and all external sources
        dia_polygon_price = fetch_dia_price(DIA_POLYGON_URL)['Price']
        dia_fantom_price = fetch_dia_price(DIA_FANTOM_URL)['Price']
        coingecko_polygon_price = fetch_coingecko_price(COINGECO_POLYGON_URL, 'polygon', POLYGON_ADDR)[0]['current_price']
        coingecko_fantom_price = fetch_coingecko_price(COINGECKO_FANTOM_URL, 'fantom', FANTOM_ADDR)[FANTOM_ADDR]['usd']
        
        #Get price using scraper
        coinmarketcap_mimatic_price = fetch_coinmarketcap_price(COINMARKETCAP_MIMATIC_URL)
        
        #Get price using graphql , this is only for demo purpose    
        dia_polygon_graphql_price = fetch_graphql_price(GRAPHQL_URL)
        
        if dia_polygon_price and dia_fantom_price and coingecko_polygon_price and coingecko_fantom_price and coinmarketcap_mimatic_price and dia_polygon_graphql_price:
        
            source_price_list =[
                ("Dia Polygon - API ", dia_polygon_price ), 
                ("Dia Polygon - GRAPHQL ", dia_polygon_graphql_price ), 
                ("Coingecko Polygon- API", coingecko_polygon_price),
                ("Dia Fantom - API ", dia_fantom_price),
                ("Coingecko Fantom - API", coingecko_fantom_price),
                ("CoinMarketMap Aggregated-Scraper ", coinmarketcap_mimatic_price),
            ]  
            
            #Send mail and slack notifications for price fetched
            price_subject = f'DIA and external Prices for -{token}'
            #generate html report for all prices , save it and send it via mail
            html_report = generate_price_html_report(source_price_list, price_subject)
            with open('source_price_report.html', 'w') as file:
                file.write(html_report)
            send_email(price_subject, html_report)
            
            #Convert the table data to a formatted table using tabulate and then send prices report to slack - 
            formatted_table = tabulate(source_price_list, headers=["Source", "Price"], tablefmt="orgtbl")
            slack_table = {"text":"```\n" + formatted_table + "\n```"}
            send_slack_notification(SLACK_URL, slack_table['text'], price_subject)
            
            thresold_breach_list =[];
            #Check for validation breach by comparing to decided threshold
            compare_and_highlight_breach(dia_polygon_price, coingecko_polygon_price, THRESHOLD,"dia_vs_coingecko_polygon", thresold_breach_list )
            compare_and_highlight_breach(dia_fantom_price, coingecko_fantom_price, 60,"dia_vs_coingecko_fantom", thresold_breach_list )
            compare_and_highlight_breach(dia_fantom_price, coinmarketcap_mimatic_price, THRESHOLD,"dia_vs_coinmarketcap_fantom_aggregated", thresold_breach_list )
            compare_and_highlight_breach(dia_polygon_price, coinmarketcap_mimatic_price, THRESHOLD,"dia_vs_coingecko_polygon_aggregated", thresold_breach_list )
                
            if thresold_breach_list:
                #generate html report for all prices , save it and send it via mail
                breach_report_subject = f"Threshold breach Report for {token}"
                html_report = generate_breach_html_report(thresold_breach_list, breach_report_subject)
                with open('thresold_breach_report.html', 'w') as file:
                    file.write(html_report)
                send_email(breach_report_subject, html_report)
            
                #Convert the table data to a formatted table using tabulate and then send prices report to slack - 
                threshold_breach_table = tabulate(thresold_breach_list, headers=["Comparator", "DIA Price", "External Price", "Deviation in %", "Threshold"], tablefmt="orgtbl")
                breach_table = {"text":"```\n" + threshold_breach_table + "\n```"}
                send_slack_notification(SLACK_URL, breach_table['text'], breach_report_subject)

def compare_and_highlight_breach(source_price, external_price,threshold, compartaor,thresold_breach_list):
    if source_price and external_price:
        diff = price_variation(source_price, external_price)
        threshold_breach = price_threshold_breached(diff, threshold);
        if threshold_breach:
            return thresold_breach_list.append((compartaor,source_price,external_price,diff, threshold))
        else:
            thresold_breach_list
  

if __name__ == "__main__":
    main()
