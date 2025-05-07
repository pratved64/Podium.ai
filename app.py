from flask import Flask, jsonify, request, render_template
from scraper.qualiScraper import getResults, f1_calendar, updateGP, lastUpdated
from predictor.predict import predictPositions
import pandas as pd
import numpy as np
import requests
import os
from predictor.utils import ConvertTimeDelta
from datetime import datetime

app = Flask(__name__)

hostName = os.getenv("DOMAIN_NAME")


def fetchQualifyingData():
    today = datetime.today().date()
    lastDate = datetime.strptime(lastUpdated, "%Y-%m-%d").date()
    if today != lastDate:
        for i in range(len(f1_calendar)):
            gpDate = datetime.strptime(f1_calendar[i]["date"], "%Y-%m-%d").date()
            nextGPDate = datetime.strptime(f1_calendar[i + 1]["date"], "%Y-%m-%d").date()
            if gpDate < today < nextGPDate:
                print('Found interval!')
                break
            elif gpDate < today:
                updateGP(f1_calendar[i]['gp'], True)
                print("Completed GP:", f1_calendar[i]['gp'])
            else:
                updateGP(f1_calendar[i]['gp'], False)

    try:
        qualData = getResults()
        return {
            'status': 'success',
            'data': qualData
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }


'''@app.route("/api/predict", methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame(data)

    predictions = predictPositions(df)
    df['PredictedPosition'] = predictions
    sortedDF = df.sort_values(by='PredictedPosition')
    print(sortedDF)
    return jsonify(sortedDF.to_dict(orient="records"))
'''


@app.route("/api/predict", methods=['GET'])
def getPredictions():
    getLink = hostName + "/api/qualifying_data"
    print(getLink)
    rq = fetchQualifyingData()
    df = pd.DataFrame(rq['data'],
                      columns=["Season", "Round", "TrackType", "Circuit", "Weather", "Rainfall", "Driver", "Team",
                               "GridPosition", "Q1", "Q2", "Q3"])
    #df = pd.DataFrame()
    dfEdited = df.copy()
    for index, row in df.iterrows():
        dfEdited.iloc[index, -3] = np.float64(ConvertTimeDelta(row['Q1']))
        dfEdited.iloc[index, -2] = np.float64(ConvertTimeDelta(row['Q2']))
        dfEdited.iloc[index, -1] = np.float64(ConvertTimeDelta(row['Q3']))

    for col in ['Q1', 'Q2', 'Q3']:
        dfEdited[col] = df[col].apply(ConvertTimeDelta).astype(float)

    dfEdited['GridPosition'] = dfEdited['GridPosition'].astype(int)

    y = predictPositions(dfEdited)
    dfEdited['FinishingPosition'] = y
    dfEdited.sort_values('FinishingPosition', inplace=True)
    return dfEdited.to_json(orient='records')


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/alt")
def alt():
    return render_template("alt-dashboard.html")

