import sqlite3
from alert_user import getDataUser

def getAlertStock(ticker: str, price: float):
    db = sqlite3.connect("database/database.db")
    result = db.execute(f"select * from alertsPrices where ticker='{ticker}';").fetchall()
    for x in result:
        print(x)
        if x[6] == "more":
            if price >= x[2]:
                getDataUser(reference_doc_user=x[3],ticker=x[1], price=x[2],id=x[0])
        elif x[6] == "less":
            if price <= x[2]:
                getDataUser(reference_doc_user=x[3],ticker=x[1], price=x[2],id=x[0])

    db.close()

def createAlertStock(ticker: str, price: float, reference_doc_user: str, validity: str, created: str, direction: str):
    db = sqlite3.connect("database/database.db")
    db.execute(f"""insert into alertsPrices(ticker, alertPrice, referenceDocUser, validity, created, direction) values('{ticker}', {price}, 
    '{reference_doc_user}', '{validity}', '{created}', '{direction}');""")
    db.commit()
    db.close()

def removeAlertStock(ticker: str, price: float ,id: int, reference_doc_user: str):
    db = sqlite3.connect("database/database.db")
    if id == 0:
        result = db.execute(f"""select * from alertsPrices where referenceDocUser='{reference_doc_user}' and alertPrice={price} and ticker='{ticker}';""").fetchall()
        for x in result:
            db.execute(f"delete from alertsPrices where id={x[0]};")
    else:
        db.execute(f"delete from alertsPrices where id={id};")
    db.commit()
    db.close()

def getAllAlertsInMyUser(reference_doc_user: str):
    db = sqlite3.connect("database/database.db")
    response = db.execute(f"select id, ticker, alertPrice, validity, created, direction from alertsPrices where referenceDocUser='{reference_doc_user}';").fetchall()
    db.close()
    alertsStocksPriceInJson = []
    for x in response:
        print(x)
        alertsStocksPriceInJson.append({"id": x[0], "ticker": x[1], "price": x[2], "validity": x[3], "created": x[4], "direction": x[5]})
    return alertsStocksPriceInJson