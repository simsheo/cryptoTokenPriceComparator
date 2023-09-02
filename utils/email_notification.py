import smtplib
from html import escape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# This could all be stored as secret like SLACK_TOKEN
FROM_ADDR = "simsheotest@gmail.com"
TO_ADDR = "sihagseema@yahoo.com"
PASSWORD = "zipltorcaxlskltk"

#Send email with given subject and message
def send_email(subject, message):
    msg = MIMEText(message, 'html')
    msg['From'] = FROM_ADDR
    msg['To'] = TO_ADDR    
    msg['Subject'] = subject
        
    # Create an SMTP instance
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # Initiate the connection with the server
    server.ehlo()

    # Start TLS (Transport Layer Security) encryption
    server.starttls()

    # Login to your Gmail account, this could also be stored as secret like SLACK_TOKEN
    server.login(FROM_ADDR,PASSWORD )
  
    server.sendmail(FROM_ADDR, TO_ADDR, msg.as_string())
    server.quit()

#Generate html  for price report
def generate_breach_html_report(source_price_list, subject):
    rows = ""
    for comp, src_price, ext_price, diff, threshold in source_price_list:
        rows += f"""
        <tr>
            <td>{comp}</td>
            <td>{escape(str(src_price))}</td>
            <td>{escape(str(ext_price))}</td>
            <td>{escape(str(diff))}</td>
            <td>{escape(str(threshold))}</td>
        </tr>
        """
   
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{subject}</title>
    </head>
    <body>
        <h1>{subject}</h1>
        <table border="1">
            <tr>
                <th>Comparator</th>
                <th>DIA Price</th>
                <th>External Price</th>
                <th>Deviation in %</th>
                <th>Threshold</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """ 

#Generate html for thresold breach report
def generate_price_html_report(source_price_list, subject):
    rows = ""
    for source, price in source_price_list:
        rows += f"""
        <tr>
            <td>{source}</td>
            <td>{escape(str(price))}</td>
        </tr>
        """
   
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{subject}</title>
    </head>
    <body>
        <h1>{subject}</h1>
        <table border="1">
            <tr>
                <th>Source</th>
                <th>Price</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """ 
