#process wikidata data from sqlite db
import json
import sqlite3
import sys


hundred_saints_db = sqlite3.connect('./hundred_saints.db')
hundred_saints_cursor = hundred_saints_db.cursor()
hundred_saints_cursor.executescript('''DROP TABLE IF EXISTS hundred_saints; CREATE TABLE hundred_saints (id varchar(20), data json)''')

conn_saints_db = sqlite3.connect('./wikidata_saints.db')
saints_cursor = conn_saints_db.cursor()


saints = saints_cursor.execute('SELECT * FROM saints;')
print("Query executed")


for idx,(id,content) in enumerate(saints):
    idx
    #print(id)
    #print(content)
    hundred_saints_cursor.execute("insert into hundred_saints values (?, ?)", [id, content])
    #do something with it
    if idx>100:
        break
hundred_saints_db.commit()
conn_saints_db.close()
hundred_saints_db.close()