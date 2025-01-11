import requests

url = "https://apprite.pythonanywhere.com/api/bank/27/"
headers = {
    "Authorization": "Token 9beb3d1fec704831d9d6076acd29b136758731ad",
    "Content-Type": "application/json"
}
data = {"active": False}

response = requests.patch(url, json=data, headers=headers)
print(response.status_code, response.json())
