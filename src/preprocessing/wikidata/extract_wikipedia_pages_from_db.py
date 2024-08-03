import sqlite3
import wikipediaapi
import json

if __name__ == '__main__':
    conn = sqlite3.connect("processed_saints.db")
    cursor = conn.cursor()
    saints = cursor.execute("SELECT * from saints")

    print("Query executed")

    saints_to_text_dict = {}

    for index, entry in enumerate(saints):
        # if index % 100 == 0:
        print("At index: ", index)
        # print(id)
        # print(content)
        wikis_string = entry[3]
        wiki_id = entry[0]
        if len(wikis_string) == 0:
            continue
        wiki_page_str_list = wikis_string.split("$")

        for lang_entry in wiki_page_str_list:
            lang_text_dict = {}
            wiki_page_split = lang_entry.split(";")
            wiki = wiki_page_split[0]
            wiki_lang_str = wiki.removesuffix('wiki')
            if wiki_lang_str.endswith("quote") or wiki_lang_str.endswith("news"):
                continue
            if wiki_lang_str == "be_x_old":
                wiki_lang_str = wiki_lang_str.replace("_", "-")
            # wikipedia_base_url = f"https://{wiki_lang_str}.wikipedia.org"
            page_title = wiki_page_split[1]

            # Get wiki content as text
            wiki_obj = wikipediaapi.Wikipedia('Heiligenlexikonmapping (chen.li@posteo.net)', wiki_lang_str)

            # Get wiki content as html
            # wiki_obj = wikipediaapi.Wikipedia('Heiligenlexikonmapping (chen.li@posteo.net)', wiki_lang_str,
            #                                   extract_format = wikipediaapi.ExtractFormat.HTML)

            page_py = wiki_obj.page(page_title)
            page_text = page_py.text
            lang_text_dict = {wiki_lang_str: page_text}
        saints_to_text_dict[wiki_id] = lang_text_dict
    json_obj = json.dumps(saints_to_text_dict)

    with open("saints_wikitexts", "w") as jsonoutput:
        jsonoutput.write(json_obj)
