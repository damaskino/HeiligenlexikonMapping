# generator
import json
import os
import sqlite3
import math
import pandas as pd
import datetime
from thefuzz import fuzz


import sys


# Loads the entries from the heiligenlexikon for comparison with the wikidata entries from the database


def load_hlex_gold_set_entries():
    gold_data_set_df = pd.read_csv("../../data/2_annotated_data_gold_and_dev/gold_standard_hand_annotated_eschbach_li_no_comments.csv", sep=";")
    return gold_data_set_df


def load_hlex_data():
    hlex_data_df = pd.read_json("../../outputs_to_review/parsed_heiligenlexikon.json")
    return hlex_data_df


def load_wikidata_data(path_to_db: str, saints_table: str):
    saints_db = sqlite3.connect(path_to_db)
    saints_cursor = saints_db.cursor()

    saints_cursor.execute(f"SELECT * FROM {saints_table};")
    # print("Query executed")
    return saints_cursor


def match_name(
        hlex_names: list, wikidata_names: list, edit_distance_threshold: int = 0
):
    for name in hlex_names:
        for wiki_name in wikidata_names:
            if (
                    name == wiki_name
                    or fuzz.ratio(name, wiki_name) > edit_distance_threshold
            ):
                return True, name
                break

    return False, "NA"


# Calculate the day distance between two dates, using 1804 as an arbitrarily picked leap year that
# still allows for february 29th to exist if necessary.


def calculate_feast_day_distance(
        hlex_day: int, hlex_month: int, wiki_day: int, wiki_month
):
    reference_year = 1804
    hlex_date = datetime.date(year=reference_year, month=hlex_month, day=hlex_day)
    wiki_date = datetime.date(year=reference_year, month=wiki_month, day=wiki_day)

    hlex_wiki_delta = hlex_date - wiki_date
    days_delta = abs(hlex_wiki_delta.days)
    return days_delta


def match_feast_day(
        hlex_feast_days: list, wikidata_feast_days: list, feast_day_tolerance: int = 0
):
    for hlex_feast_day in hlex_feast_days:
        if not isinstance(hlex_feast_day, str):
            if math.isnan(hlex_feast_day):
                continue
        hlex_feast_day = str(hlex_feast_day)
        hlex_feast_day_split = hlex_feast_day.split(".")
        hlex_day = int(hlex_feast_day_split[0])
        hlex_month = int(hlex_feast_day_split[1])
        # TODO: Workarounds, remove when respective entries are fixed in extraction

        if hlex_month > 12 or hlex_month < 1:
            print("INVALID MONTH: ", hlex_month)
            continue
        if hlex_day > 31:
            print("INVALID DAY: ", hlex_day)
            continue

        if hlex_month==6 and hlex_day ==31:
            continue
        if hlex_day==0:
            continue


        for wiki_feast_day in wikidata_feast_days:
            if len(wiki_feast_day) == 0:
                continue
            wiki_feast_day_split = wiki_feast_day.split(",")
            wiki_day = int(wiki_feast_day_split[1])
            wiki_month = int(wiki_feast_day_split[0])
            days_delta = calculate_feast_day_distance(
                hlex_day=hlex_day,
                hlex_month=hlex_month,
                wiki_day=wiki_day,
                wiki_month=wiki_month,
            )
            if days_delta <= feast_day_tolerance:
                return True
                break
    return False


def write_matches_to_file(
        matches: list, edit_distance_threshold=100, feast_day_tolerance=0, dev_flag=True
):
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

    file_name_base = "match_results"
    edit_distance_string = "edit_dist_thresh_" + str(edit_distance_threshold)
    feast_day_tolerance = "feast_tolerance_" + str(feast_day_tolerance)
    file_ending = "_on_gold.csv"
    file_name_full = (
            "_".join([file_name_base, edit_distance_string, feast_day_tolerance])
            + file_ending
    )
    target_folder = "matching_results"
    full_path = os.path.join(target_folder, file_name_full)
    with open(full_path, "w") as match_results_file:
        match_results_file.write(output_string)


def load_data() -> (list, pd.DataFrame):
    gold_set_df = load_hlex_gold_set_entries()
    print("Loading hlex data...")
    hlex_df = load_hlex_data()
    print("Hlex loaded!")
    return gold_set_df, hlex_df


