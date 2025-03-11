import requests

url = "http://127.0.0.1:5000/predict"
data = {
    "type_of_meal_plan": "Meal Plan 1",
    "room_type_reserved": "Room_Type 1",
    "market_segment_type": "Offline"
}

response = requests.post(url, json=data)
print(response.json())
