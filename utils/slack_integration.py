import requests
import os

def send_slack_notification(slack_url, message, subject,blocks = None):
    # Slack channel or user ID where you want to send the message
    channel = "price_monitoring" # Change this to the appropriate channel or user ID
    # Retrieve the token from the .env file
    slack_token = os.environ.get('SLACK_TOKEN_SECRET')

    if slack_token:
    # Use the token for your application
        print("SLACK token:", slack_token)
    else:
        print("SLACK token not found.")
       
    response = requests.post(slack_url, {
        'token': slack_token,
        'channel': channel,
        'text': message,
        'username': subject,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()
   
    # Check if the message was sent successfully
    if response:
        print(f"Message sent successfully to {channel}!")
    else:
        print("Failed to send message:", response.text)



