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

            lang_wiki = wikipediaapi.Wikipedia('Heiligenlexikonmapping (chen.li@posteo.net)', wiki_lang_str)
            page_title = page_title.replace(' ', '_')
            page_py = lang_wiki.page(page_title)
            # print(page_py)
