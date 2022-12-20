import sqlite3

class DataLocal():
    def getData(self, ticker: str):
        db = sqlite3.connect("./database/tickers.db")
        data = db.execute(f"select * from dataStock where ticker='{ticker.upper()}'").fetchall()
        # print(data[0])
        return {
            "nome": data[0][0],
            "logo": data[0][1],
            "info": data[0][2],
            "ticker": data[0][3],
            "dy": data[0][4],
            "preco_min_cota": data[0][5],
            "preco_max_cota": data[0][6],
            "ultimo_pagamento": data[0][7],
            "oscilacao_cota": data[0][8],
            "valor_cota": data[0][9],
            "linkSiteRi": data[0][10],
            "valorizacaoCota": data[0][11],
            "cnpj": data[0][12],
        }

    def getOrderDatas(self, order: str):
        db = sqlite3.connect("./database/tickers.db")
        datas = db.execute(f"select * from dataStock order by {order}").fetchall()
        datasInJson = []
        for x in datas:
            if x[0] != "":
                datasInJson.append({"data": {
                    "nome": x[0],
                    "logo": x[1],
                    "info": x[2],
                    "ticker": x[3],
                    "dy": x[4],
                    "preco_min_cota": x[5],
                    "preco_max_cota": x[6],
                    "ultimo_pagamento": x[7],
                    "oscilacao_cota": x[8],
                    "valor_cota": x[9],
                    "linkSiteRi": x[10],
                    "valorizacaoCota": x[11],
                    "cnpj": x[12]}
                })
        return {"result": datasInJson}