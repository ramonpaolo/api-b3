import json
import sqlite3
from bs4 import BeautifulSoup
import requests

#dbDocuments = sqlite3.connect("../database/documentosRelacaoComInvestidores.db")
dbBussines = sqlite3.connect("../database/tickers.db")

#db.execute("create table documentosRelacaoComInvestidores(id integer not null primary key autoincrement , ticker text, linkArquivo text, dataArquivo text);")
#db.commit()

#url = requests.get(
#                "https://www.itau.com.br/relacoes-com-investidores/ShowResultado.aspx?IdResultado=uhu/W0xck4lPh0zHZdAxxA==&linguagem=pt")
#nav = BeautifulSoup(url.text, "html5lib")

#print(nav.find_all("a", attrs={"id": "ContentInternal_ContentPlaceHolderConteudo_lnkDownloadApresentacao"})[0]["href"])

dbBussines.execute("create table dataStock(nome text, logo text, info text, ticker text, dy number, precoMinimoCotaEmUmAno number, precoMaximoCotaEmUmAno number, dividendoEmUmAno number, oscilacaoCota number, valorCota number ,linkSiteRi text, valorizacaoCotaUmAno number, cnpj text);")
dbBussines.commit()

#with open("../data.json", "r") as file:
#    for x in json.loads(file.read())['data']:
#        print(x)
#        dbBussines.execute(f"insert into dataStock values('{x['nome']}','{x['logo']}','Nada sobre....','{x['ticker']}','{x['dy']}','{x['preco_min_cota']}','{x['preco_max_cota']}', '{x['ultimo_pagamento']}', '{x['oscilacao_cota']}','{x['valor_cota']}', 'https://', '0.0', 'cnpj');")
#        dbBussines.commit()

#https://www.itau.com.br/relacoes-com-investidores/