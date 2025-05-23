import pickle
import os
import numpy as np
import pandas

baseDir = os.path.dirname(os.path.abspath(__file__))
modelPath = os.path.join(baseDir, 'Models', 'regModel.pkl')
encoderPath = os.path.join(baseDir, 'Models')
encoders = ['labelEncoderCircuit.pkl', 'labelEncoderDriver.pkl', 'labelEncoderTeam.pkl', 'labelEncoderTrackType.pkl']

with open(modelPath, 'rb') as modelFile:
    model = pickle.load(modelFile)

labelEncoders = {}
for e in encoders:
    with open(os.path.join(encoderPath, e), 'rb') as encoderFile:
        labelEncoders[e] = pickle.load(encoderFile)


def calculateMean(arr: list):
    edited = []
    zeros = 0
    for i in arr:
        if i == 1000:
            edited.append(0)
            zeros += 1
        else:
            edited.append(i)
    return sum(edited) / (len(edited) - zeros)


def predictPositions(data: pandas.DataFrame):
    for col in ['TrackType', 'Team', 'Driver', 'Circuit']:
        encoder = labelEncoders[f'labelEncoder{col}.pkl']
        seen = set(encoder.classes_)
        incoming = set(data[col].unique())
        newLabels = list(incoming - seen)
        if len(newLabels) > 0:
            encoder.classes_ = np.concatenate([encoder.classes_, newLabels])

        data[col] = encoder.transform(data[col])

    '''q1Mean = calculateMean(list(data['Q1']))
    q2Mean = calculateMean(list(data['Q2']))
    q3Mean = calculateMean(list(data['Q3']))
    data['MeanDeltaQ1'] = data['Q1']
    data['MeanDeltaQ2'] = data['Q2']
    data['MeanDeltaQ3'] = data['Q3']
    print(q1Mean, q2Mean, q3Mean)
    for i in range(data.shape[0]):
        data.iloc[i, -3] = data.iloc[i, -3] - q1Mean
        data.iloc[i, -2] = data.iloc[i, -2] - q2Mean
        data.iloc[i, -1] = data.iloc[i, -1] - q3Mean'''

    means = data[['Q1', 'Q2', 'Q3']].mean()
    data['MeanDeltaQ1'] = data['Q1'] - means['Q1']
    data['MeanDeltaQ2'] = data['Q2'] - means['Q2']
    data['MeanDeltaQ3'] = data['Q3'] - means['Q3']

    pred = model.predict(data)
    for col in ['TrackType', 'Team', 'Driver', 'Circuit']:
        encoder = labelEncoders[f'labelEncoder{col}.pkl']
        data[col] = encoder.inverse_transform(data[col])

    # for key, value in labelEncoders.items():
    #    with open(os.path.join(encoderPath, key), 'wb') as replaceFile:
    #        pickle.dump(value, replaceFile)

    return pred
