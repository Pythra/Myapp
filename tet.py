import requests

def update_pin(profile_id, token, new_pin):
    url = f"https://apprite.pythonanywhere.com/api/profile/{profile_id}/"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    data = {"pin": new_pin}

    # Send the PUT request
    response = requests.put(url, json=data, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("PIN updated successfully:", response.json())
    else:
        print(f"Failed to update PIN. Status Code: {response.status_code}, Response: {response.json()}")

# Example usage
profile_id = 26  # Replace with the actual profile ID
token = "758b3599a7d374379e2ebe6b4d220bb106eaa65f"  # Replace with the actual token
new_pin = "1234"  # Replace with the new PIN

update_pin(profile_id, token, new_pin)
