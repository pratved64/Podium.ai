import pandas as pd
import numpy as np

df = pd.read_csv('./raceResults.csv')


def calculateMean(arr):
    # print(arr)
    # print(sum(arr) / len(arr))
    edited = []
    zeros = 0
    for i in arr:
        if i == 1000:
            edited.append(0)
            zeros += 1
        else:
            edited.append(i)
    return sum(edited) / (len(edited) - zeros)


raceNum = 0
lastIndex = 0
q1Mean = []
q3Mean = []
q2Mean = []
races = []
while raceNum < 146:
    '''
    resHead = lastIndex + 1
    roundNum = df.iloc[resHead, 1]
    current = resHead
    resTail = resHead
    while df.iloc[current, 1] == roundNum:
        resTail = current
        current += 1
    '''

    start, end = raceNum * 20, (raceNum + 1) * 20
    # print(df.iloc[start:end][['Round', 'Driver', 'GridPosition']])
    q1Mean.append(calculateMean(list(df.iloc[start:end, 11])))
    q2Mean.append(calculateMean(list(df.iloc[start:end, 12])))
    q3Mean.append(calculateMean(list(df.iloc[start:end, 13])))
    races.append(df.iloc[start:end])
    raceNum += 1

print(q1Mean)
print(q2Mean)
print(q3Mean)

dfModified = pd.DataFrame()
for r in range(145):
    currentRace = races[r]
    currentQ1 = q1Mean[r]
    currentQ2 = q2Mean[r]
    currentQ3 = q3Mean[r]

    for driver in range(20):
        currentRace.iloc[driver, -3] = np.float64(currentRace.iloc[driver, 11] - currentQ1)
        currentRace.iloc[driver, -2] = np.float64(currentRace.iloc[driver, 12] - currentQ2)
        currentRace.iloc[driver, -1] = np.float64(currentRace.iloc[driver, 13] - currentQ3)

    print(currentRace[['Driver', 'MeanDeltaQ1', 'MeanDeltaQ2', 'MeanDeltaQ3']])
    dfModified = pd.concat([dfModified, currentRace], axis=0)

dfModified.to_csv('raceResults1.csv')
