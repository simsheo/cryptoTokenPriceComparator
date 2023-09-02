import logging

# Function to find percentage variation between price from two sources 
def price_variation(dia_price, external_source_price ):
    diff_percentage =  abs(external_source_price - dia_price) / dia_price * 100
    logging.info(f"price_comparator:price_variation-->source price :{dia_price}, external price:{external_source_price}, percentage variation: {diff_percentage}")
    return diff_percentage

#Function to compare price difference with threshold and highlight any breach
def price_threshold_breached(diff_percentage,threshold_percent):
    if diff_percentage > threshold_percent:
        logging.info(f"price_comparator:price_variation-->The percentage variation is more then threshold:: diff {diff_percentage} , threshold {threshold_percent}")
        return True
    else:
        logging.info(f"price_comparator:price_variation-->The percentage variation is less threshold: diff {diff_percentage} , threshold {threshold_percent}")
        return False
