import platform
import sys
import time
import sqlite3
import json

from qwikidata.entity import WikidataItem
from qwikidata.json_dump import WikidataJsonDump
from qwikidata.utils import dump_entities_to_json

# modified basic_json_dump example for extracting saints from wikidata dump

P_CANONIZATION = "P411"
Q_SAINT = "Q43115"
P_INSTANCE_OF = "P31"
Q_HUMAN = "Q5"

def has_canonization_status(item: WikidataItem, truthy: bool = True) -> bool:
    """Return True if the Wikidata Item has a canonization status."""
    if truthy:
        claim_group = item.get_truthy_claim_group(P_CANONIZATION)
    else:
        claim_group = item.get_claim_group(P_CANONIZATION)

    item.get

    occupation_qids = [
        claim.mainsnak.datavalue.value["id"]
        for claim in claim_group
        if claim.mainsnak.snaktype == "value"
    ]
    return Q_SAINT in occupation_qids

def is_human(item: WikidataItem, truthy: bool = True) -> bool:


    if truthy:
        claim_group = item.get_truthy_claim_group(P_INSTANCE_OF)
    else:
        claim_group = item.get_claim_group(P_INSTANCE_OF)

    occupation_qids = [
        claim.mainsnak.datavalue.value["id"]
        for claim in claim_group
        if claim.mainsnak.snaktype == "value"
    ]

    return Q_HUMAN in occupation_qids

# create an instance of WikidataJsonDump

#Workaround to deal with different dev setups
wjd_dump_path = ""
if platform.system()=="Windows":
    wjd_dump_path = "D:\\0-MasterData\\latest-all.json.gz"
else:
    wjd_dump_path = "/Users/chen/0-MasterData/latest-all.json.bz2"
wjd = WikidataJsonDump(wjd_dump_path)

#Set up the db connection and initial db
conn = sqlite3.connect('wikidata_humans.db')
cursor = conn.cursor()

cursor.executescript('''DROP TABLE IF EXISTS humans; CREATE TABLE humans (id varchar(20), data json)''')

human_count = 0
# create an iterable of WikidataItem representing humans

t1 = time.time()
for ii, entity_dict in enumerate(wjd):
    entity = entity_dict
    try:
        if entity_dict["type"] == "item":
            entity = WikidataItem(entity_dict)
            #if has_canonization_status(entity):
            if is_human(entity):
                human_count+=1
                cursor.execute("insert into humans values (?, ?)",[entity_dict['id'], json.dumps(entity_dict)])

                #humans.append(entity)
                #print(entity)

        if ii % 1000 == 0:
            conn.commit()
            t2 = time.time()
            dt = t2 - t1
            print(
                "found {} humans among {} entities [entities/s: {:.2f}]".format(
                    human_count, ii, ii / dt
                )
            )


        #if human_count > 1000:
        #    break

    except Exception as e:
        print(e)
        print("Exception at entity:", entity_dict)
        sys.exit()

conn.commit()
cursor.close()
conn.close()


