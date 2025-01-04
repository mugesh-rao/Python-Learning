import requests
from urllib.parse import quote
import time

phone_number = "6379299044"
api_key = "xqVoHxJtM417"
base_url = "https://api.textmebot.com/send.php"

def send_message(number):
    message = f"Will"
    encoded_message = quote(message)
    url = f"{base_url}?recipient=+91{phone_number}&apikey={api_key}&text={encoded_message}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Message sent: {message}")
        else:
            print(f"Failed to send message: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

# Loop to send the message 100 times with incremented numbers and a 6-second delay between each
for i in range(1, 101):
    send_message(i)
    time.sleep(6)  # Wait for 6 seconds before sending the next message
