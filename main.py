from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import html5lib
from get_data import getAllValuesFiis, getAllValuesStocks, getAllValuesEtfs, getAllValuesBdrs

app = Flask(__name__)

infoAction = {}

@app.route("/", methods=["GET"])
def route():

#----------------------------- FIIs ------------------------

    if request.args.get("fii"):

        url = requests.get(
            f"https://statusinvest.com.br/fundos-imobiliarios/{request.args.get('fii')}")
        nav = BeautifulSoup(url.text, "html5lib")

        infoAction = getAllValuesFiis(nav, request.args.get("fii").upper())
        
        return jsonify(data=infoAction)

#----------------------------- Stocks ------------------------

    elif request.args.get('ticker') != None:
       
        url = requests.get(
            f"https://statusinvest.com.br/acoes/{request.args.get('ticker')}")
        nav = BeautifulSoup(url.text, "html5lib")

        infoAction = getAllValuesStocks(nav, request.args.get("ticker").upper())
        
        return jsonify(data=infoAction)

#----------------------------- ETF ------------------------

    elif request.args.get('etfs') != None:
        
        url = requests.get(
            f"https://statusinvest.com.br/etfs/{request.args.get('etfs')}")
        nav = BeautifulSoup(url.text, "html5lib")

        infoAction = getAllValuesEtfs(nav, request.args.get("etfs").upper())

        return jsonify(data=infoAction)

# ---------------------- BDRs -------------------

    elif request.args.get('bdrs') != None:

        url = requests.get(
            f"https://statusinvest.com.br/bdrs/{request.args.get('bdrs').upper()}")
        nav = BeautifulSoup(url.text, "html5lib")

        infoAction = getAllValuesBdrs(nav, request.args.get('bdrs'))

        return jsonify(data=infoAction)

#----------------------------- ERROR ------------------------

    elif request.args.get('ticker') and request.args.get('fii') and request.args.get('bdrs') and request.args.get('etf')  == None:
        return {
            'error': "ticker value is null"
        }

if __name__ == "__main__":
    app.run(port=3000, host="192.168.100.106", threaded=True)
