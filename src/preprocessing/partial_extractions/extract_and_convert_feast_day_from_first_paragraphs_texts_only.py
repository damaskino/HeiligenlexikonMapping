from tqdm import tqdm

from src.preprocessing.heiligenlexikon.parse_dates import convert_date
from src.preprocessing.heiligenlexikon.parse_transformed_heiligenlex import HlexParser

# the <term> tag in the document contains only the name and the canonization status
from src.preprocessing.heiligenlexikon.regex_matching import match_raw_feast_day

parser = HlexParser(no_nlp=True)
hlex_soup = parser.load_transformed_hlex_to_soup()

entries = [entry for entry in hlex_soup.find_all("entry")]

entry_paragraph_mapping = []
for entry in tqdm(entries):
    entry_id = entry.get("xml:id")
    non_empty_paragraphs = []
    paragraphs = entry.find_all("p")
    if paragraphs:
        non_empty_paragraphs = [p.text for p in paragraphs if not p.is_empty_element]
    if non_empty_paragraphs:
        entry_paragraph_mapping.append((entry_id, non_empty_paragraphs[0]))

print("Building result string")
result_string = ""
for _, paragraph_from_mapping in tqdm(entry_paragraph_mapping):
    print(paragraph_from_mapping)
    raw_feast_date = match_raw_feast_day(paragraph_from_mapping)
    if raw_feast_date is not None:
        parsed_feast_days = convert_date(raw_feast_date)
        result_string += str(parsed_feast_days)
        result_string += "\n"

print("writing to file")
with open(
        "../data/1_intermediate/first_paragraphs_parsed_feast_days_only.txt",
        "w",
        encoding="utf-8",
) as entries_file:
    entries_file.write(result_string)
