from fastapi import FastAPI
import uvicorn
from get_data_local import DataLocal
from alert_stock_price import createAlertStock, getAllAlertsInMyUser, removeAlertStock
from documents_funds import getAllDocumentsByCNPJ
from get_price_cryptocurrencies import getValueCryptos

app = FastAPI(debug=True)

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

@app.put("/create-alert-stock-price")
async def putAlertStockPrice(ticker: str, reference_doc_user: str, price: float, validity: str, created: str, direction: str):
    #print(ticker)
    #print(reference_doc_user)
    createAlertStock(ticker, price, reference_doc_user, validity, created, direction)
    return {
        "result": "done"
    }
@app.get("/get-alerts-stock-price/{reference_doc_user}")
async def getAlertsStockPrice(reference_doc_user: str):
    return getAllAlertsInMyUser(reference_doc_user)

@app.delete("/remove-alert-stock-price")
async def deleteAlertStockPrice(ticker: str, reference_doc_user: str, price: float):
    removeAlertStock(ticker, price, 0, reference_doc_user)
    return {
        "result": "done"
    }

@app.get("/get-documents-funds/{cnpj}")
async def getDocument(cnpj: str):
    return {"result" : getAllDocumentsByCNPJ(cnpj)}

@app.get("/get-values-cryptos")
async def getCryptos():
    return {"result": getValueCryptos()}

uvicorn.run(app, host="192.168.100.105", port=8000)