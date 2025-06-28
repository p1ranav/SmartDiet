import requests

url = 'http://127.0.0.1:5000/diet-plan'

data = {
    "weight": 70,
    "height": 175,
    "foods": ["Apple", "Chicken Breast", "Broccoli"]
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response Text:", response.text)  # <-- print raw text before parsing json

try:
    print("Response JSON:", response.json())
except Exception as e:
    print("JSON decode error:", e)
