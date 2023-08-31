# Function to validate price between two sources based on predefined threshold 
def price_variation(dia_price, external_source_price ):
    diff_percentage =  abs(external_source_price - dia_price) / dia_price * 100
    print(f"The percentage variation between two sources for price is: {diff_percentage}")
    return diff_percentage

def price_threshold_breached(diff_percentage,threshold_percent):
    if diff_percentage > threshold_percent:
        return True
    else:
        return False