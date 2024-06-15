from tqdm import tqdm

from src.preprocessing.heiligenlexikon.parse_transformed_heiligenlex import HlexParser

# the <term> tag in the document contains only the name and the canonization status

parser = HlexParser(no_nlp=True)
hlex_soup = parser.load_transformed_hlex_to_soup()

entries = [entry for entry in hlex_soup.find_all("entry")]

first_hi_rends = []
for entry in tqdm(entries):
    entry_id = entry.get("xml:id")
    hi_rends = entry.find_all("hi", rend="bold")

    hi_rends_to_add = ""
    if hi_rends:
        first_hi_rend = hi_rends[0]
        hi_rends_to_add = str(first_hi_rend)

    if len(hi_rends) == 2:
        second_hi_rend = hi_rends[1]
        hi_rends_to_add += "\n" + str(second_hi_rend.parent)
    first_hi_rends.append(hi_rends_to_add)
    # paragraphs = entry.find_all('p')
    # if paragraphs:
    #     first_paragraph = entry.find_all('p')[0]
    #     hi_rends = first_paragraph.find_all('hi', rend="bold")
    #     if len(hi_rends) > 0:
    #         print("hi_rend found in first paragraph!")
    #         sys.exit()

    # first_hi_rend = hi_rends[0]
    # first_hi_rends.append(first_hi_rend)

print("writing to file")
with open(
        "../../../data/1_intermediate/first_hi_rends.txt", "w", encoding="utf-8"
) as entries_file:
    entries_file.write("\n#\n#\n#\n".join(first_hi_rends))
