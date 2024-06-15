from tqdm import tqdm

from src.preprocessing.heiligenlexikon.occupation_extraction import (
    setup_occupation_list,
    extract_occupation,
)
from src.preprocessing.heiligenlexikon.parse_transformed_heiligenlex import HlexParser

# the <term> tag in the document contains only the name and the canonization status

parser = HlexParser(no_nlp=True)
hlex_soup = parser.load_transformed_hlex_to_soup("../../data/Heiligenlex-1858.xml")

occupation_list = setup_occupation_list("../../../resources/occupation_list.txt")

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
for entry_id, paragraph_from_mapping in tqdm(entry_paragraph_mapping):
    result_string += f"{entry_id}\n"
    occupation = extract_occupation(
        paragraph_from_mapping, occupation_list=occupation_list
    )
    if occupation == None:
        occupation = " "
    result_string += occupation
    result_string += "\n#\n#\n#"

print("writing to file")
with open(
        "../../../data/1_intermediate/first_paragraphs_occupations_only.txt",
        "w",
        encoding="utf-8",
) as entries_file:
    entries_file.write(result_string)
