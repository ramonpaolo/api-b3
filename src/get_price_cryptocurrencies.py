import json
import requests
from connections_db.connections_cryptocurrencies import ConnectionDBCryptoCurrencies
from dotenv import load_dotenv
import os

load_dotenv(".env")

def updateCryptos():
    connectionCrypto = ConnectionDBCryptoCurrencies()

    # Troque a chave de acesso pela sua. https://developers.coinranking.com/account/
    response = requests.get("https://api.coinranking.com/v2/coins", params={'x-access-token': os.getenv("API_KEY")})
    parsed = json.loads(response.text)
    coins = parsed["data"]["coins"]

    for x in coins:
        print(f"uuid: {x['uuid']}")
        print(f"symbol: {x['symbol']}")
        print(f"name: {x['name']}")
        print(f"iconUrl: {x['iconUrl']}")
        print(f"price: {x['price']}")
        print(f"rank: {x['rank']}")
        print(f"btcPrice: {x['btcPrice']} \n")
        connectionCrypto.updateValues(x)
        #Se for sua primeira vez executando, execute primeiro a inserção de dados na tabela
        #connectionCrypto.addValues(x)

    connectionCrypto.db.commit()
    connectionCrypto.db.close()

def getValueCryptos():
    coins = ConnectionDBCryptoCurrencies().getValues()
    coinsInJson = []
    for x in coins:
        coinsInJson.append({'uuid': x[0],
        "symbol": x[1],
        "name": x[2],
        "color": x[3],
        "iconUrl": x[4],
        "marketCap": x[5],
        "price": x[6],
        "change": x[7],
        "rank": x[8],
        "lowVolume": x[9],
        "coinrankingUrl": x[10],
        "24hVolume": x[11],
        "btcPrice": x[12]
        })
    return coinsInJson
    #Code to Download crypto images
    # r = requests.get(x['iconUrl'], stream=True)
    # if r.status_code == 200:
    #    r.raw.decode_content = True
    # Abrir arquivo com permissão de escrita binária
    #    with open(f"assets/crypto/{x['name']}.svg", 'wb') as f:
    #        shutil.copyfileobj(r.raw, f)
    #    print('Downloaded Image: ', f"{x['name']}.svg")
    # else:
    #    print('Não conseguiu salvar a imagem')
