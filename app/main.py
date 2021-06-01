from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from models import *
from helper import *
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
def test():
    return {"status":200, "body": "Success"}

@app.post("/predict_report")
def predict_report(report: ReportModel):
    report_list = get_report_filtered(report.category)["values"]
    current_latlng = [report.latitude, report.longitude]
    report_tocheck = []
    for rep in report_list:
        if(rep["latitude"] == None or rep["longitude"] == None):
            continue
        report_latlng = [rep["latitude"], rep["longitude"]]
        if(check_latlong_distance(current_latlng, report_latlng)):
            if(check_time(datetime.now(), rep["createdat"])):
                report_tocheck.append(rep)
    prediction = predict_report_batch(report.description, report_tocheck)
    similar = prediction["body"]["similar_sentences"]
    if(len(similar)>0):
        return {"status":200, "body": { "similar_sentences": similar, "message": "There are similar reports." } }
    else:
        req = post_report_db(report)
        if(req):
            return {"status":200, "body": { "similar_sentences": [], "message":"Data berhasil ditambahkan" } }
        else:
            return {"status":400, "body": { "similar_sentences": [], "message":"Error data gagal ditambahkan" } }

@app.post("/add_report")
def add_report(report: ReportModel):
    req = post_report_db(report)
    if(req):
        return {"status":200, "body": "Data berhasil ditambahkan" }
    else:
        return {"status":400, "body": "Data berhasil ditambahkan" }