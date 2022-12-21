import sqlite3
from connections_db.connections_cryptocurrencies import ConnectionDBCryptoCurrencies

dbTickers = sqlite3.connect("database/tickers.db")
dbTickers.execute("create table dataStock(nome text, logo text, info text, ticker text, dy number, precoMinimoCotaEmUmAno number, precoMaximoCotaEmUmAno number, dividendoEmUmAno number, oscilacaoCota number, valorCota number ,linkSiteRi text, valorizacaoCotaUmAno number, cnpj text);")
dbTickers.commit()

ConnectionDBCryptoCurrencies().createTable()