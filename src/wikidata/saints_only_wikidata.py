#process wikidata data from sqlite db
import json
import sqlite3
import sys

saints_count = 0
conn_humans_db = sqlite3.connect('./wikidata_humans.db')
humans_cursor = conn_humans_db.cursor()

#cursor.execute('SELECT * FROM humans LIMIT %i,%i;', (1000,10))

conn_saints_db = sqlite3.connect('wikidata_saints.db')
saints_cursor = conn_saints_db.cursor()
saints_cursor.executescript('''DROP TABLE IF EXISTS saints; CREATE TABLE saints (id varchar(20), data json)''')

humans = humans_cursor.execute('SELECT * FROM humans;')
print("Query executed")


def parse_content(content_str :str)->dict:
    #if '"Q51621"' or '"P411"' in content_str:

    #if '"Q51621 in content_str"':
    #    print(content_str)
    #    if not '"P411"' in content_str:
    #        print(content_str)
    #        sys.exit()
    #if '"P411"' in content_str:
    #    print(content_str)
    #    if not '"Q51621"' in content_str:
    #        sys.exit()
    #    print(content_str)
    result_json = json.loads(content_str)
    return result_json

def json_has_saint_info(json_dict: dict)->bool:
    if 'P411' in json_dict['claims'].keys():
        return True
    return False

#
for idx,(id,content) in enumerate(humans):
    idx
    #print(id)
    #print(content)
    if idx%10000==0:
        print(f"At entry{idx}")
        print(f"{saints_count} saints so far...")
        conn_saints_db.commit()
    json_content = parse_content(content)
    if json_has_saint_info(json_content):
        #print("Found a saint!")
        #print("ID:", json_content['id'])
        saints_count += 1
        saints_cursor.execute("insert into saints values (?, ?)", [json_content['id'], json.dumps(json_content)])
        #do something with it
conn_saints_db.commit()
conn_saints_db.close()
conn_humans_db.close()