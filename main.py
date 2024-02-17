import requests
from datetime import datetime
import os

GENDER = "male"
WEIGHT_KG = 75
HEIGHT_CM = 168
AGE = 24

API_KEY = os.environ["API_KEY"]
API_ID = os.environ["API_ID"]
SYNDIGO_ENDPOINT = os.environ["SYNDIGO_ENDPOINT"]

SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]
SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]
### Processing user query about exercise with Syndigo API
query = input("Tell me which exercies you did: ")

syndigo_headers = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY
}

syndigo_exercise_config = {
    "query": query,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE

}
syndigo_exercise_endpoint = f"{SYNDIGO_ENDPOINT}/natural/exercise"

response = requests.post(syndigo_exercise_endpoint, headers=syndigo_headers, json=syndigo_exercise_config)

### Recording workouts with current time to Google Sheet with Sheety API
today = datetime.now()
date = today.strftime("%d/%m/%Y")
time = today.strftime("%H:%M:%S")
workouts = [{"date":date, "time":time,"exercise":workout["user_input"].title(), "duration":workout["duration_min"], "calories":workout["nf_calories"]} for workout in response.json()["exercises"]]

for workout1 in workouts:
    sheety_config = {
        "sheet1": workout1
    }
    sheety_headers = {
        "Authorization": SHEETY_TOKEN
    }
    response = requests.post(SHEETY_ENDPOINT, json=sheety_config, headers=sheety_headers)
    print(response.text)



