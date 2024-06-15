import platform
import time

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

# create an iterable of WikidataItem representing humans
humans = []
t1 = time.time()
for ii, entity_dict in enumerate(wjd):
    entity = entity_dict
    try:
        if entity_dict["type"] == "item":
            entity = WikidataItem(entity_dict)
            #if has_canonization_status(entity):
            if is_human(entity):
                humans.append(entity)
                #print(entity)

        if ii % 1000 == 0:
            t2 = time.time()
            dt = t2 - t1
            print(
                "found {} humans among {} entities [entities/s: {:.2f}]".format(
                    len(humans), ii, ii / dt
                )
            )

        if len(humans) > 10000:
            break
    except Exception:
        print("Exception at entity:", entity_dict)

# write the iterable of WikidataItem to disk as JSON
out_fname = "filtered_entities.json"
print("Dumping to Json...")
dump_entities_to_json(humans, out_fname)


