# Since every day of the year in Wikidata has it's own entry/id, we will try to build a dictionary of those days first

# Starting from January 1 / Q2150
from qwikidata.linked_data_interface import get_entity_dict_from_api
import calendar


def map_wikidata_calender(first_day_of_year_id: str) -> dict[str:str]:
    month_name_list = list(calendar.month_name)
    current_date_id = first_day_of_year_id

    wiki_id_date_dict = {}
    # Going through the gregorian calender year
    while True:
        # update date id
        date_dict = get_entity_dict_from_api(current_date_id)
        string_representation = date_dict['labels']['en']['value']
        print(current_date_id, ' : ', string_representation)

        date_split = string_representation.split()
        month = date_split[0]
        month_number = str(month_name_list.index(month))
        day = date_split[1]
        month_and_day = month_number + ";" + day
        wiki_id_date_dict[current_date_id] = month_and_day

        # P31 is "instance of" property, first element of that is assumed to be "point in time with respect to recurrent timeframe"
        # P156 is "followed by" property, which we use to get to the next date
        current_date_id = date_dict['claims']['P31'][0]['qualifiers']['P156'][0]['datavalue']['value']['id']

        if current_date_id == first_day_of_year_id:
            break

    return wiki_id_date_dict


def write_date_dict_to_file(wiki_id_date_dict: dict, file_name: str):
    with open(file_name, 'w') as f:
        string_to_write = ""
        for entry in wiki_id_date_dict:
            string_to_write += entry + ";" + wiki_id_date_dict[entry] + "\n"
        f.write(string_to_write)


#gregorian calendar starts with Q2150
gregorian_wiki_id_date_dict = map_wikidata_calender("Q2150")
write_date_dict_to_file(gregorian_wiki_id_date_dict, file_name="gregorian_wiki_date_mapping.txt")

#orthodox eastern liturgical calendar starts with Q13376314
orthodox_wiki_id_date_dict = map_wikidata_calender("Q13376314")
write_date_dict_to_file(orthodox_wiki_id_date_dict, file_name="orthodox_wiki_date_mapping.txt")
