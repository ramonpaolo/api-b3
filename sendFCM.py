import requests
import json

def sendFCM(token: str, message: str):

    serverToken = 'AAAAdg2a0gs:APA91bG11saJcoEf85Bvw6OllXVtlMv_hRcTHYhqzH8mJa4Zz_yqnVYWmxMSCBdaG9z8iD3Bf46v7XYOd72ssIPGFEnLuLkE0h4m8M28fFiz9oRn8-oXFNIFMdvvP9cApMl2gM9Q1Efj'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
      }

    body = {
          "notification": {
        "title": "Alerta de Preço",
        "body": f"{message}"
        },
            "to": f"{token}"
        }
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers=headers, data=json.dumps(body))