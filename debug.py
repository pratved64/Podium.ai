import requests
import pandas as pd
import numpy as np
import pickle
from predictor.utils import ConvertTimeDelta
from predictor.predict import predictPositions

encoderPath = './predictor/Models/labelEncoder.pkl'
getLink = "http://127.0.0.1:3000/api/qualifying_data"
postLink = "http://localhost:3000/api/predict"

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

