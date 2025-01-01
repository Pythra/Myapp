import requests

# Set your Postmark API token and email details
API_URL = "https://api.postmarkapp.com/email"
API_TOKEN = "c63c358d-8bc7-4c50-a152-e7ead3290119"

# Email data
payload = {
    "From": "support@useasappay.com",
    "To": "pEZE336@GMAIL.COM",
    "Subject": "Hello from Postmark",
    "HtmlBody": "<strong>Hello</strong> there your activation code is 900.",
    "MessageStream": "outbound"
}

# HTTP headers
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Postmark-Server-Token": API_TOKEN
}

# Send the POST request
response = requests.post(API_URL, json=payload, headers=headers)

# Print the response
if response.status_code == 200:
    print("Email sent successfully:", response.json())
else:
    print("Failed to send email:", response.status_code, response.text)
