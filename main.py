from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import html5lib
from get_data import getAllValuesFiis, getAllValuesStocks, getAllValuesEtfs, getAllValuesBdrs
from lists import fiis, bdrs, stocks, etfs
import get_data_local

app = Flask(__name__)

infoAction = {}
typeStock = ""

@app.route("/", methods=["GET"])
def route():
    infoAction = get_data_local.getData(request.args.get("ticker"))
    return jsonify(data=infoAction)


if __name__ == "__main__":
    app.run(port=3000, host="192.168.1.11", threaded=True, debug=True)
