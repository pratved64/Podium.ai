import requests
from bs4 import BeautifulSoup
import os
import json
from dotenv import load_dotenv

load_dotenv()

weatherKey = os.getenv("WEATHER_API_KEY")

base_dir = os.path.dirname(os.path.abspath(__file__))
circuitsPath = os.path.join(base_dir, "circuits2025.json")
metadataPath = os.path.join(base_dir, "metadata.json")

with open(circuitsPath, 'r') as file:
    gpData = json.load(file)

with open(metadataPath, 'r') as file:
    lastUpdated = json.load(file)['lastUpdate']

teamMap = {
    'McLaren': 'McLaren',
    'McLaren Mercedes': 'McLaren',
    'Mercedes': 'Mercedes',
    'Ferrari': 'Ferrari',
    'Red Bull Racing Honda RBPT': 'Red Bull Racing',
    'Haas Ferrari': 'Haas F1 Team',
    'Williams Mercedes': 'Williams',
    'Aston Martin Aramco Mercedes': 'Aston Martin',
    'Racing Bulls Honda RBPT': 'RB',
    'Alpine Renault': 'Alpine',
    'Kick Sauber Ferrari': 'Kick Sauber',
}

f1_calendar = [
    {"round": 1, "date": "2025-03-16", "gp": "australia"},
    {"round": 2, "date": "2025-03-23", "gp": "china"},
    {"round": 3, "date": "2025-04-06", "gp": "japan"},
    {"round": 4, "date": "2025-04-13", "gp": "bahrain"},
    {"round": 5, "date": "2025-04-20", "gp": "saudi-arabia"},
    {"round": 6, "date": "2025-05-04", "gp": "miami"},
    {"round": 7, "date": "2025-05-18", "gp": "imola"},
    {"round": 8, "date": "2025-05-25", "gp": "monaco"},
    {"round": 9, "date": "2025-06-01", "gp": "spain"},
    {"round": 10, "date": "2025-06-15", "gp": "canada"},
    {"round": 11, "date": "2025-06-29", "gp": "austria"},
    {"round": 12, "date": "2025-07-06", "gp": "great-britain"},
    {"round": 13, "date": "2025-07-27", "gp": "belgium"},
    {"round": 14, "date": "2025-08-03", "gp": "hungary"},
    {"round": 15, "date": "2025-08-31", "gp": "netherlands"},
    {"round": 16, "date": "2025-09-07", "gp": "italy"},
    {"round": 17, "date": "2025-09-21", "gp": "azerbaijan"},
    {"round": 18, "date": "2025-10-05", "gp": "singapore"},
    {"round": 19, "date": "2025-10-19", "gp": "usa"},
    {"round": 20, "date": "2025-10-26", "gp": "mexico"},
    {"round": 21, "date": "2025-11-09", "gp": "brazil"},
    {"round": 22, "date": "2025-11-22", "gp": "las-vegas"},
    {"round": 23, "date": "2025-11-30", "gp": "qatar"},
    {"round": 24, "date": "2025-12-07", "gp": "abu-dhabi"},
]


def updateGP(circuitKey, comp):
    gpData[circuitKey]['completed'] = comp
    with open(circuitsPath, 'w') as gpFile:
        json.dump(gpData, gpFile)



def loadCircuits(path=circuitsPath) -> dict:
    with open(path, 'r') as f:
        return json.load(f)


def scrapeResults(season, slug, weather, raceID=1255):
    url = f'https://www.formula1.com/en/results/{season}/races/{raceID}/{slug}/qualifying'
    resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if resp.status_code != 200:
        raise Exception(f'Failed to load qualifying page: Status {resp.status_code}')

    soup = BeautifulSoup(resp.text, 'html.parser')

    # ---- Circuit / round location (avoid brittle CSS-module class) ----
    circuit_el = soup.select_one('button#content-dropdown span span')
    circuit = circuit_el.get_text(strip=True) if circuit_el else (slug.replace('-', ' ').title() if slug else "Unknown Circuit")

    # ---- Results table ----
    table = soup.select_one('table.f1-table')

    if not table:
        raise Exception("Results table not found!")

    tbody = table.find('tbody')
    if not tbody:
        raise Exception("Results table body not found!")

    qualifyingResults = []
    pos = 1
    for row in tbody.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) < 7:
            continue

        # Driver 3-letter code inside <span class="md:hidden">CODE</span>
        driverCell = cells[2]
        code_span = driverCell.select_one('span.md\\:hidden')
        driverCode = code_span.get_text(strip=True) if code_span else "N/A"

        # Team name: plain text of the TEAM cell
        team = cells[3].get_text(strip=True) or "N/A"

        # Q1/Q2/Q3: text inside the <p> tag in each cell
        def td_p_text(td):
            p = td.find('p')
            t = p.get_text(strip=True) if p else td.get_text(strip=True)
            return t if t else "N/A"

        q1 = td_p_text(cells[4])
        q2 = td_p_text(cells[5])
        q3 = td_p_text(cells[6])

        qualifyingResults.append({
            "Season": season,
            "Round": (raceID - 1253), 
            "Circuit": circuit,
            "Weather": weather[0],
            "Rainfall": weather[1],
            "Driver": driverCode,
            "Team": teamMap.get(team, team),
            "GridPosition": pos,
            "Q1": q1,
            "Q2": q2,
            "Q3": q3
        })
        pos += 1

    return qualifyingResults


def checkWet(weatherCode) -> int:
    rain_codes = [
        1072, 1150, 1153, 1168, 1171, 1180, 1183, 1186, 1189, 1192, 1195, 1198, 1201, 1204, 1207, 1240, 1243, 1246,
        1249, 1252, 1273, 1276, 1087
    ]
    return 1 if weatherCode in rain_codes else 0


def getWeather(lat, lon):
    url = f"http://api.weatherapi.com/v1/current.json?key={weatherKey}&q={lat},{lon}"
    response = requests.get(url)
    response.raise_for_status()
    resJson = response.json()['current']
    rainfall = checkWet(resJson['condition']['code'])
    return resJson['temp_c'], rainfall


def getResults():
    CIRCUIT_COORDS = loadCircuits()
    current = {}
    for val in CIRCUIT_COORDS.values():
        if not val['completed']:
            current = val
            break

    try:
        r = scrapeResults(2025, current['name'], getWeather(current['lat'], current['lon']), raceID=current['index'])
        return r
    except Exception as e:
        print("Error:", e)
        return None


if __name__ == '__main__':
    print(*getResults(), sep="\n")
