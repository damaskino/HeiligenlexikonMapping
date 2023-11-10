import json
import re
from typing import List

german_date_dict = {
    "Jan.": "01.",
    "Jau.": "01.",
    "Januar": "01.",
    "Feb.": "02.",
    "Febr.": "02.",
    "Februar": "02.",
    "Fedr.": "02.",
    "Fébé.": "02.",
    "Fehx.": "02.",
    "März": "03.",
    "Mäcz": "03.",
    "Mäxz": "03.",
    "Apr.": "04.",
    "April": "04.",
    "Mai": "05.",
    "Jun.": "06.",
    "Juni": "06.",
    "Jul.": "07.",
    "Juli": "07.",
    "Aug.": "08.",
    "Ang.": "08.",
    "August": "08.",
    "September": "09.",
    "Sept.": "09.",
    "October": "10.",
    "Oct.": "10.",
    "Okt.": "10.",
    "Nov.": "11.",
    "Novemb.": "11.",
    "November": "11.",
    "Rov.": "11.",
    "Dec.": "12.",
    "Dee.": "12.",
    "Dez.": "12.",
}

second_pass_german_date_dict = {
    "Febr": "02",
    "Feb": "02.",
    "Mal": "05.",
    "Aug": "08.",
    "Sept": "09.",
    "Oct": "10",
    "Nov": "11.",
    "Dec": "12.",
}

connectives = ["al", "u.", ",", "et", "und"]


def split_date_into_day_and_month(date_string: str):
    date_pattern = r"([0-9]+)"
    date_matches = re.findall(date_pattern, date_string)

    day = date_matches[0]
    month = None

    if len(date_matches) > 1:
        month = date_matches[1]
    return day, month


def resolve_multiple_dates(raw_date: str) -> List:
    for connective in connectives:
        if connective in raw_date:
            result = []
            raw_date_al_split = raw_date.split(connective)
            first_date = raw_date_al_split[0].strip()
            first_day, first_month = split_date_into_day_and_month(first_date)

            second_day = None
            second_month = None

            second_date = raw_date_al_split[1].strip()
            if len(second_date) > 0:
                second_day, second_month = split_date_into_day_and_month(second_date)

            if first_month == None and second_month != None:
                first_month = second_month

            result.append({'Day': int(first_day), 'Month': int(first_month)})

            if second_day != None and second_month != None:
                result.append({'Day': int(second_day), 'Month': int(second_month)})

            if len(raw_date_al_split) > 2:
                third_date = raw_date_al_split[2].strip()
                third_day, third_month = split_date_into_day_and_month(third_date)
                result.append({'Day': int(third_day), 'Month': int(third_month)})

            return result


def convert_date(raw_date: str):
    result_dates = []
    raw_date = raw_date.replace("(", "")
    raw_date = raw_date.replace(")", "")

    # Replace string representations of months with numbers
    for item in german_date_dict:
        raw_date = raw_date.replace(item, german_date_dict[item])
    for item in second_pass_german_date_dict:
        raw_date = raw_date.replace(item, second_pass_german_date_dict[item])

    if any(connective in raw_date for connective in connectives):
        result_dates = resolve_multiple_dates(raw_date)
    else:
        day, month = split_date_into_day_and_month(raw_date)
        result_dates.append({'Day': int(day), 'Month': int(month)})
    return result_dates


# TODO write test that checks if all dates conform to the same format at the end

if __name__ == "__main__":
    with open(r"../outputs_to_review/parsed_heiligenlexikon.json") as json_file:
        json_data = json.load(json_file)
        for item in json_data:
            # print(item)
            raw_input_date = json_data[item]["FeastDay"]
            if raw_input_date is not None:
                convert_date(raw_input_date)
