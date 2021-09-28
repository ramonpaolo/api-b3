from fastapi import FastAPI
import uvicorn
from get_data_local import DataLocal
from get_price_cryptocurrencies import getValueCryptos

app = FastAPI(debug=False)

infoAction = {"data": {}}

@app.get("/get-ticker/{ticker}")
async def getTicker(ticker: str):
    dataLocal = DataLocal()
    infoAction["data"] = dataLocal.getData(ticker)
    return infoAction

@app.get("/get-tickers")
async def getTickers():
    dataLocal = DataLocal()
    return dataLocal.getOrderDatas("oscilacaoCota")

@app.get("/get-stocks-by-order/{order}")
async def getStocksByOrder(order: str):
    dataLocal = DataLocal()
    return dataLocal.getOrderDatas(order)

@app.get("/get-values-cryptos")
async def getCryptos():
    return {"result": getValueCryptos()}

uvicorn.run(app, host="localhost", port=8000)