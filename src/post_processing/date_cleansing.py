#basically: if a number is accompanied by either month we know the date, if there is an al or et or comma between that, we can
#assume that the date is referring to the month after date. So essentially search from left to right, while remembering the days
#when we find the month, the days before that can be added to the month.
import pandas as pd

faulty_entries_df = pd.read_csv('faulty_date_entries.csv', sep=';', encoding='utf-8')
print(faulty_entries_df[1])