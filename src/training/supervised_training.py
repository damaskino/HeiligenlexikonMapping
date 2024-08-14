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
positive_examples_df['Shouldmatch'] = True
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
wikidata_ids = list(training_data_ids_df['WikidataID'])
# These wikidata pages have no wikipedia pages associated with them!
# about 58
wikidata_ids_without_pages = [id for id in wikidata_ids if (id not in wiki_text_df.columns)]
wikidata_ids_with_pages = [id for id in wikidata_ids if (id in wiki_text_df.columns)]


# go through all texts in Wikitext and create list
# TODO: going only through German for now
# total_text_num = len(hlex_texts)
wiki_training_texts_df = wiki_text_df[wikidata_ids_with_pages]
# NOTE: some entries from the traning data are wikidata entries only, meaning they do not have any associated
# Wikipedia pages!


# TODO compute embeddings for all Hlex descriptions


# TODO starting with fixed threshold, make it shifting later to find best threshold
threshold = 0.75

total_matches = 0
true_positives = 0
true_negatives = 0
false_positives = 0
false_negatives = 0

result_list = []

# converting to list for faster iteration
full_training_list = full_training_df.to_numpy().tolist()
training_samples_num = len(full_training_list)
# TODO: going through a fraction of the entries to iron out the details, expand to full data later
# for idx, hlex_tuple in enumerate(hlex_texts[:]):
for idx, hlex_list in enumerate(full_training_list[:]):
    match_id = ""
    max_similarity = 0
    best_candidate_wiki_id = ""

    # Keep track of if the current result was a true positive, true negative, etc.
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    hlex_id = hlex_list[0]
    hlex_doc = hlex_list[1]
    should_match = hlex_list[2]
    # if idx % 100 == 0:
    #    print("At index: ", idx, "out of ", training_samples_num)
    print("At index: ", idx, "out of ", training_samples_num)
    hlex_sentences = hlex_doc.split('.')
    wiki_sentences = []
    hlex_embeddings = model.encode(hlex_sentences)
    hlex_doc_embedding = hlex_embeddings.mean(axis=0)

    print("Going through wiki texts...")
    for sent_idx, item in enumerate(wiki_training_texts_df.columns):
        if sent_idx % 100 == 0:
            print("At wiki sentence: ", sent_idx)
        # print(df[item])
        if "de" in wiki_training_texts_df[item].keys():
            wiki_german_doc = wiki_training_texts_df[item]["de"]
            if type(wiki_german_doc) != str:
                continue
            wiki_sentences = wiki_german_doc.split('.')

        if len(wiki_sentences) == 0:
            continue

        # TODO only use a couple sentences for now
        wiki_embeddings = model.encode(wiki_sentences[:3])
        # Aggregate sentence embeddings to get document embeddings
        # Here, we use mean pooling
        wiki_doc_embedding = wiki_embeddings.mean(axis=0)

        # Compute cosine similarity between the two document embeddings
        similarity = util.cos_sim(hlex_doc_embedding, wiki_doc_embedding)
        if similarity > max_similarity:
            max_similarity = similarity
            best_candidate_wiki_id = item

    if max_similarity >= threshold:
        # if max_similarity does not reach threshold, ignore
        print(f"Best Candidate for {hlex_id}: ", best_candidate_wiki_id)
        print(f"Cosine similarity between the documents: {max_similarity}")

        total_matches += 1
        match_id = best_candidate_wiki_id
        # check if the identified match is correct
        if should_match:
            true_positives += 1
        else:
            false_positives += 1


    if max_similarity < threshold:
        if should_match:
            false_negatives += 1
        else:
            true_negatives += 1


    single_match_dict = {"HLexID": hlex_id, "MatchID": match_id, "TP": tp, "TN": tn, "FP": fp, "FN": fn}
    result_list.append(single_match_dict)

filename = f"training_embedding_results_{str(threshold)}.json"

with open(filename,'w') as outputfile:
    json.dump(result_list, outputfile)

print("Treshold: ", threshold)
print("True Positives:", true_positives)
print("True Negatives:", true_negatives)
print("False Positives:", false_positives)
print("False Negatives:", false_negatives)

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
