import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import messaging
import smtplib
import alert_stock_price
import sendFCM

cred = credentials.Certificate("./bovespa-c99eb-firebase-adminsdk-47db2-ff0c7b8081.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client(app)

messageToSendMobile = """Esse email, se refere ao seu alerta criado para a ação stock. A ação stock está ao preço de: R$price"""
messageToSendEmail = """
<html>
<head>Alerta de Preço</head>
<body>
<center>
Esse email, se refere ao seu alerta criado para a ação <b>stock</b>.
A ação <b>stock</b> está ao preço de: <b>R$price</b>
</center>
</body>
</html>
"""

def getDataUser(reference_doc_user: str, ticker: str, price: float, id: int):
    result = db.collection("Users").document(reference_doc_user).get()

    if result.exists:
        dataUser = result.to_dict()

        if dataUser["notificationEmail"] is True:
            messageEmail = messageToSendEmail.replace("stock", ticker).replace("price", f"{price}").encode("utf-8")
            sendMessageEmail(dataUser["email"], messageEmail)

        if dataUser["notificationMobile"] is True:
            messageMobile = messageToSendMobile.replace("stock", ticker).replace("price", f"{price}").__str__()
            sendMessageMobile(dataUser["tokenId"], messageMobile)

        alert_stock_price.removeAlertStock(ticker, price, id, reference_doc_user)

    else:
        print("Não existe")

def sendMessageMobile(token: str, message: str):
    sendFCM.sendFCM(token, message)

def sendMessageEmail(email: str, message: str):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("ramonpaolomaran12@gmail.com", "kukctsnabubuxhzr") #código único
    server.sendmail("ramonpaolomaran12@gmail.com", email, message)
    server.close()