import json

if __name__ == '__main__':
    with open("circuits2025.json", 'r') as jsonFile:
        data = json.load(jsonFile)
        start = 1254
        for details in data.values():
            if details['name'] != "Silverstone":
                details['index'] = start
                start += 1
            else:
                details['index'] = 1277

    with open("circuits2025.json", 'w') as jsonFile:
        json.dump(data, jsonFile)