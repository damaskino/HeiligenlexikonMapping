import sqlite3
import wikipediaapi

if __name__ == '__main__':
    conn = sqlite3.connect("processed_saints.db")
    cursor = conn.cursor()
    saints = cursor.execute("SELECT * from saints")

    for index, entry in enumerate(saints):
        if index % 1000 == 0:
            print("At index: ", index)
        # print(id)
        # print(content)
        wikis_string = entry[3]
        if len(wikis_string) == 0:
            continue
        wiki_page_str_list = wikis_string.split("$")

        for entry in wiki_page_str_list:
            wiki_page_split = entry.split(";")
            wiki = wiki_page_split[0]
            wiki_lang_str = wiki.removesuffix('wiki')

            # wikipedia_base_url = f"https://{wiki_lang_str}.wikipedia.org"
            page_title = wiki_page_split[1]

            # Get wiki content as text
            wiki_obj = wikipediaapi.Wikipedia('Heiligenlexikonmapping (chen.li@posteo.net)', wiki_lang_str)

            # Get wiki content as html
            # wiki_obj = wikipediaapi.Wikipedia('Heiligenlexikonmapping (chen.li@posteo.net)', wiki_lang_str,
            #                                   extract_format = wikipediaapi.ExtractFormat.HTML)

            page_py = wiki_obj.page(page_title)
            print(page_py.text)
