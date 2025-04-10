import lightgbm as lgb
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle

df = pd.read_csv('./raceResults1.csv')

labelEncoders = {}

# Non-numeric to Numeric mapping
for col in ['TrackType', 'Circuit', 'Driver', 'Team']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    labelEncoders[col] = le

# Take care of improper values
df.fillna(df.median(), inplace=True)

# Split into inputs and outputs
x = df.drop(columns=['FinishingPosition'])
y = df['FinishingPosition']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=13)

# Gradient Boosting Model Setup
lgb_model = lgb.LGBMRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    min_samples_leaf=1,
    subsample=0.8,
    random_state=34
)

# Train Model
lgb_model.fit(x_train, y_train)

y_pred = lgb_model.predict(x_test)

# Analyse Model Performance
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")
print(f"R2 Score: {r2}")

predictions = pd.DataFrame(y_test)
predictions['PredictedPosition'] = y_pred
print(predictions)

with open('../predictor/Models/regModel.pkl', 'wb') as model:
    pickle.dump(lgb_model, model)

for key, enc in labelEncoders.items():
    with open(f'../predictor/Models/labelEncoder{key}.pkl', 'wb') as encoder:
        pickle.dump(enc, encoder)
