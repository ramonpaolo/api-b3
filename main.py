from flask import Flask, request
from selenium.webdriver import Chrome
from time import sleep

app = Flask("B3")

infoAction = {}

@app.route("/", methods=["GET"])
def route():
    if request.args.get('name') == None or request.args.get('ticker') == None:
        return {
            'error': "one value is null"
        }
    else:
        nav = Chrome("../chromedriver")
        nav.get(f"https://www.infomoney.com.br/cotacoes/{request.args.get('name')}-{request.args.get('ticker')}/proventos/")
        for x in range(10):
            sleep(1)
            try:
                infoAction["dy"] = nav.find_elements_by_xpath('//tr[@class="even"]/td')[1].text
                infoAction["ultimo_pagamento"] = nav.find_elements_by_xpath('//tr[@class="even"]/td')[6].text
                nav.close()
                print("carregando...")
                break
            except:
                print("Não deu para pegar o valor do DY")
        print("Nome ativo: " + request.args.get('name') + "\nTICKER: " + request.args.get("ticker") + "\nDY: R$"
        + infoAction["dy"] + "\nÚltimo pagamento: " + infoAction["ultimo_pagamento"])
        return {
                "nome" : request.args.get('name'),
                "ticker" : request.args.get("ticker"),
                "dy" : infoAction["dy"],
                "ultimo_pagamento": infoAction["ultimo_pagamento"],
                "error": ""
        }


if __name__ == "__main__":
    app.run(port=3000, host="192.168.100.102")