import requests

url = "https://apprite.pythonanywhere.com/api/bank/list/"
headers = {"Authorization": "Token 758b3599a7d374379e2ebe6b4d26eaa65f"}

response = requests.get(url, headers=headers)
print(response.status_code, response.json())
