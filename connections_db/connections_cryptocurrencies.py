import sqlite3
import os

class ConnectionDBCryptoCurrencies():
    def __init__(self):
        #print(os.system("dir"))
        self.db = sqlite3.connect("database/cryptos.db")

    def createTable(self):
        self.db.execute("create table cryptos(uuid text, symbol text, name text, color text, iconUrl text, marketCap number, price number, change number, rank number, lowVolume number, coinrankingUrl text, volume number, btcPrice number);")
        self.db.commit()

    def updateValues(self, x: object):
        self.db.execute(f"update cryptos set marketCap={float(x['marketCap'])}, price={float(x['price'])}, change={float(x['change'])}, rank={x['rank']}, lowVolume={float(x['lowVolume'])}, volume={float(x['24hVolume'])}, btcPrice={float(x['btcPrice'])} where name='{x['name']}';")

    def addValues(self, x: object):
        self.db.execute(f"""insert into cryptos values('{x['uuid']}','{x['symbol']}','{x['name']}', '{x['color']}','{x['iconUrl']}', {float(x['marketCap'])} , {float(x['price'])}, {float(x['change'])}, {x['rank']}, {float(x['lowVolume'])},'{x['coinrankingUrl']}', {float(x['24hVolume'])},{float(x['btcPrice'])});""")

    def getValues(self):
        return self.db.execute("select * from cryptos;")