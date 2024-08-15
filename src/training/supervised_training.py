import sqlite3
import json
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import datetime

print("Starting at: ", str(datetime.datetime.now()))
print("Loading model...")
# TODO: check if this model is appropriate for german data!
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Done")

print("Loading training data...")
training_data_ids_df = pd.read_csv('positive_negative_set.csv', encoding='utf-8', sep=';')
print("Done")
positive_examples_df = training_data_ids_df.loc[:, ('HeiligenLexikonID', 'WikidataID')]
negative_examples_df = training_data_ids_df.loc[:, ('NegativeExample', "WikidataID")]
negative_examples_df = negative_examples_df.dropna()
negative_examples_df.rename(columns={'NegativeExample': 'HeiligenLexikonID'}, inplace=True)

negative_examples_df['ShouldMatch'] = False
positive_examples_df['ShouldMatch'] = True
full_training_df = pd.concat([positive_examples_df, negative_examples_df], axis=0, ignore_index=True)

# put hlex texts into a list
# TODO: need to be able to reassign it to their respective entries!
hlex_texts_positives = list(zip(training_data_ids_df['HeiligenLexikonID'], training_data_ids_df['OriginalText']))
# TODO may have to add some more examples that just don't have positive matches, but do have negative matches...

# prepare the hlex text data
hlex_df = pd.read_json('../../outputs_to_review/parsed_heiligenlexikon.json')
hlex_texts_negatives_df = pd.merge(negative_examples_df['HeiligenLexikonID'], hlex_df.T[['OriginalText']],
                                   left_on='HeiligenLexikonID', right_index=True, how='left')
hlex_texts_positives_df = pd.merge(positive_examples_df['HeiligenLexikonID'], hlex_df.T[['OriginalText']],
                                   left_on='HeiligenLexikonID', right_index=True, how='left')

# Wikidata IDs mapped to dicts of language/wikitext pairs
wiki_text_df = pd.read_json("../../data/3_wikipedia_texts/saints_wikitexts.json")
wikidata_ids = list(positive_examples_df['WikidataID'])
# The following wikidata pages have no wikipedia pages associated with them! (about 58)
wikidata_ids_without_pages = [id for id in wikidata_ids if (id not in wiki_text_df.columns)]
wikidata_ids_with_pages = [id for id in wikidata_ids if (id in wiki_text_df.columns)]

wiki_training_texts_df = wiki_text_df[wikidata_ids_with_pages]
# go through all texts in Wikitext and create list
# TODO: going only through German for now
# total_text_num = len(hlex_texts)
# NOTE: some entries from the traning data are wikidata entries only, meaning they do not have any associated
# Wikipedia pages!


# TODO compute embeddings for all Hlex descriptions


# TODO starting with fixed threshold, make it shifting later to find best threshold
threshold = 0.75
threshold = 0.5
threshold = 0.2

total_matches = 0
true_positives = 0
true_negatives = 0
false_positives = 0
false_negatives = 0

result_list = []

wikidata_ids_without_pages = []
wikidata_ids_no_german_page = []



# converting to list for faster iteration
full_training_list = full_training_df.to_numpy().tolist()
training_samples_num = len(full_training_list)
# TODO: going through a fraction of the entries to iron out the details, expand to full data later
# for idx, hlex_tuple in enumerate(hlex_texts[:]):
for idx, hlex_list in enumerate(full_training_list):
    similarity = 0

    hlex_id = hlex_list[0]
    wikidata_id = hlex_list[1]
    should_match = hlex_list[2]
    # if idx % 100 == 0:
    #    print("At index: ", idx, "out of ", training_samples_num)
    print("At index: ", idx, "out of ", training_samples_num)
    hlex_doc = hlex_df[hlex_id]['OriginalText']
    hlex_doc = hlex_doc.replace("\n", " ")
    hlex_sentences = hlex_doc.split('.')
    wiki_sentences = []
    hlex_embeddings = model.encode(hlex_sentences)
    hlex_doc_embedding = hlex_embeddings.mean(axis=0)


    if wikidata_id not in wiki_text_df.keys():
        wikidata_ids_without_pages.append(wikidata_id)

        continue

    wikitext_series = wiki_text_df[wikidata_id]

    if "de" not in wikitext_series.keys():
        wikidata_ids_no_german_page.append(wikidata_id)

    if "de" in wikitext_series.keys():

        if type(wikitext_series["de"]) != str:
            wikidata_ids_no_german_page.append(wikidata_id)

        if type(wikitext_series["de"]) == str:
            wiki_german_doc = wikitext_series["de"]
            #todo add similarities
            wiki_german_doc = wiki_german_doc.replace("\n", " ")
            wiki_sentences = wiki_german_doc.split('.')
            wiki_embeddings = model.encode(wiki_sentences[:])
            # Aggregate sentence embeddings to get document embeddings
            # Here, we use mean pooling
            wiki_doc_embedding = wiki_embeddings.mean(axis=0)

            # Compute cosine similarity between the two document embeddings
            similarity = util.cos_sim(hlex_doc_embedding, wiki_doc_embedding)

    result_str = ";".join([hlex_id,wikidata_id,str(int(should_match)),str(float(similarity))])
    result_list.append(result_str)
results = "\n".join(result_list)

print("Wikidata pages without Wikipedia pages:")
print(len(wikidata_ids_without_pages))
print(wikidata_ids_without_pages)

print("Wikidata pages without German pages:")
print(len(wikidata_ids_no_german_page))
print(wikidata_ids_no_german_page)

with open("training_similarities.csv", "w") as resultfile:
    resultfile.write(results)
