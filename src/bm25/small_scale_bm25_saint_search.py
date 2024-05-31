# generator
import json
import sqlite3
import math
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
        if not isinstance(hlex_feast_day, str):
            if math.isnan(hlex_feast_day):
                continue
        hlex_feast_day = str(hlex_feast_day)
        hlex_feast_day_split = hlex_feast_day.split(".")
        day = hlex_feast_day_split[0]
        month = hlex_feast_day_split[1]
        for wiki_feast_day in wikidata_feast_days:
            if len(wiki_feast_day) == 0:
                continue
            wiki_feast_day_split = wiki_feast_day.split(",")
            wiki_day = wiki_feast_day_split[1]
            wiki_month = wiki_feast_day_split[0]
            if day == wiki_day and month == wiki_month:
                return True
                break
    return False


def write_matches_to_file(matches: list):
    output_string = ""
    for entry_dict in matches:
        output_string += (
                ";".join(
                    [
                        entry_dict["HlexEntry"],
                        entry_dict["GoldStandardMatch"],
                        entry_dict["SystemMatch"],
                    ]
                )
                + "\n"
        )
    with open("match_results.txt", "w") as match_results_file:
        match_results_file.write(output_string)

def load_data()-> (list, pd.DataFrame):
    dev_set_list = load_hlex_dev_set_entries()
    print("Loading hlex data...")
    hlex_df = load_hlex_data()
    print("Hlex loaded!")
    return dev_set_list, hlex_df

#TODO: make use of parameters
def match_entries(dev_set_list, hlex_df, name_edit_distance_threshold=0, feast_day_tolerance=0):
    entry_matches = []
    for entry_to_map in dev_set_list:
        entry_split = entry_to_map.split(";")
        hlex_entry_id = entry_split[0]
        entry_gold_standard_wiki_match = entry_split[2].rstrip()

        # retrieve the info we have from hlex
        hlex_entry = hlex_df[hlex_entry_id]

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
        wikidata_saints = load_wikidata_data("../wikidata/processed_saints.db", "saints")
        for wiki_entry_id, wiki_namelist, wiki_feastlist in wikidata_saints:
            wiki_entry_id = wiki_entry_id.rstrip()
            print(wiki_entry_id)
            print(wiki_namelist)
            wiki_namelist = wiki_namelist.split(";")
            print(wiki_feastlist)
            wiki_feastlist = wiki_feastlist.split(";")

            # match names
            name_match_found, result = match_name(
                hlex_names=hlex_saint_names, wikidata_names=wiki_namelist
            )
            if name_match_found:
                print("Found name match!")
                print("Entry: ", hlex_entry_id, "->", wiki_entry_id)

            feast_match_found = match_feast_day(
                hlex_feast_days=hlex_feast_days, wikidata_feast_days=wiki_feastlist
            )
            if feast_match_found:
                print("Feast day match found!")
                print("Entry: ", hlex_entry_id, "->", wiki_entry_id)

            if feast_match_found and name_match_found:
                print("Found matching entry!")
                entry_matches.append(
                    {
                        "HlexEntry": hlex_entry_id,
                        "GoldStandardMatch": entry_gold_standard_wiki_match,
                        "SystemMatch": wiki_entry_id,
                    }
                )
                # sys.exit()
            # match_feast_day(hlex_feast_days=hlex_feast_day, wikidata_feast_days=wiki_feastlist)
            # match feast day(s)

    print(entry_matches)
    write_matches_to_file(entry_matches)
    # print(hlex_df)
    # corpus

if __name__ == '__main__':
    dev_set_list, hlex_df = load_data()
    #the naivest approach, if one name from hlex matches exactly with a name/alias/label in wikidata
    # *and* if either of the feast days match, consider this a match
    match_entries(dev_set_list=dev_set_list, hlex_df=hlex_df)
    match_entries(dev_set_list=dev_set_list, hlex_df=hlex_df, name_edit_distance_threshold=80, feast_day_tolerance=2)
    #slightly differentiated approach where