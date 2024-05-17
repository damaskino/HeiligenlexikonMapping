# generator
import json
import sqlite3

import pandas as pd


# Loads the entries from the heiligenlexikon for comparison with the wikidata entries from the database


def load_hlex_dev_set_entries():
    with open("../../data/2_annotated_data/dev_set.txt") as dev_set_file:
        return list(dev_set_file.readlines())


def load_hlex_data():
    hlex_data_df = pd.read_json("../../outputs_to_review/parsed_heiligenlexikon.json")
    return hlex_data_df


def load_wikidata_data(path_to_db: str, saints_table: str):
    saints_db = sqlite3.connect(path_to_db)
    saints_cursor = saints_db.cursor()

    saints_cursor.execute(f"SELECT * FROM {saints_table};")
    print("Query executed")
    return saints_cursor


def name_matching(hlex_names: list, wikidata_aliases: dict):
    wikidata_aliases = []
    for language in wikidata_aliases:
        for alias_for_lang in language:
            alias = alias_for_lang['value']
            wikidata_aliases.append()

    for name in hlex_names:
        for wiki_name in wikidata_aliases:
            if name == wiki_name:
                return True, name

    return False, "NA"


dev_set_list = load_hlex_dev_set_entries()
print("Loading hlex data...")
hlex_df = load_hlex_data()
print("Hlex loaded!")
for entry_to_map in dev_set_list:
    entry_split = entry_to_map.split(";")
    entry_id = entry_split[0]

    # retrieve the info we have from hlex
    hlex_entry = hlex_df[entry_id]

    saint_names = []
    hlex_saint_name = hlex_entry["SaintName"]
    saint_names.append(hlex_saint_name)

    hlex_canon_status = hlex_entry["CanonizationStatus"]
    hlex_gender = hlex_entry["Gender"]
    hlex_feast_day = hlex_entry["FeastDay0"]
    hlex_feast_day1 = hlex_entry["FeastDay1"]
    hlex_feast_day2 = hlex_entry["FeastDay2"]
    hlex_occupation = hlex_entry["Occupation"]
    hlex_aliases_list = hlex_entry["Aliases"]
    if len(hlex_aliases_list) > 0:
        saint_names += hlex_aliases_list

        # for alias in hlex_aliases_list:
        #    print(alias)
    # match the info from hlex to wikidata

    # needs to be done everytime unfortunately because the cursor needs to be reset everytime
    wikidata_saints = load_wikidata_data(
        "../wikidata/hundred_saints.db", "hundred_saints"
    )
    for entry_id, content in wikidata_saints:
        json_saint = json.loads(content)

        # Matching names/aliases
        wikidata_aliases_dict = json_saint['aliases']
        name_matching(saint_names, wikidata_aliases_dict)

        # Matching Feast day(s)
        feast_day_wiki_data_id = ""
        if 'P841' in json_saint['claims']:
            feast_day_wiki_data_id = json_saint['claims']['P841'][0]['mainsnak']['datavalue']['value']['id']
            # TODO this assumes that the mainsnak is always first and that it contains the feast day, need to account for multiple snaks

        # TODO need to convert the wikidata_id of the day to an actual date
        feast_day_wiki_date = ""
print(hlex_df)
# corpus
