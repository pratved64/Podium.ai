from flask import Flask, jsonify, request, render_template
from scraper.qualiScraper import getResults
from predictor.predict import predictPositions
import pandas as pd
import numpy as np
import requests
from predictor.utils import ConvertTimeDelta

app = Flask(__name__)


@app.route("/api/qualifying_data", methods=['GET'])
def fetchQualifyingData():
    try:
        qualData = getResults()
        return jsonify({
            'status': 'success',
            'data': qualData
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


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
    getLink = "http://127.0.0.1:3000/api/qualifying_data"
    df = pd.DataFrame(requests.get(getLink).json()['data'],
                      columns=["Season", "Round", "TrackType", "Circuit", "Weather", "Rainfall", "Driver", "Team",
                               "GridPosition", "Q1", "Q2", "Q3"])
    dfEdited = df.copy()
    for index, row in df.iterrows():
        dfEdited.iloc[index, -3] = np.float64(ConvertTimeDelta(row['Q1']))
        dfEdited.iloc[index, -2] = np.float64(ConvertTimeDelta(row['Q2']))
        dfEdited.iloc[index, -1] = np.float64(ConvertTimeDelta(row['Q3']))

    dfEdited[['Q1', 'Q2', 'Q3']] = dfEdited[['Q1', 'Q2', 'Q3']].astype(float)
    dfEdited['GridPosition'] = dfEdited['GridPosition'].astype(int)

    y = predictPositions(dfEdited)
    dfEdited['FinishingPosition'] = y
    dfEdited.sort_values('FinishingPosition', inplace=True)
    return dfEdited.to_json(orient='records')


@app.route("/")
def home():
    return render_template("dashboard.html")


app.run(port=3000, debug=True)
