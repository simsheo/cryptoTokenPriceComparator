import smtplib
from html import escape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, message):
    fromaddr ="simsheotest@gmail.com"
    toaddr = "sihagseema@yahoo.com"
    
    msg = MIMEText(message, 'html')
    msg['From'] = fromaddr
    msg['To'] = toaddr    
    msg['Subject'] = subject
        
    # Create an SMTP instance
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # Initiate the connection with the server
    server.ehlo()

    # Start TLS (Transport Layer Security) encryption
    server.starttls()

    # Login to your Gmail account
    server.login(fromaddr, "zipltorcaxlskltk")
  
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

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