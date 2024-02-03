import json

from qwikidata.json_dump import WikidataJsonDump
from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api


def load_wikidata_from_dump(wikidata_ids):
    wjd_dump_path = "D:\\0-MasterData\\latest-all.json.gz"
    wjd = WikidataJsonDump(wjd_dump_path)
    entity_list = []
    for ii, entity_dict in enumerate(wjd):
        if ii % 1000 == 0:
            print(f"At {ii} ")
        entity = entity_dict
        if entity["id"] in wikidata_ids:
            entity_list.append(entity)
            print(entity["id"])
            wikidata_ids.remove(entity["id"])
            if len(wikidata_ids) == 0:
                break

    json_data = json.dumps(entity_list)
    return json_data


def load_wikidata_from_web(wikidata_ids):
    entity_list = []
    for wiki_data_id in wikidata_ids:
        entity_dict = get_entity_dict_from_api(wiki_data_id)
        wiki_item = WikidataItem(entity_dict)
        print(wiki_item)
        entity_list.append(entity_dict)
    json_data = json.dumps(entity_list)
    return json_data
    ## create a property representing "subclass of"
    # P_SUBCLASS_OF = "P279"
    # p279_dict = get_entity_dict_from_api(P_SUBCLASS_OF)
    # p279 = WikidataProperty(p279_dict)

    # create a lexeme representing "bank"
    # L_BANK = "L3354"
    # l3354_dict = get_entity_dict_from_api(L_BANK)
    # l3354 = WikidataLexeme(l3354_dict)


def split_gold_standard_line(line: str):
    print("Splitting: ", line)
    line = line.strip()
    entry = line.split(";")
    print(entry)

    hlex_id = entry[0]
    wikipedia_link = entry[1]
    wikidata_id = entry[2]
    return hlex_id, wikipedia_link, wikidata_id


gold_standard = None
h_lex = None
# parse goldstandard
with open("../../resources/gold_standard_hand_annotated_eschbach_li.txt") as f:
    gold_standard = f.readlines()

with open("../../outputs_to_review/parsed_heiligenlexikon.json") as f:
    hlex = json.loads(f.read())

gold_standard_entries = []
wikidata_ids_for_retrieval = []
for line in gold_standard:
    if "#" in line or len(line.strip()) == 0:
        continue
        # TODO handle lines with # that we want to keep!
    hlex_id, wikipedia_link, wikidata_id = split_gold_standard_line(line)

    if wikidata_id:
        wikidata_ids_for_retrieval.append(wikidata_id)
    # load entry from hlex
    hlex_entry = hlex[hlex_id]
    entry_text = hlex_entry[
        "OriginalText"
    ]  # TODO: only get the first paragraph in case we don't already?
    gold_standard_entries.append((hlex_id, wikipedia_link, wikidata_id, entry_text))

# for entry in gold_standard_entries:
# load entry from wikidata


# create an iterable of WikidataItem representing saints

# json_data = load_wikidata_from_dump(wikidata_ids_for_retrieval)
json_data = load_wikidata_from_web(wikidata_ids_for_retrieval)

#
with open(
        "../../outputs_to_review/wikidata_gold_standard_entries.json", "w"
) as json_file:
    json_file.write(json_data)

# put entries next to each other in resulting json
