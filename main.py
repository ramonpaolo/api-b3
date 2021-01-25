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
    if request.args.get('ticker') == None:
        return {
            'error': "ticker value is null"
        }
    elif request.args.get('ticker') == "all":
        infoActions = []
        with open("data.json") as file:
            dataJson = json.load(file)
       
        for x in dataJson["data"]:
            print(x)

            url = requests.get(
                f"https://statusinvest.com.br/acoes/{x['ticker']}")
            nav = BeautifulSoup(url.text, "html5lib")
            infoActions.append({"nome": x["nome"], "logo": x["logo"], "info": x["info"], "ticker": x["ticker"], "valor_cota": nav.find('strong').text,
                                "dy": nav.find_all("strong")[3].text, "oscilacao_cota": nav.find_all('b')[9].text.strip("\n").lstrip().rstrip(), "preco_min_cota": "32.40", "preco_max_cota": "33.40", "ultimo_pagamento": "04/01/2021"})
        return jsonify(data=infoActions)

    else:
        infoAction["ticker"] = request.args.get("ticker").upper()
        url = requests.get(
            f"https://statusinvest.com.br/acoes/{request.args.get('ticker')}")
        nav = BeautifulSoup(url.text, "html5lib")

        with open("data.json") as file:
            dataJson = json.load(file)
        qtdData = 0

        for x in dataJson["data"]:
            qtdData = 1
            if x["ticker"] == infoAction["ticker"]:
                infoAction["nome"] = x["nome"]
                infoAction["logo"] = x["logo"]
                infoAction["info"] = x["info"]
                infoAction["ticker"] = x["ticker"]
                infoAction["valor_cota"] = nav.find('strong').text
                infoAction["dy"] = nav.find_all("strong")[3].text
                infoAction["oscilacao_cota"] = nav.find_all(
                    'b')[9].text.strip("\n").lstrip().rstrip()
                infoAction["preco_min_cota"] = "32.30"
                infoAction["preco_max_cota"] = "32.34"
                infoAction["ultimo_pagamento"] = "04/01/2021"
                qtdData = 0
                print("Tem JSON")
                print(infoAction)
                return jsonify(data=infoAction)

        if qtdData == 1:
            print("NÃO tem JSON")
            try:
                infoAction["info"] = "Texto"
                infoAction["nome"] = nav.find("small").text
                try:
                    text = wikipedia.summary(infoAction["nome"], 3)
                    infoAction["info"] = GoogleTranslator(
                        source="auto", target="pt").translate(text)
                except:
                    print("Não conseguiu pegar da Wikipédia/traduzir")

                print(f"Valor cota:{nav.find('strong').text}")
                infoAction["valor_cota"] = nav.find('strong').text

                print(
                    f'Dividend Yield em 12m: {nav.findAll("strong")[3].text}%')
                infoAction["dy"] = nav.find_all("strong")[3].text

                infoAction["oscilacao_cota"] = nav.find_all('b')[9].text

                for x in nav.find_all("div"):
                    if x.get("title") == "Logotipo da empresa '" + infoAction['nome'].upper() + "'":
                        try:
                            print(x.get("title"))
                            infoAction["logo"] = x.get(
                                "data-img").split("(")[1].split(")")[0]
                            print("URL image: " +
                                  x.get("data-img").split("(")[1].split(")")[0])
                        except:
                            print("Não deu certo pegar a IMAGEM")
                            infoAction["logo"] = "https://cdn-statusinvest.azureedge.net/img/company/cover/344.jpg"

            #print(f"Preço Min cota:{nav.find_all('p')[12].text}")
            #infoAction["preco_min_cota"] = nav.find_all('p')[12].text

            #print(f"Preço Max cota:{nav.find_all('p')[13].text}")
            #infoAction["preco_max_cota"] = nav.find_all('p')[13].text

                infoAction["preco_min_cota"] = "32.30"
                infoAction["preco_max_cota"] = "32.34"
                infoAction["ultimo_pagamento"] = "04/01/2021"
                dataJson["data"].insert(0, infoAction)

                with open("data.json", "w") as file:
                    json.dump(dataJson, file)

                return jsonify(data={
                    "nome": infoAction["nome"],
                    "ticker": request.args.get("ticker").upper(),
                    "dy": infoAction["dy"],
                    "ultimo_pagamento": infoAction["ultimo_pagamento"],
                    "preco_max_cota": infoAction["preco_max_cota"],
                    "preco_min_cota": infoAction["preco_min_cota"],
                    "oscilacao_cota": infoAction["oscilacao_cota"].strip("\n").lstrip().rstrip(),
                    "valor_cota": infoAction["valor_cota"],
                    "info": infoAction["info"],
                    "logo": infoAction["logo"]
                })

            except:
                print("Não deu para pegar o valor do DY")
                return {
                    "error": "not value"
                }


if __name__ == "__main__":
    app.run(port=3000, host="192.168.100.106", threaded=True)
