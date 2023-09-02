import json

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
    "Dec": "12."
}


def resolve_multiple_dates():
    pass


def convert_date(raw_date: str):
    raw_date = raw_date.replace("(", "")
    raw_date = raw_date.replace(")", "")
    for item in german_date_dict:
        raw_date = raw_date.replace(item, german_date_dict[item])
    for item in second_pass_german_date_dict:
        raw_date = raw_date.replace(item, second_pass_german_date_dict[item])

    if "al" in raw_date:
        raw_date_al_split = raw_date.split("al")
        # if len(raw_date_al_split)>1:
        #    print(raw_date_al_split)
        #    print(raw_date)
        #    print(raw_date_al_split[0])
    elif "u." in raw_date:
        raw_date_u_split = raw_date.split("u.")
        print(raw_date_u_split)
        first = raw_date_u_split[0]
        rest = raw_date_u_split[1:]
        print("First: ", first)
        print("Rest: ", rest)
        print("\n")
    elif "et" in raw_date:
        raw_date_et_split = raw_date.split("et")
    elif "," in raw_date:
        raw_date_comma_split = raw_date.split(",")
    elif "und" in raw_date:
        raw_date_und_split = raw_date.split("und")
    else:
        # if none of the other apply, it should be a single date
        raw_date
        parsed_single_date = raw_date.replace("..", ".")
        # print(parsed_single_date)
        return [parsed_single_date]


# TODO write test that checks if all dates conform to the same format at the end

with open(r"../outputs_to_review/parsed_heiligenlexikon.json") as json_file:
    json_data = json.load(json_file)
    for item in json_data:
        # print(item)
        raw_input_date = json_data[item]["FeastDay"]
        if raw_input_date is not None:
            convert_date(raw_input_date)
