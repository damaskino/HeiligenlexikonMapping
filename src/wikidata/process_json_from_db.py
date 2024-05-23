import sqlite3
import json
import os
import sys

from src.wikidata.wikidata_day_dict import wikidata_misc_day_dict
from wikidata_day_dict import wikidata_general_day_dict, wikidata_orthodox_day_dict

# conn = sqlite3.connect('hundred_saints.db')
# cursor = conn.cursor()
# saints = cursor.execute('SELECT * from hundred_saints')
conn = sqlite3.connect('wikidata_saints.db')
cursor = conn.cursor()
saints = cursor.execute('SELECT * from saints')


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
    # we skip these ids because they appear in the feast days section but don't actually refer to a date
    # They're also marked as potentially having issues in wikidata, so most likely an annoation error
    # Q1841: Catholicism
    # Q35032: Eastern Orthodox Church
    # Q9592: Catholic Church
    # Q365695: Holy Translators
    # Q2387117: Bright Week --> Potentially mappable to days?
    # Q18726: 1933
    # Q3333484: Eastern Orthodoxy
    # Q11184: Julian Calendar
    # Q17414321: Abdons Day, commemorates persian martyr abdon most likely noise/malformed
    # Q115801525: Thout 1, first day of the coptic calendar -> mappable/usable?
    # Q12966185: May 5th 2012
    # Q20830799: First sunday in August -> usable?
    # Q123: September (The month) -> usable?
    # Q731505: Paopi, Second Month of the Coptic Calendar -> usable?
    feast_day_ids_to_skip = ["Q1841", "Q35032", "Q9592", "Q3464625", "Q2387117", "Q18726", "Q3333484", "Q11184",
                             "Q17414321", "Q115801525", "Q12966185", "Q20830799", "Q123", "Q731505"]

    if 'P841' in claims_dict:
        feast_day_list = claims_dict['P841']
        for feast_day_item in feast_day_list:
            # Check needed because some noisy items have "unknown value"
            if 'datavalue' in feast_day_item['mainsnak']:
                feast_day_wikidata_id = feast_day_item['mainsnak']['datavalue']['value']['id']
            else:
                continue

            date_split = []

            # TODO: this ID is causing problems
            # TODO regenerate calendar mappings with proper indexing
            if feast_day_wikidata_id in feast_day_ids_to_skip:
                # print(claims_dict)
                continue

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
            day = date_split[0]
            month = date_split[1]
            print(day)
            print(month)

            # TODO account for eastern orthodox calendar dates like
            # Q16851085
            # map the date id to an actual date
        # could be multiple feast days, so would have to unpack those separately


def parse_json_content(json_saint: dict):
    # print(json_saint)
    # print(json_saint['labels'])
    wikidata_id = json_saint['id']
    labels = json_saint['labels']
    descriptions = json_saint['descriptions']
    aliases = json_saint['aliases']
    claims = json_saint['claims']
    feast_day = get_feast_days(claims)

    sitelinks = json_saint['sitelinks']

    json_saint.keys()


# TODO: check how many have a birthdate available, and sort accordingly, could help in processing time

# Loads the entries from the heiligenlexikon for comparison with the wikidata entries from the database
def load_hlex_entries():
    pass


for index, (id, content) in enumerate(saints):
    # print(id)
    # print(content)
    print("Entry: ", index)
    print("EntryID: ", id)
    json_saint = json.loads(content)
    parse_json_content(json_saint)
