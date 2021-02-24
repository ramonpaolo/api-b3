from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import html5lib
import wikipedia
from deep_translator import GoogleTranslator
import json

app = Flask(__name__)

infoAction = {}

@app.route("/", methods=["GET"])
def route():

    with open("data.json") as file:
            dataJson = json.load(file)

#----------------------------- FIIs ------------------------

    if request.args.get("fii"):

        url = requests.get(
            f"https://statusinvest.com.br/fundos-imobiliarios/{request.args.get('fii')}")
        nav = BeautifulSoup(url.text, "html5lib")

        infoAction["ticker"] = request.args.get("fii").upper()
        
        for x in dataJson["data"]:
            if x["ticker"] == infoAction["ticker"]:
                infoAction["nome"] = x["nome"]
                infoAction["logo"] = x["logo"]
                infoAction["info"] = x["info"]
                infoAction["valor_cota"] = nav.find('strong').text
                infoAction["dy"] = nav.find_all("strong")[3].text
                infoAction["oscilacao_cota"] = nav.find_all(
                    'b')[10].text.strip("\n").lstrip().rstrip()
                infoAction["preco_min_cota"] = nav.find_all("strong")[1].text
                infoAction["preco_max_cota"] = nav.find_all("strong")[2].text
                infoAction["ultimo_pagamento"] = nav.find_all("span")[33].text
                
                print("FIIs: " + infoAction.__str__())

                return jsonify(data=infoAction)

        infoAction["info"] = "Nada a declarar..."
        infoAction["nome"] = nav.find("small").text
        infoAction["preco_min_cota"] = nav.find_all("strong")[1].text
        infoAction["preco_max_cota"] = nav.find_all("strong")[2].text
        infoAction["ultimo_pagamento"] = nav.find_all("span")[32].text
        infoAction["valor_cota"] = nav.find('strong').text
        infoAction["dy"] = nav.find_all("strong")[3].text
        infoAction["oscilacao_cota"] = nav.find_all('b')[10].text.strip("\n").lstrip().rstrip()
        infoAction["logo"] = "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"

        try:
            text = wikipedia.summary(infoAction["nome"], 3)
            infoAction["info"] = GoogleTranslator(
                source="auto", target="pt").translate(text)
        except:
            print("Não conseguiu pegar da Wikipédia/traduzir")

        for x in nav.find_all("div"):
            if x.get("class") == "company-brand w-100 w-md-30 p-3 rounded mb-3  mb-md-0 bg-lazy":
                try:
                    infoAction["logo"] = x.get(
                        "data-img").split("(")[1].split(")")[0]
                    print("URL image: " +
                          x.get("data-img").split("(")[1].split(")")[0])
                except:
                    print("Não deu certo pegar a IMAGEM")

        print("FIIs: " + infoAction.__str__())

        dataJson["data"].insert(0, infoAction)

        with open("data.json", "w") as file:
            json.dump(dataJson, file)

        return jsonify(data=infoAction)

#----------------------------- Stocks ALL ------------------------

    elif request.args.get('ticker') == "all":
        infoActions = []

        for x in dataJson["data"]:
            url = requests.get(
                f"https://statusinvest.com.br/acoes/{x['ticker']}")
            nav = BeautifulSoup(url.text, "html5lib")
            infoActions.append({"nome": x["nome"], "logo": x["logo"], "info": x["info"], "ticker": x["ticker"], "valor_cota": nav.find('strong').text,
                                "dy": nav.find_all("strong")[3].text, "oscilacao_cota": nav.find_all('b')[11].text.strip("\n").lstrip().rstrip(),
                                "preco_min_cota": nav.find_all("strong")[1].text, "preco_max_cota": nav.find_all("strong")[1].text,
                                "ultimo_pagamento": nav.find_all("span")[32].text})
        return jsonify(data=infoActions)

