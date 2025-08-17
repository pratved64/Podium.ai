import fastf1
import pandas as pd
import time
from predictor.utils import sumBool, ConvertTimeDelta

fastf1.Cache.enable_cache('cache_folder')

raceData = []
seasons = range(2021, 2022)

for season in seasons:
    try:
        schedule = fastf1.get_event_schedule(season, include_testing=False)
        for round_number in range(1, 25):
            try:
                session = schedule.get_event_by_round(round_number).get_session('R')
                quali = schedule.get_event_by_round(round_number).get_session('Qualifying')
                session.load()
                quali.load()

                circuit = session.event.Location
                weather = session.weather_data['AirTemp'].mean()
                rain = sumBool(session.weather_data['Rainfall'])

                results = session.results
                quali_results = quali.results[['Abbreviation', 'TeamName', 'Q1', 'Q2', 'Q3']]
                quali_results = quali_results.fillna('N/A')
                for _, row in results.iterrows():
                    driver = row['Abbreviation']
                    team = row['TeamName']
                    gridPosition = row['GridPosition']
                    finishPosition = row['Position']

                    qualiRow = quali_results[quali_results['Abbreviation'] == driver]
                    q1 = ConvertTimeDelta(str(qualiRow.iloc[0, 2]))
                    q2 = ConvertTimeDelta(str(qualiRow.iloc[0, 3]))
                    q3 = ConvertTimeDelta(str(qualiRow.iloc[0, 4]))

                    raceData.append([
                        season, round_number, circuit, weather, rain,
                        driver, team, gridPosition, finishPosition,
                        q1, q2, q3
                    ])

                print(f"Collected {circuit} ({season}-{round_number})")
                time.sleep(1)

            except Exception as e:
                print(f"Skipping {season}-{round_number} due to {e}")

    except Exception as e:
        print(f"Skipping {season} due to {e}")

print(raceData)
df = pd.DataFrame(raceData,
                  columns=['Season', 'Round', 'Circuit', 'Weather', 'Rainfall', 'Driver', 'Team', 'Grid_Position',
                           'Finishing_Position', 'Q1', 'Q2', 'Q3'])
df.to_csv('./results/modifiedRaceData_2021.csv')
print("Completed!")
