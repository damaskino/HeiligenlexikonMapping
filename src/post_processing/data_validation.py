import pandas as pd
import datetime
#Go through parsed data and look for inconsistencies
hlex_df = pd.read_json('../../outputs_to_review/parsed_heiligenlexikon.json')

def is_valid_date(input_date_str: str):
    if pd.isnull(input_date_str):
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

for item in feast_days_df.itertuples():
    counter = 0
    id = item[0]
    for entry in item[1:]:
        if is_valid_date(entry):
            continue
        else:
            counter+=1
print("Invalid dates found:")
print(counter)


#TODO check for vectorized alternative