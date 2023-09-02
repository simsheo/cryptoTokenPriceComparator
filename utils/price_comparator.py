import logging

# Function to validate price between two sources based on predefined threshold 
def price_variation(dia_price, external_source_price ):
    diff_percentage =  abs(external_source_price - dia_price) / dia_price * 100
    logging.info(f"The percentage variation between two sources for price is: {diff_percentage}")
    return diff_percentage

#Function to compare price difference with threshold and highlight any breach
def price_threshold_breached(diff_percentage,threshold_percent):
    if diff_percentage > threshold_percent:
        logging.info("The percentage variation is more then threshold")
        return True
    else:
        logging.info("The percentage variation is more then threshold")
        return False
