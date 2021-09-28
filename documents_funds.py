import sqlite3

def getAllDocumentsByCNPJ(cnpj: str):
    cnpj = cnpj.replace("slash", "/").replace("q", "-")
    db = sqlite3.connect("database/fundos.db")
    datas = db.execute(f"select * from eventualFundosImobiliarios where cnpjFundo='{cnpj}'").fetchall()
    db.close()
    datasInJson = []
    for x in datas:
        print(x)
        datasInJson.append({
        "tipoFundo": x[0],
        "cnpjFundo": x[1],
        "nomeFundo": x[2],
        "dataDocumento": x[3],
        "dataRecebimento": x[4],
        "nomeArquivo": x[6],
        "idDocument": x[7],
        "linkArquivo": x[8]
    })
    return datasInJson