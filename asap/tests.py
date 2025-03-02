import requests

# API Endpoint
url = "http://localhost:8000/api/giftcard-deposits/"

# Headers
headers = {
    "Authorization": "Token 1aa6281fdfcf29d289c5bd740fc75a90891ba174",
    "Content-Type": "application/json"
}

# Data Payload
data = {
    "owner": 1,  # Replace with actual user ID
    "giftcard": 1,  # Replace with actual gift card ID
    "type": "Amazon",
    "code": "ABCDEFG12345",
    "pin": "1234",
    "price": 100.0,
    "naira": 75000.0,
    "status": "pending"
}

# Sending the request
response = requests.post(url, json=data, headers=headers)

# Print Response
print("Status Code:", response.status_code)
print("Response:", response.json())
