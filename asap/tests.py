import requests

# API endpoint
url = "https://myapp-7jrc.onrender.com/api/signup/"

# Test data
data = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "TestPassword123!"
}

# Send POST request
response = requests.post(url, json=data)

# Print response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
