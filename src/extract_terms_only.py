from src.parse_transformed_heiligenlex import HlexParser

# the <term> tag in the document contains only the name and the canonization status

parser = HlexParser()
hlex_soup = parser.load_transformed_hlex_to_soup()

terms = [term.text for term in hlex_soup.find_all("term")]

with open("../outputs_to_review/terms.txt", "w", encoding="utf-8") as terms_file:
    terms_file.write("\n".join(terms))
