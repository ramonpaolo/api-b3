import wikipedia
import json
from deep_translator import GoogleTranslator

infoAction = {}
dataJson = {}

class BasicData():
    def __init__(self, soup, ticker: str): 
        self.soup = soup
        self.ticker = ticker

    def getInfoWikipedia(self):
        try:
            text = wikipedia.summary("Empresa: " + infoAction["nome"], 3)
            return GoogleTranslator(
                source="auto", target="pt").translate(text)
        except:
            print("Não conseguiu pegar da Wikipédia/traduzir")
            return "Nada encontrado...."

    def getDatasInternet(self):
        infoAction["nome"] = self.soup.find("small").text 
        infoAction["logo"] = self.getImage()
        infoAction["info"] = self.getInfoWikipedia()
        infoAction["ticker"] = self.ticker.upper()

        return infoAction

    def getImage(self):
        #print(self.soup.find("div", "company-brand w-100 w-md-30 p-3 rounded mb-3  mb-md-0 bg-lazy"))
        print(self.soup.find("div", title="Logotipo da empresa '"+infoAction["nome"].upper()+"'"))
        if self.soup.find("div", title="Logotipo da empresa '"+infoAction["nome"].upper()+"'") != None:
            getImage = self.soup.find("div", title="Logotipo da empresa '"+infoAction["nome"].upper()+"'")
            try:
                return getImage.__str__().split("(")[1].split(")")[0]
            except:
                print(infoAction["nome"].upper())
                print("Não deu certo pegar a IMAGEM")
                return "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"
            
        return "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"

    def getValuesLocal(self):
        global dataJson
        with open("data.json") as file:
                dataJson = json.load(file)
        for x in dataJson["data"]:
            if x["ticker"] == self.ticker.upper():
                infoAction["nome"] = x["nome"]
                infoAction["logo"] = x["logo"]
                infoAction["info"] = x["info"]
                infoAction["ticker"] = x["ticker"]

                return infoAction
        return None

    def writeData(self, infoAction):
        global dataJson
        if self.getValuesLocal() == None:
            dataJson["data"].insert(0, infoAction)
            with open("data.json", "w") as file:
                json.dump(dataJson, file)       
        return infoAction

#------------------------------------------

def getValuesMoneyBdrs(soup):
    infoAction["preco_min_cota"] = soup.find_all("strong")[1].text
    infoAction["preco_max_cota"] = soup.find_all("strong")[2].text
    infoAction["ultimo_pagamento"] = soup.find_all("span")[33].text
    infoAction["valor_cota"] = soup.find('strong').text
    infoAction["dy"] = soup.find_all("strong")[3].text
    infoAction["oscilacao_cota"] = soup.find_all('b')[10].text.strip("\n").lstrip().rstrip()

    return infoAction

def getAllValuesBdrs(soup, ticker: str):
    comandBasics = BasicData(soup, ticker)
    infoAction = comandBasics.getValuesLocal()
    if infoAction != None:
        infoAction = getValuesMoneyBdrs(soup)
    else:
        infoAction = comandBasics.getDatasInternet()
        infoAction = getValuesMoneyBdrs(soup)
    comandBasics.writeData(infoAction)
    return infoAction

#----------------------------------------

def getValuesMoneyEtfs(soup):
    infoAction["valor_cota"] = soup.find('strong').text
    infoAction["dy"] = None
    infoAction["oscilacao_cota"] = soup.find_all('b')[10].text.strip("\n").lstrip().rstrip()
    infoAction["preco_min_cota"] = soup.find_all("strong")[1].text
    infoAction["preco_max_cota"] = soup.find_all("strong")[2].text
    infoAction["ultimo_pagamento"] = None

    return infoAction

def getAllValuesEtfs(soup, ticker: str):
    comandBasics = BasicData(soup, ticker)
    infoAction = comandBasics.getValuesLocal()
    if infoAction != None:
        infoAction = getValuesMoneyEtfs(soup)
    else:
        infoAction = comandBasics.getDatasInternet()
        infoAction = getValuesMoneyEtfs(soup)
    comandBasics.writeData(infoAction)
    return infoAction

#-----------------------

def getValuesMoneyStocks(soup):
    infoAction["dy"] = soup.find_all("strong")[3].text
    infoAction["preco_min_cota"] = soup.find_all("strong")[1].text
    infoAction["preco_max_cota"] = soup.find_all("strong")[2].text
    infoAction["ultimo_pagamento"] = soup.find_all("span")[32].text
    infoAction["valor_cota"] = soup.find('strong').text
    infoAction["oscilacao_cota"] = soup.find_all('b')[10].text.strip("\n").lstrip().rstrip()

    return infoAction


def getAllValuesStocks(soup, ticker: str):
    comandBasics = BasicData(soup, ticker)
    infoAction = comandBasics.getValuesLocal()
    if infoAction != None:
        infoAction = getValuesMoneyStocks(soup)
    else:
        infoAction = comandBasics.getDatasInternet()
        infoAction = getValuesMoneyStocks(soup)
    comandBasics.writeData(infoAction)
    return infoAction

#-----------------------

def getValuesMoneyFiis(soup):
    infoAction["preco_min_cota"] = soup.find_all("strong")[1].text
    infoAction["preco_max_cota"] = soup.find_all("strong")[2].text
    infoAction["ultimo_pagamento"] = soup.find_all("span")[33].text
    infoAction["valor_cota"] = soup.find('strong').text
    infoAction["dy"] = soup.find_all("strong")[3].text
    infoAction["oscilacao_cota"] = soup.find_all('b')[10].text.strip("\n").lstrip().rstrip()

    return infoAction

def getAllValuesFiis(soup, ticker: str):
    comandBasics = BasicData(soup, ticker)
    infoAction = comandBasics.getValuesLocal()
    if infoAction != None:
        infoAction = getValuesMoneyFiis(soup)
    else:
        infoAction = comandBasics.getDatasInternet()
        infoAction = getValuesMoneyFiis(soup)
    comandBasics.writeData(infoAction)
    return infoAction