import requests
import os
import logging

def send_slack_notification(slack_url, message, subject,blocks = None):
    # Slack channel or user ID where you want to send the message
    channel = "price_monitoring" # Change this to the appropriate channel or user ID
    
    # Retrieve the token from the , setup as secret
    slack_token = os.environ.get('SLACK_TOKEN')
    if slack_token:
        logging.info(f"slack_integration:send_slack_notification-->SLACK token:{slack_token}")
    else:
        logging.warn("slack_integration:send_slack_notification-->SLACK token not found.")
       
    response = requests.post(slack_url, {
        'token': slack_token,
        'channel': channel,
        'text': message,
        'username': subject,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()
   
    # Check if the message was sent successfully
    if response:
        logging.info(f"slack_integration:send_slack_notification-->Message sent successfully to {channel}!")
    else:
        logging.info(f"slack_integration:send_slack_notification-->Failed to send message:{response.text}")



