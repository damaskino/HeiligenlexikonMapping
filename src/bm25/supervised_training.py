import sqlite3

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util

print("Loading model...")
# TODO: check if this model is appropriate for german data!
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Done")

print("Loading training data...")
training_data_ids_df = pd.read_csv('positive_negative_set.csv', encoding='utf-8', sep=';')
print("Done")

# Devset: for every entry, go through all other entries and check which one seems to be a fit, based
# on text matching with embeddings first, and possibly other features later on

# wikidata data for other features
# saints_db = sqlite3.connect("../preprocessing/wikidata/wikidata_saints.db")
# saints_cursor = saints_db.cursor()
# saints = saints_cursor.executescript("SELECT * FROM saints;")

# for idx, (id, content) in enumerate(saints):
#     print(id)
#     print(content)
#
#     # do something with it
#     if idx > 100:
#         break

# hlex full data in case we need it
# hlex_df = pd.read_json('../../outputs_to_review/parsed_heiligenlexikon.json')

# put hlex texts into a list
# TODO: need to be able to reassign it to their respective entries!
hlex_texts = list(zip(training_data_ids_df['HeiligenLexikonID'], training_data_ids_df['OriginalText']))

# Wikidata IDs mapped to dicts of language/wikitext pairs
wiki_text_df = pd.read_json("../../data/3_wikipedia_texts/saints_wikitexts.json")

# go through all texts in Wikitext and create list
# TODO: going only through German for now
total_text_num = len(hlex_texts)

# TODO: going through a fraction of the entries to iron out the details, expand to full data later
for idx, hlex_tuple in enumerate(hlex_texts[:]):
    max_similarity = 0
    best_candidate = ""

    hlex_id = hlex_tuple[0]
    hlex_doc = hlex_tuple[1]
    if idx % 100 == 0:
        print("At index: ", idx, "out of ", total_text_num)
    hlex_sentences = hlex_doc.split('.')
    wiki_sentences = []
    hlex_embeddings = model.encode(hlex_sentences)
    hlex_doc_embedding = hlex_embeddings.mean(axis=0)

    # Get the German Wikipedia Text if available or another one
    for item in wiki_text_df.columns:
        # print(df[item])
        if "de" in wiki_text_df[item].keys():
            wiki_german_doc = wiki_text_df[item]["de"]
            if type(wiki_german_doc) != str:
                continue
            wiki_sentences = wiki_german_doc.split('.')

        if len(wiki_sentences) == 0:
            continue

        wiki_embeddings = model.encode(wiki_sentences)

        # Aggregate sentence embeddings to get document embeddings
        # H    ere, we use mean pooling

        wiki_doc_embedding = wiki_embeddings.mean(axis=0)

        # Compute cosine similarity between the two document embeddings
        similarity = util.cos_sim(hlex_doc_embedding, wiki_doc_embedding)
        if similarity > max_similarity:
            max_similarity = similarity
            best_candidate = item

    print(f"Best Candidate for {hlex_id}: ", best_candidate)
    print(f"Cosine similarity between the documents: {max_similarity}")