#----------------------------- Stocks ------------------------

    elif request.args.get('ticker') != None:
       
        infoAction["ticker"] = request.args.get("ticker").upper()

        url = requests.get(
            f"https://statusinvest.com.br/acoes/{request.args.get('ticker')}")
        nav = BeautifulSoup(url.text, "html5lib")

        for x in dataJson["data"]:
            if x["ticker"] == infoAction["ticker"]:
                infoAction["nome"] = x["nome"]
                infoAction["logo"] = x["logo"]
                infoAction["info"] = x["info"]
                infoAction["valor_cota"] = nav.find('strong').text
                infoAction["dy"] = nav.find_all("strong")[3].text
                infoAction["oscilacao_cota"] = nav.find_all('b')[10].text.strip("\n").lstrip().rstrip()
                infoAction["preco_min_cota"] = nav.find_all("strong")[1].text
                infoAction["preco_max_cota"] = nav.find_all("strong")[2].text
                infoAction["ultimo_pagamento"] = nav.find_all("span")[32].text
                
                print("Stocks: " + infoAction.__str__())

                return jsonify(data=infoAction)

        infoAction["info"] = "Texto"
        infoAction["nome"] = nav.find("small").text
        infoAction["dy"] = nav.find_all("strong")[3].text
        infoAction["preco_min_cota"] = nav.find_all("strong")[1].text
        infoAction["preco_max_cota"] = nav.find_all("strong")[2].text
        infoAction["ultimo_pagamento"] = nav.find_all("span")[32].text
        infoAction["valor_cota"] = nav.find('strong').text
        infoAction["oscilacao_cota"] = nav.find_all('b')[10].text.strip("\n").lstrip().rstrip()
        infoAction["logo"] = "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"
        
        try:
            text = wikipedia.summary(infoAction["nome"], 3)
            infoAction["info"] = GoogleTranslator(
                source="auto", target="pt").translate(text)
        except:
            print("Não conseguiu pegar da Wikipédia/traduzir")

        for x in nav.find_all("div"):
            if x.get("title") == "Logotipo da empresa '" + infoAction['nome'].upper() + "'":
                try:
                    infoAction["logo"] = x.get(
                        "data-img").split("(")[1].split(")")[0]
                    print("URL image: " +
                            x.get("data-img").split("(")[1].split(")")[0])
                except:
                    print("Não deu certo pegar a IMAGEM")

        dataJson["data"].insert(0, infoAction)

        with open("data.json", "w") as file:
            json.dump(dataJson, file)

        return jsonify(data=infoAction)

#----------------------------- ETF ------------------------

    elif request.args.get('etfs') != None:
        
        url = requests.get(
            f"https://statusinvest.com.br/etfs/{request.args.get('etfs')}")
        nav = BeautifulSoup(url.text, "html5lib")
        infoAction["ticker"] = request.args.get("etfs").upper()
        
        for x in dataJson["data"]:
            if x["ticker"] == infoAction["ticker"]:
                infoAction["nome"] = x["nome"]
                infoAction["logo"] = x["logo"]
                infoAction["info"] = x["info"]
                infoAction["valor_cota"] = nav.find('strong').text
                infoAction["dy"] = None
                infoAction["oscilacao_cota"] = nav.find_all('b')[10].text.strip("\n").lstrip().rstrip()
                infoAction["preco_min_cota"] = nav.find_all("strong")[1].text
                infoAction["preco_max_cota"] = nav.find_all("strong")[2].text
                infoAction["ultimo_pagamento"] = None

                print("ETFs: " + infoAction.__str__())

                return jsonify(data=infoAction)

        infoAction["nome"] = nav.find("small").text
        infoAction["valor_cota"] = nav.find('strong').text
        infoAction["dy"] = None
        infoAction["oscilacao_cota"] = nav.find_all('b')[10].text.strip("\n").lstrip().rstrip()
        infoAction["preco_min_cota"] = nav.find_all("strong")[1].text
        infoAction["preco_max_cota"] = nav.find_all("strong")[2].text
        infoAction["ultimo_pagamento"] = None
        infoAction["info"] = "Nada a declarar..."

        print("ETFs: " + infoAction.__str__())

        try:
            text = wikipedia.summary(infoAction["nome"], 3)
            infoAction["info"] = GoogleTranslator(
                source="auto", target="pt").translate(text)
        except:
            print("Não conseguiu pegar da Wikipédia/traduzir")

        #Procurar pela tag que contêm a URL da logo
        for x in nav.find_all("div"):
            if x.get("class") == "company-brand w-100 w-md-30 p-3 rounded mb-3  mb-md-0 bg-lazy":
                try:
                    infoAction["logo"] = x.get("data-img").split("(")[1].split(")")[0]
                    print("URL image: " + x.get("data-img").split("(")[1].split(")")[0])
                except:
                    print("Não deu certo pegar a IMAGEM")
            else:
                infoAction["logo"] = "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"
        
        dataJson["data"].insert(0, infoAction)
        
        with open("data.json", "w") as file:
            json.dump(dataJson, file)
        
        print(infoAction)
        
        return jsonify(data=infoAction)

