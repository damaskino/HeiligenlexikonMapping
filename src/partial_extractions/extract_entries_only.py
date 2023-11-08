from src.parse_transformed_heiligenlex import HlexParser

# the <term> tag in the document contains only the name and the canonization status

parser = HlexParser(no_nlp=True)
hlex_soup = parser.load_transformed_hlex_to_soup()

entries = [str(entry) for entry in hlex_soup.find_all("entry")]

with open("../../data/1_intermediate/entries.txt", "w", encoding="utf-8") as entries_file:
    entries_file.write("\n#\n#\n#\n".join(entries))
