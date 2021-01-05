from flask import Flask, request, jsonify
import requests
from time import sleep
from bs4 import BeautifulSoup
import html5lib

app = Flask("B3")

infoAction = {}

@app.route("/", methods=["GET"])
def route():
    if request.args.get('name') == None or request.args.get('ticker') == None:
        return {
            'error': "one value is null"
        }
    else:
        url = requests.get(f"https://www.infomoney.com.br/cotacoes/{request.args.get('name')}-{request.args.get('ticker')}/proventos/")
        nav = BeautifulSoup(url.text, "html5lib")
        
        for x in range(40):
            sleep(1)
            try:
                print("Carregando...")
                infoAction["dy"] = "1,19"
               
                print(f"Valor cota:{nav.find_all('p')[10]}")
                infoAction["valor_cota"] = nav.find_all('p')[10].text

                print(f"Oscilação Cota:{nav.find_all('p')[11]}")
                infoAction["oscilacao_cota"] = nav.find_all('p')[11].text

                print(f"Preço Min cota:{nav.find_all('p')[12]}")
                infoAction["preco_min_cota"] = nav.find_all('p')[12].text

                print(f"Preço Max cota:{nav.find_all('p')[13]}")
                infoAction["preco_max_cota"] = nav.find_all('p')[13].text
                
                infoAction["ultimo_pagamento"] = "04/01/2021"
                
                if infoAction["preco_max_cota"] != None:
                    break
            except:
                print("Não deu para pegar o valor do DY")
                return{
                    "error": "not value"
                }
        print("Nome ativo: " + request.args.get('name') + "\nTICKER: " + request.args.get("ticker") + "\nDY: R$"
        + infoAction["dy"] + "\nÚltimo pagamento: " + infoAction["ultimo_pagamento"])
        return jsonify(data={
                "nome" : request.args.get('name').title(),
                "ticker" : request.args.get("ticker").upper(),
                "dy" : infoAction["dy"],
                "ultimo_pagamento": infoAction["ultimo_pagamento"],
                "preco_max_cota_dia": infoAction["preco_max_cota"],
                "preco_min_cota_dia": infoAction["preco_min_cota"],
                "oscilacao_cota_dia": infoAction["oscilacao_cota"].strip("\n").lstrip().rstrip(),
                "valor_cota": infoAction["valor_cota"]
        })


if __name__ == "__main__":
    app.run(port=3000, host="192.168.100.102", debug=True)