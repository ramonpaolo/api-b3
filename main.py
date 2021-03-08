from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import html5lib
from get_data import getAllValuesFiis, getAllValuesStocks, getAllValuesEtfs, getAllValuesBdrs
from lists import fiis, bdrs, stocks, etfs

app = Flask(__name__)

infoAction = {}
typeStock = ""

@app.route("/", methods=["GET"])
def route():

    if request.args.get("ticker") in stocks:
        typeStock = "stock"
    elif request.args.get("ticker") in fiis:
        typeStock = "fii"
    elif request.args.get("ticker") in etfs:
        typeStock = "etfs"
    elif request.args.get("ticker") in bdrs:
        typeStock = "bdrs"
    else :
        return {
            'error': "ticker value is null"
        }


#----------------------------- FIIs ------------------------

    if typeStock == "fii":

        url = requests.get(
            f"https://statusinvest.com.br/fundos-imobiliarios/{request.args.get('ticker')}")
        nav = BeautifulSoup(url.text, "html5lib")
        
        infoAction = getAllValuesFiis(nav, request.args.get("ticker").upper())
        
        return jsonify(data=infoAction)

#----------------------------- Stocks ------------------------

    elif typeStock == "stock":
       
        url = requests.get(
            f"https://statusinvest.com.br/acoes/{request.args.get('ticker')}")
        nav = BeautifulSoup(url.text, "html5lib")

        infoAction = getAllValuesStocks(nav, request.args.get("ticker").upper())
        
        return jsonify(data=infoAction)

#----------------------------- ETF ------------------------

    elif typeStock == "etfs":
        
        url = requests.get(
            f"https://statusinvest.com.br/etfs/{request.args.get('ticker')}")
        nav = BeautifulSoup(url.text, "html5lib")

        infoAction = getAllValuesEtfs(nav, request.args.get("ticker").upper())

        return jsonify(data=infoAction)

# ---------------------- BDRs -------------------

    elif typeStock == "bdrs":

        url = requests.get(
            f"https://statusinvest.com.br/bdrs/{request.args.get('ticker').upper()}")
        nav = BeautifulSoup(url.text, "html5lib")

        infoAction = getAllValuesBdrs(nav, request.args.get('ticker'))

        return jsonify(data=infoAction)

if __name__ == "__main__":
    app.run(port=3000, host="192.168.100.106", threaded=True)
