from tqdm import tqdm

from src.parse_transformed_heiligenlex import HlexParser

# the <term> tag in the document contains only the name and the canonization status

parser = HlexParser(no_nlp=True)
hlex_soup = parser.load_transformed_hlex_to_soup()

entries = [entry for entry in hlex_soup.find_all("entry")]

entry_paragraph_mapping = []
for entry in tqdm(entries):
    entry_id = entry.get("xml:id")
    non_empty_paragraphs = []
    paragraphs = entry.find_all('p')
    if paragraphs:
        non_empty_paragraphs = [str(p) for p in paragraphs if not p.is_empty_element]
    if non_empty_paragraphs:
        entry_paragraph_mapping.append((entry_id, non_empty_paragraphs[0]))

print("Building result string")
result_string = ""
for entry, paragraph_from_mapping in tqdm(entry_paragraph_mapping):
    result_string += "\n" + paragraph_from_mapping
    result_string += "\n#\n#\n#"

print("writing to file")
with open("../../data/1_intermediate/first_paragraphs_only.txt", "w", encoding="utf-8") as entries_file:
    entries_file.write(result_string)
