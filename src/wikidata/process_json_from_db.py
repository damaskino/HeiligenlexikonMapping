import sqlite3
import json
import os

conn = sqlite3.connect('hundred_saints.db')
cursor = conn.cursor()
saints = cursor.execute('SELECT * from hundred_saints')


#keys in the json:
#https://doc.wikimedia.org/Wikibase/master/php/docs_topics_json.html
#type: the type of entry, should be either item or property
#id: the id of the entry
#labels: labels, i.e. the name of the entry in different languages
#descriptions: descriptions for the different languages
#aliases: different names for different languages, multiples for each language possible
#claims: this is where the "meat" is
# contains different statements about the object could be synonmous with claims it seems, most likely properties(?), i.e. "is saint", "is human"
# each statement consists of a mainsnak (who invents these words??) which is the value of the property it's associated with
# (think: Property "is a" has the value/snak "elefant")s and two optional lists of qualifier snaks and references
# a statement is always associated with a property (P<number of property>) and there can be multiple statements about the same property in an item
# e.g. the
#sitelinks: links to other sites describing the objects, usually wikipedia-sites only it seems


def parse_json_content(json_saint: dict):
    print(json_saint)
    wikidata_id = json_saint['id']
    labels = json_saint['labels']
    descriptions = json_saint['descriptions']
    aliases = json_saint['aliases']
    claims = json_saint['claims']
    sitelinks = json_saint['sitelinks']

    json_saint.keys()

#TODO: check how many have a birthdate available, and sort accordingly, could help in processing time

#Loads the entries from the heiligenlexikon for comparison with the wikidata entries from the database
def load_hlex_entries:
    pass


for id,content in saints:
    print(id)
    print(content)
    json_saint = json.loads(content)
    parse_json_content(json_saint)