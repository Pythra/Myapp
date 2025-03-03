import requests

url = "https://apprite.pythonanywhere.com/api/initiate-email-verification/"
data = {
    "email": "peze336@gmail.com"  # Test email
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())
