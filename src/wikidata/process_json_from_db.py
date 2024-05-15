import sqlite3
import json
import os

conn = sqlite3.connect('hundred_saints.db')
cursor = conn.cursor()
saints = cursor.execute('SELECT * from hundred_saints')


#keys in the json:
#https://doc.wikimedia.org/Wikibase/master/php/docs_topics_json.html
#type: the type of entry, should be either item or property
#id: the id of the entry
#labels: labels, i.e. the name of the entry in different languages
#descriptions: descriptions for the different languages
#aliases: different names for different languages, multiples for each language possible
#claims: contains different statements about the object, most likely properties(?), i.e. "is saint", "is human"
#sitelinks: links to other sites describing the objects, usually wikipedia-sites only it seems


def parse_json_content(json_saint: dict):
    print(json_saint)

    json_saint.keys()

for id,content in saints:
    print(id)
    print(content)
    json_saint = json.loads(content)
    parse_json_content(json_saint)