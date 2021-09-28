import sqlite3

db = sqlite3.connect("database/database.db")

db.execute("""
create table alertsPrices(
id integer not null primary key autoincrement,
ticker text,
alertPrice real,
referenceDocUser text,
validity text,
created text,
direction text
);""")