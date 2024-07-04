# basically: if a number is accompanied by either month we know the date, if there is an al or et or comma between that, we can
# assume that the date is referring to the month after date. So essentially search from left to right, while remembering the days
# when we find the month, the days before that can be added to the month.
import pandas as pd
import sys
from src.post_processing.data_validation import is_valid_date
from src.preprocessing.heiligenlexikon.parse_dates import german_date_dict

date_exceptions = {"31.06.": "30.06."}


def parse_cleaned_date_item(date_item: list):
    days = []
    for item in date_item:

        if item.isdigit():
            if item == "36":
                days.append("30")
            elif item == "2324":
                days.append("23")
                days.append("24")
            elif item == "124":
                days.append("24")
            elif item == "51":
                days.append("5")
            else:
                days.append(item)
        else:
            month = german_date_dict[item]
            for day in days:

                date = day + "." + month

                if date in date_exceptions:
                    date = date_exceptions[date]
                if is_valid_date(date):
                    print(date)
                else:
                    print("Invalid Date found!")
                    print(date)

            days = []


faulty_entries_df = pd.read_csv(
    "faulty_date_entries.csv", sep=";", encoding="utf-8", header=None
)
faulty_entries_series = faulty_entries_df[1]
# print(faulty_entries_df)
for idx, item in faulty_entries_series.items():
    item = item.lstrip("(")
    item = item.rstrip(")")
    item = item.replace(".", "")
    item = item.replace(",", "")
    item_split = item.split(" ")
    # print(item_split)

    terms_to_filter = ["al", "u", "et", "und", "", "etc"]

    filtered_split = list(filter(lambda item: item not in terms_to_filter, item_split))

    print(filtered_split)
    parse_cleaned_date_item(filtered_split)

# print(faulty_entries_df[1])
