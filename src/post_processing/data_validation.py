import pandas as pd
import datetime
#Go through parsed data and look for inconsistencies
hlex_df = pd.read_json('../../outputs_to_review/parsed_heiligenlexikon.json')

def is_valid_date(input_date_str: str):
    if pd.isnull(input_date_str):
        return True
    if input_date_str is None:
        return True

    date_split = input_date_str.split(".")
    day = int(date_split[0])
    month = int(date_split[1])
    try:
        datetime.datetime(year=1804, month=month, day=day)
        return True
    except:
        return False

#Checking dates
#print(hlex_df)
feast_days_df = hlex_df.T[['FeastDay', 'FeastDay0', 'FeastDay1', 'FeastDay2']]
#feast_days_df = hlex_df.T['FeastDay']
#feast_days_df.map(check_date, na_action='ignore')

counter = 0
faulty_entries = []
for item in feast_days_df.itertuples():
    hlex_id = item[0]
    for entry in item[1:]:
        if is_valid_date(entry):
            continue
        else:
            raw_entry = hlex_df.T.RawFeastDay[hlex_id]
            if 'al' in raw_entry:
                faulty_entries.append(";".join([hlex_id,raw_entry]))
                print(hlex_id, ": ", entry, " - Raw:", raw_entry)
                counter+=1
with open('faulty_date_entries.csv', 'w', encoding='utf-8') as faulty_entries_file:
    result_to_write = "\n".join(faulty_entries)
    faulty_entries_file.write(result_to_write)
print("Invalid dates found:")
print(counter)


#TODO check for vectorized alternative