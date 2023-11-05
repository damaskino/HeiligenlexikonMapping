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
    entry_paragraph_mapping.append((entry_id, non_empty_paragraphs))

print("Building result string")
result_string = ""
for entry, paragraphs in tqdm(entry_paragraph_mapping):
    result_string += "\n".join(paragraphs)
    result_string += "\n#\n#\n#\n"

print("writing to file")
with open("../data/1_intermediate/paragraphs.txt", "w", encoding="utf-8") as entries_file:
    entries_file.write(result_string)
