import time

from qwikidata.entity import WikidataItem
from qwikidata.json_dump import WikidataJsonDump
from qwikidata.utils import dump_entities_to_json

# modified basic_json_dump example for extracting saints from wikidata dump

P_CANONIZATION = "P411"
Q_SAINT = "Q43115"


def has_canonization_status(item: WikidataItem, truthy: bool = True) -> bool:
    """Return True if the Wikidata Item has a canonization status."""
    if truthy:
        claim_group = item.get_truthy_claim_group(P_CANONIZATION)
    else:
        claim_group = item.get_claim_group(P_CANONIZATION)

    occupation_qids = [
        claim.mainsnak.datavalue.value["id"]
        for claim in claim_group
        if claim.mainsnak.snaktype == "value"
    ]
    return Q_SAINT in occupation_qids


# create an instance of WikidataJsonDump
wjd_dump_path = "D:\\0-MasterData\\latest-all.json.gz"
wjd = WikidataJsonDump(wjd_dump_path)

# create an iterable of WikidataItem representing saints
saints = []
t1 = time.time()
for ii, entity_dict in enumerate(wjd):
    entity = entity_dict
    try:
        if entity_dict["type"] == "item":
            entity = WikidataItem(entity_dict)
            if has_canonization_status(entity):
                saints.append(entity)
                print(entity)

        if ii % 1000 == 0:
            t2 = time.time()
            dt = t2 - t1
            print(
                "found {} saints among {} entities [entities/s: {:.2f}]".format(
                    len(saints), ii, ii / dt
                )
            )

        if len(saints) > 10000:
            break
    except Exception:
        print("Exception at entity:", entity_dict)

# write the iterable of WikidataItem to disk as JSON
out_fname = "filtered_entities.json"
print("Dumping to Json...")
dump_entities_to_json(saints, out_fname)

# wjd_filtered = WikidataJsonDump(out_fname)

# load filtered entities and create instances of WikidataItem
# for ii, entity_dict in enumerate(wjd_filtered):
#    item = WikidataItem(entity_dict)
