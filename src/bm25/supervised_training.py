import sqlite3

import pandas as pd
from sklearn.preprocessing import LabelEncoder

data_df = pd.read_csv('positive_negative_set.csv', encoding='utf-8', sep=';')

# Devset: for every entry, go through all other entries and check which one seems to be a fit, based
# on text matching with embeddings first, and possibly other features later on

# wikidata data
saints_db = sqlite3.connect("../preprocessing/wikidata/wikidata_saints.db")
saints_cursor = saints_db.cursor()
saints = saints_cursor.executescript("SELECT * FROM saints;")

# Wikidata IDs mapped to dicts of language/wikitext pairs
wiki_text_df = pd.read_json("../../data/3_wikipedia_texts/saints_wikitexts_stub.json")

# Get the German Text if available or another one
for item in wiki_text_df.columns:
    # print(df[item])
    if "de" in wiki_text_df[item].keys():
        german_doc = wiki_text_df[item]["de"]

for idx, (id, content) in enumerate(saints):
    print(id)
    print(content)

    # do something with it
    if idx > 100:
        break


def encode_labels(labels):
    n_labels = len(labels)
