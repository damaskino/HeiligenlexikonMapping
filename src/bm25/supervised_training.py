import sqlite3

import pandas as pd
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

# hlex data
hlex_df = pd.read_json('../../outputs_to_review/parsed_heiligenlexikon.json')

# put hlex texts into a list
# TODO: need to be able to reassign it to their respective entries!
hlex_texts = list(zip(hlex_df.T.index, hlex_df.T['OriginalText']))

# Wikidata IDs mapped to dicts of language/wikitext pairs
wiki_text_df = pd.read_json("../../data/3_wikipedia_texts/saints_wikitexts_stub.json")

# go through all texts in Wikitext and create list
# TODO: going only through German for now
total_text_num = len(hlex_texts)

# TODO: going through a fraction of the entries to iron out the details, expand to full data later
for idx, hlex_tuple in enumerate(hlex_texts[10]):
    hlex_id = hlex_tuple[0]
    hlex_doc = hlex_tuple[1]
    if idx % 100 == 0:
        print("At index: ", idx, "out of ", total_text_num)
    hlex_sentences = hlex_doc.split('.')
    wiki_sentences = []

    # Get the German Text if available or another one
    for item in wiki_text_df.columns:
        # print(df[item])
        if "de" in wiki_text_df[item].keys():
            wiki_german_doc = wiki_text_df[item]["de"]
            wiki_sentences = wiki_german_doc.split('.')

    if len(wiki_sentences) == 0:
        continue
    embeddings1 = model.encode(hlex_sentences)
    embeddings2 = model.encode(wiki_sentences)

    # Aggregate sentence embeddings to get document embeddings
    # Here, we use mean pooling
    doc_embedding1 = embeddings1.mean(axis=0)
    doc_embedding2 = embeddings2.mean(axis=0)

    # Compute cosine similarity between the two document embeddings
    similarity = util.cos_sim(doc_embedding1, doc_embedding2)
    # print(f"Cosine similarity between the documents: {similarity.item()}")
