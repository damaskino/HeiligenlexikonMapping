import sys
import json
from qwikidata.entity import WikidataItem

file_path = "filtered_entities.json"
with open(file_path, "r", encoding="utf-8") as new_file:
    json_content = json.loads(new_file.read())
    for item in json_content:
        wiki_item = WikidataItem(item)
        print("\n")
        print(item)
        print(wiki_item)
        print("\n")