# If only one name matches don't consider feast days, if multiple name matches found, look at feast days
def match_entries(
        gold_set_df,
        hlex_df,
        name_edit_distance_threshold=100,
        feast_day_tolerance=0,
):

    entries_to_match = list(gold_set_df["HeiligenLexikonID"])
    entry_matches = []
    for idx, entry_to_map in enumerate(entries_to_match):
        entry_split = entry_to_map.split(";")
        hlex_entry_id = entry_split[0]

        gold_data_series_item = gold_set_df.loc[gold_set_df['HeiligenLexikonID']==hlex_entry_id]
        gold_match_series_item = gold_data_series_item['GoldWikidataID']
        gold_match_series_item = list(gold_match_series_item)[0]
        entry_gold_standard_wiki_match=""
        print("Extracting Entry value...")
        print(f"At entry: {idx} with id: {hlex_entry_id}")
        if type(gold_match_series_item)==str:
            entry_gold_standard_wiki_match=gold_match_series_item


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
        if not isinstance(hlex_aliases_list, list):
            hlex_aliases_list = []

        if len(hlex_aliases_list) > 0:
            hlex_saint_names += hlex_aliases_list

        # Account for multiple name matches across wiki entries,
        # highly likely in cases where the saint name is common (e.g. Peter)
        # If there is more than one name match, we take the feast day as an additional distinguishing feature
        name_matches = []
        feast_matches = []
        system_match = ""
        # for alias in hlex_aliases_list:
        #    print(alias)
        # match the info from hlex to wikidata

        # needs to be done everytime unfortunately because the cursor needs to be reset everytime
        wikidata_saints = load_wikidata_data(
            "../preprocessing/wikidata/processed_saints.db", "saints"
        )
        for wiki_saint_tuple in wikidata_saints:

            wiki_entry_id = wiki_saint_tuple[0]
            wiki_namelist = wiki_saint_tuple[1]
            wiki_feastlist = wiki_saint_tuple[2]
            wiki_entry_id = wiki_entry_id.rstrip()
            # print(wiki_entry_id)
            # print(wiki_namelist)
            wiki_namelist = wiki_namelist.split(";")
            # print(wiki_feastlist)
            wiki_feastlist = wiki_feastlist.split(";")

            # match names
            # NOTE: currently only considers the first found match and does not look further if a match is found
            name_match_found, result = match_name(
                hlex_names=hlex_saint_names,
                wikidata_names=wiki_namelist,
                edit_distance_threshold=name_edit_distance_threshold,
            )
            if name_match_found:
                # print("Found name match!")
                # print("Entry: ", hlex_entry_id, "->", wiki_entry_id)
                name_matches.append(wiki_entry_id)

                # NOTE: currently only considers the first found match and does not look further if a match is found
                # ONLY consider feast days if the name was a match
                feast_match_found = match_feast_day(
                    hlex_feast_days=hlex_feast_days, wikidata_feast_days=wiki_feastlist
                )
                if feast_match_found:
                    print("Feast day match found!")
                    # print("Entry: ", hlex_entry_id, "->", wiki_entry_id)
                    feast_matches.append(wiki_entry_id)

        # Gone through all wiki entries for this hlex entry, now we tally up the matching results
        if len(name_matches) == 1:
            if name_matches[0] in feast_matches:
                system_match = name_matches[0]
        elif len(name_matches) > 1:
            for candidate_entry in name_matches:
                if candidate_entry in feast_matches:
                    system_match = candidate_entry
                    # TODO only checks for first matching feast day atm, might consider adding more feast days
                    # and give higher priority to wiki entries when multiple feast days match for the same entry
                    break
        entry_matches.append(
            {
                "HlexEntry": hlex_entry_id,
                "GoldStandardMatch": entry_gold_standard_wiki_match,
                "SystemMatch": system_match,
            }
        )

    # print(entry_matches)
    write_matches_to_file(
        entry_matches, name_edit_distance_threshold, feast_day_tolerance
    )
    # print(hlex_df)
    # corpus


if __name__ == "__main__":
    gold_set_df, hlex_df = load_data()
    # the naivest approach, if one name from hlex matches exactly with a name/alias/label in wikidata
    # *and* if either of the feast days match, consider this a match
    match_entries(gold_set_df=gold_set_df, hlex_df=hlex_df, name_edit_distance_threshold=70)
    sys.exit()
    match_entries(entries_to_match=gold_set_df, hlex_df=hlex_df, dev_flag=False)
    match_entries(entries_to_match=gold_set_df, hlex_df=hlex_df)
    # Using edit distance: as long as a name is similar enough to pass an edit distance threshold, it is considered to be a name match
    # Feast day tolerance: allow the feast days between hlex and wiki entries to diverge within a fixed number of days
    match_entries(
        entries_to_match=gold_set_df, hlex_df=hlex_df, name_edit_distance_threshold=90
    )
    match_entries(
        entries_to_match=gold_set_df,
        hlex_df=hlex_df,
        name_edit_distance_threshold=80,
        feast_day_tolerance=0,
    )
    match_entries(
        entries_to_match=gold_set_df,
        hlex_df=hlex_df,
        name_edit_distance_threshold=80,
        feast_day_tolerance=2,
    )
    match_entries(
        entries_to_match=gold_set_df,
        hlex_df=hlex_df,
        name_edit_distance_threshold=80,
        feast_day_tolerance=7,
    )
    match_entries(
        entries_to_match=gold_set_df,
        hlex_df=hlex_df,
        name_edit_distance_threshold=70,
        feast_day_tolerance=0,
    )
    match_entries(
        entries_to_match=gold_set_df,
        hlex_df=hlex_df,
        name_edit_distance_threshold=70,
        feast_day_tolerance=2,
    )
    match_entries(
        entries_to_match=gold_set_df,
        hlex_df=hlex_df,
        name_edit_distance_threshold=70,
        feast_day_tolerance=5,
    )
    match_entries(
        entries_to_match=gold_set_df,
        hlex_df=hlex_df,
        name_edit_distance_threshold=70,
        feast_day_tolerance=10,
    )
