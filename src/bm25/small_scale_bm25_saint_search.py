# generator
import json
import sqlite3

import pandas as pd
import sys


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


def match_name(hlex_names: list, wikidata_names: list):
    for name in hlex_names:
        for wiki_name in wikidata_names:
            if name == wiki_name:
                return True, name
                break

    return False, "NA"

def match_feast_day(hlex_feast_days: list, wikidata_feast_days: list):
    for hlex_feast_day in hlex_feast_days:
        if hlex_feast_day == None:
            continue
        hlex_feast_day = str(hlex_feast_day)
        hlex_feast_day_split = hlex_feast_day.split('.')
        day = hlex_feast_day_split[0]
        month = hlex_feast_day_split[1]
        for wiki_feast_day in wikidata_feast_days:
            if len(wiki_feast_day)==0:
                continue
            wiki_feast_day_split = wiki_feast_day.split(',')
            wiki_day = wiki_feast_day_split[1]
            wiki_month = wiki_feast_day_split[0]
            if day == wiki_day and month == wiki_month:
                return True
                break
    return False

dev_set_list = load_hlex_dev_set_entries()
print("Loading hlex data...")
hlex_df = load_hlex_data()
print("Hlex loaded!")
for entry_to_map in dev_set_list:
    entry_split = entry_to_map.split(";")
    entry_id = entry_split[0]

    # retrieve the info we have from hlex
    hlex_entry = hlex_df[entry_id]

    hlex_saint_names = []
    hlex_saint_name = hlex_entry["SaintName"]
    hlex_saint_names.append(hlex_saint_name)

    hlex_canon_status = hlex_entry["CanonizationStatus"]
    hlex_gender = hlex_entry["Gender"]

    hlex_feast_days = []
    hlex_feast_day = hlex_entry["FeastDay0"]
    if hlex_feast_day:
        hlex_feast_days.append(hlex_feast_day)
    hlex_feast_day1 = hlex_entry["FeastDay1"]
    if hlex_feast_day1:
        hlex_feast_days.append(hlex_feast_day1)
    hlex_feast_day2 = hlex_entry["FeastDay2"]
    if hlex_feast_day2:
        hlex_feast_days.append(hlex_feast_day2)
    hlex_occupation = hlex_entry["Occupation"]
    hlex_aliases_list = hlex_entry["Aliases"]
    if len(hlex_aliases_list) > 0:
        hlex_saint_names += hlex_aliases_list

        # for alias in hlex_aliases_list:
        #    print(alias)
    # match the info from hlex to wikidata

    # needs to be done everytime unfortunately because the cursor needs to be reset everytime
    wikidata_saints = load_wikidata_data(
        "../wikidata/processed_saints.db", "saints"
    )
    for entry_id, wiki_namelist, wiki_feastlist in wikidata_saints:
        print(entry_id)
        print(wiki_namelist)
        wiki_namelist = wiki_namelist.split(';')
        print(wiki_feastlist)
        wiki_feastlist = wiki_feastlist.split(';')

        #match names
        name_match_found, result = match_name(hlex_names=hlex_saint_names, wikidata_names=wiki_namelist)
        if name_match_found:
            print("Found name match!")
            print("Entry: ", entry_id)

        feast_match_found = match_feast_day(hlex_feast_days=hlex_feast_days, wikidata_feast_days=wiki_feastlist)
        if feast_match_found:
            print("Feast day match found!")
            print("Entry: ", entry_id)

        if feast_match_found and name_match_found:
            print("Found matching entry!")
            sys.exit()
        #match_feast_day(hlex_feast_days=hlex_feast_day, wikidata_feast_days=wiki_feastlist)
        #match feast day(s)


print(hlex_df)
# corpus
