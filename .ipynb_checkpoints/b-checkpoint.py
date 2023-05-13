import requests
from datetime import date

BASE_URL = 'http://127.0.0.1:5000/Tasks_Manager/Tasks'
deadline = str(date.today())

response = requests.put(BASE_URL, json={'activity': 'activity', 'responsible': 'responsible'})
print(response.json())