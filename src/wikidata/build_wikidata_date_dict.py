# Since every day of the year in Wikidata has it's own entry/id, we will try to build a dictionary of those days first

# Starting from January 1 / Q2150
from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api

# P31 instance of, point in time with respect to current time frame, P156 followed by, i.e. "the day after that is..."

january1st_id = "Q2150"
current_date_id = january1st_id

wiki_id_date_dict = {}
while True:
    # update date id
    date_dict = get_entity_dict_from_api(current_date_id)
    current_date_id = date_dict['claims']['P31'][0]['qualifiers']['P156'][0]['datavalue']['value']['id']
    string_representation = date_dict['labels']['en']['value']

    wiki_id_date_dict[current_date_id] = string_representation
    print(current_date_id)
    if current_date_id == january1st_id:
        break

with open('date_wikidata_id_mapping.txt', 'w') as f:
    string_to_write = ""
    for entry in wiki_id_date_dict:
        string_to_write += entry + ";" + wiki_id_date_dict[entry] + "\n"
    f.write(string_to_write)
