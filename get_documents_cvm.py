import pandas as pd
import sqlite3

df = pd.read_csv("database/backup.csv", sep=";")
print(df.columns)
db = sqlite3.connect("database/fundos.db")
db.execute("create table eventualFundosImobiliarios(tipoFundo text, cnpjFundo text, nomeFundo text, dataDocumento text, dataRecebimento text, tipoDocumento text, nomeArquivo text, idDocument integer not null primary key autoincrement, linkArquivo text)")
countErrors = 0
for x in df.values:
    #print(x)
    try:
        db.execute(f"insert into eventualFundosImobiliarios(tipoFundo, cnpjFundo, nomeFundo, dataDocumento, dataRecebimento, tipoDocumento, nomeArquivo, linkArquivo) values('{x[0]}', '{x[1]}','{x[2]}','{x[3]}','{x[4]}','{x[5]}','{x[6]}','{x[8]}')")
    except:
        countErrors = countErrors+1
db.commit()
print(countErrors)
db.close()