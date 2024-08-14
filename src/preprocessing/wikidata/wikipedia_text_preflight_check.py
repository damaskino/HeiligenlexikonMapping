# A "preflight check" to make sure all the urls we generated are valid before we try and get their contents

import sqlite3
import wikipediaapi
import json
import tenacity
from tenacity import wait_fixed
import urllib


# @tenacity.retry(wait=wait_fixed(2))
def fetch_page_text(page_title, wiki_lang_str):
    wiki_obj = wikipediaapi.Wikipedia('Heiligenlexikonmapping (chen.li@posteo.net)', wiki_lang_str)
    #
    # # Get wiki content as html
    # # wiki_obj = wikipediaapi.Wikipedia('Heiligenlexikonmapping (chen.li@posteo.net)', wiki_lang_str,
    # #                                   extract_format = wikipediaapi.ExtractFormat.HTML)
    #
    # page_py = wiki_obj.page(page_title)
    page_text = ""
    page_title = page_title.replace(" ", "_")
    print("Raw page title:", page_title)
    page_title_encoded = urllib.parse.quote(page_title)
    # page_text = page_py.text

    wikipedia_base_url = f"https://{wiki_lang_str}.wikipedia.org/wiki/"
    wikipedia_url = wikipedia_base_url + page_title_encoded
    print("Requesting url: ", wikipedia_url)
    response_code = urllib.request.urlopen(wikipedia_url).getcode()

    # print(response_code)
    if response_code != 200:
        print("Error at url: ", wikipedia_url)
        print(response_code)

    return page_text


if __name__ == '__main__':
    conn = sqlite3.connect("processed_saints.db")
    cursor = conn.cursor()
    saints = cursor.execute("SELECT * from saints")

    print("Query executed")

    saints_to_text_dict = {}

    for index, entry in enumerate(saints):
        if index < 7600:
            continue
        # if index % 100 == 0:
        print("At index: ", index)
        # print(id)
        # print(content)
        wikis_string = entry[3]
        wiki_id = entry[0]
        if len(wikis_string) == 0:
            continue
        wiki_page_str_list = wikis_string.split("$")
        lang_text_dict = {}
        for lang_entry in wiki_page_str_list:
            wiki_page_split = lang_entry.split(";")
            wiki = wiki_page_split[0]
            wiki_lang_str = wiki.removesuffix('wiki')
            if wiki_lang_str.endswith("quote") or wiki_lang_str.endswith("news") or wiki_lang_str.endswith(
                    "source") or wiki_lang_str.endswith("wikiversity") or wiki_lang_str.endswith(
                    "books") or wiki_lang_str.endswith("voyage"):
                continue
            wiki_lang_str = wiki_lang_str.replace("_", "-")

            page_title = wiki_page_split[1]

            # Get wiki content as text
            page_text = fetch_page_text(page_title, wiki_lang_str)
            lang_text_dict[wiki_lang_str] = page_text
        saints_to_text_dict[wiki_id] = lang_text_dict
    json_obj = json.dumps(saints_to_text_dict)

    with open("saints_wikitexts.json", "w") as jsonoutput:
        jsonoutput.write(json_obj)