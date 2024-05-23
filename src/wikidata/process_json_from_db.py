import sqlite3
import json
import os
import sys

from src.wikidata.wikidata_day_dict import wikidata_misc_day_dict, feast_day_ids_to_skip
from wikidata_day_dict import wikidata_general_day_dict, wikidata_orthodox_day_dict



# keys in the json:
# https://doc.wikimedia.org/Wikibase/master/php/docs_topics_json.html
# type: the type of entry, should be either item or property
# id: the id of the entry
# labels: labels, i.e. the name of the entry in different languages
# descriptions: descriptions for the different languages
# aliases: different names for different languages, multiples for each language possible
# claims: this is where the "meat" is
# contains different statements about the object could be synonmous with claims it seems, most likely properties(?), i.e. "is saint", "is human"
# each statement consists of a mainsnak (who invents these words??) which is the value of the property it's associated with
# (think: Property "is a" has the value/snak "elefant")s and two optional lists of qualifier snaks and references
# a statement is always associated with a property (P<number of property>) and there can be multiple statements about the same property in an item
# e.g. the
# sitelinks: links to other sites describing the objects, usually wikipedia-sites only it seems


def parse_date(date_string: str):
    date_string = date_string.split()
    month = date_string[0]
    day = date_string[1]


def get_feast_days(claims_dict: dict):

    result_feast_days = []

    if 'P841' in claims_dict:
        feast_day_list = claims_dict['P841']
        for feast_day_item in feast_day_list:

            # Check needed because some noisy items have "unknown value"
            if 'datavalue' in feast_day_item['mainsnak']:
                feast_day_wikidata_id = feast_day_item['mainsnak']['datavalue']['value']['id']
            else:
                continue

            if feast_day_wikidata_id in feast_day_ids_to_skip:
                continue

            date_split = []

            if feast_day_wikidata_id in wikidata_general_day_dict:
                date_split = wikidata_general_day_dict[feast_day_wikidata_id].split(',')
            if feast_day_wikidata_id in wikidata_orthodox_day_dict:
                date_split = wikidata_orthodox_day_dict[feast_day_wikidata_id].split(',')
            if feast_day_wikidata_id in wikidata_misc_day_dict:
                date_split = wikidata_misc_day_dict[feast_day_wikidata_id].split(',')

            if len(date_split) == 0:
                print("Date not found in gregorian or julian calendar")
                print(feast_day_wikidata_id)
                sys.exit()
            month = date_split[0]
            day = date_split[1]

            result_feast_days.append((month,day))
        return result_feast_days


def parse_json_content(json_saint: dict):
    # print(json_saint)
    # print(json_saint['labels'])
    wikidata_id = json_saint['id']
    labels = json_saint['labels']
    descriptions = json_saint['descriptions']
    aliases = json_saint['aliases']
    claims = json_saint['claims']
    feast_days = get_feast_days(claims)
    print(feast_days)
    sitelinks = json_saint['sitelinks']

    json_saint.keys()


# TODO: check how many have a birthdate available, and sort accordingly, could help in processing time

# Loads the entries from the heiligenlexikon for comparison with the wikidata entries from the database
def load_hlex_entries():
    pass


if '__name__' == '__main__':

    # conn = sqlite3.connect('hundred_saints.db')
    # cursor = conn.cursor()
    # saints = cursor.execute('SELECT * from hundred_saints')
    conn = sqlite3.connect('wikidata_saints.db')
    cursor = conn.cursor()
    saints = cursor.execute('SELECT * from saints')

    for index, (id, content) in enumerate(saints):
        # print(id)
        # print(content)
        print("Entry: ", index)
        print("EntryID: ", id)
        json_saint = json.loads(content)
        parse_json_content(json_saint)
