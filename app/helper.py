from math import sin, cos, sqrt, atan2, radians
import requests
import json
from datetime import datetime
import random

def generate_id():
    id1 = random.randint(10, 99)
    id2 = random.randint(10, 99)
    id3 = random.randint(10, 99)
    return f"{id1}.{id2}.{id3}"

def get_report_filtered(filter):
    report = requests.get(f"http://34.101.203.70/{filter}")
    result = json.loads(report.text)
    return result

def post_report_db(report):
    body = {
        "kategori": report.category,
        "sub_kategori": report.subcategory,
        "deskripsi": report.description,
        "latitude": report.latitude,
        "longitude": report.longitude,
        "vote": 1,
        "id_kecamatan": generate_id(),
        "foto": report.img_url
        }
    req = requests.post("http://34.101.203.70/post", data=body)
    return req

def predict_report_batch(first_report, report_batch):
    body = {"firstSentence": first_report, "batch": report_batch}
    prediction = requests.post("http://34.101.189.212/predict_batch", json=body)
    result = json.loads(prediction.text)
    return result

def check_latlong_distance(firstLatLong, secondLatLong, max_distance=5):
    R = 6373.0
    lat1 = radians(firstLatLong[0])
    lon1 = radians(firstLatLong[1])
    lat2 = radians(secondLatLong[0])
    lon2 = radians(secondLatLong[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    if(distance >= max_distance):
        return False
    return True

def check_time(currentDate, secondDate):
    time = datetime.strptime(secondDate, "%Y-%m-%dT%H:%M:%S.%fZ")
    delta = currentDate - time
    if(delta.days > 7):
        return False
    return True
