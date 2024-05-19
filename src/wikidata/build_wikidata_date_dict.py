# Since every day of the year in Wikidata has it's own entry/id, we will try to build a dictionary of those days first

# Starting from January 1 / Q2150
from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api

# P31 instance of, point in time with respect to current time frame, P156 followed by, i.e. "the day after that is..."

current_date_id = "Q2150"

while True:
    # update date id
    date_dict = get_entity_dict_from_api(current_date_id)
    current_date_id = date_dict['claims']['P31'][0]['qualifiers']['P156'][0]['datavalue']['value']['id']
    print(date_dict['labels']['en']['value'])
    print(current_date_id)
