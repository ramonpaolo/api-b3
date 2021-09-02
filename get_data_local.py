import json

def getData(ticker: str):
    with open("data.json", "r") as file:
        data = json.load(file)
        for x in range(0, len(data["data"])):
            if data["data"][x]["ticker"] == ticker.upper():
                return data["data"][x]