# ---------------------- BDRs -------------------

    elif request.args.get('bdrs') != None:

        url = requests.get(
            f"https://statusinvest.com.br/bdrs/{request.args.get('bdrs')}")
        nav = BeautifulSoup(url.text, "html5lib")

        infoAction["ticker"] = request.args.get("bdrs").upper()

        for x in dataJson["data"]:
            if x["ticker"] == infoAction["ticker"]:
                infoAction["nome"] = x["nome"]
                infoAction["logo"] = x["logo"]
                infoAction["info"] = x["info"]
                infoAction["valor_cota"] = nav.find('strong').text
                infoAction["dy"] = nav.find_all("strong")[3].text
                infoAction["oscilacao_cota"] = nav.find_all('b')[10].text.strip("\n").lstrip().rstrip()
                infoAction["preco_min_cota"] = nav.find_all("strong")[1].text
                infoAction["preco_max_cota"] = nav.find_all("strong")[2].text
                infoAction["ultimo_pagamento"] = nav.find_all("span", "sub-value")[3].text

                print("BDRs: " + infoAction.__str__())

                return jsonify(data=infoAction)

        infoAction["nome"] = nav.find("small").text
        infoAction["valor_cota"] = nav.find('strong').text
        infoAction["dy"] = nav.find_all("strong")[3].text
        infoAction["oscilacao_cota"] = nav.find_all('b')[10].text.strip("\n").lstrip().rstrip()
        infoAction["info"] = "Nada a declarar..."
        infoAction["preco_min_cota"] = nav.find_all("strong")[1].text
        infoAction["preco_max_cota"] = nav.find_all("strong")[2].text
        infoAction["ultimo_pagamento"] = nav.find_all("span")[32].text
        infoAction["logo"] = "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"

        try:
            text = wikipedia.summary(infoAction["nome"], 3)
            infoAction["info"] = GoogleTranslator(
                source="auto", target="pt").translate(text)
        except:
            print("Não conseguiu pegar da Wikipédia/traduzir")

        #Procurar pela tag que contêm a URL da logo
        for x in nav.find_all("div"):
            if x.get("class") == "company-brand w-100 w-md-30 p-3 rounded mb-3  mb-md-0 bg-lazy":
                try:
                    infoAction["logo"] = x.get(
                        "data-img").split("(")[1].split(")")[0]
                    print("URL image: " +
                          x.get("data-img").split("(")[1].split(")")[0])
                except:
                    print("Não deu certo pegar a IMAGEM")

        print("BDRs: " + infoAction.__str__())

        dataJson["data"].insert(0, infoAction)

        with open("data.json", "w") as file:
            json.dump(dataJson, file)

        return jsonify(data=infoAction)

#----------------------------- ERROR ------------------------

    elif request.args.get('ticker') and request.args.get('fii') and request.args.get('bdrs') and request.args.get('etf')  == None:
        return {
            'error': "ticker value is null"
        }

if __name__ == "__main__":
    app.run(port=3000, host="192.168.100.106", threaded=True, debug=True)
