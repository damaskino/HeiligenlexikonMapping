import sqlite3
import json
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import datetime



def find_longest_doc_language(wiki_text_series):
    longest_doc_lang = ""
    longest_doc_length = 0
    for lang in wiki_text_series.keys():
        if type(wiki_text_series[lang]) == str:
            if longest_doc_length < len(wiki_text_series[lang]):
                longest_doc_length = len(wiki_text_series[lang])
                longest_doc_lang = lang
    return longest_doc_lang


def calculate_similarities(wiki_sentences_limit: int=None):
    result_list = []

    wikidata_ids_without_pages = []
    wikidata_ids_no_german_page = []

    # converting to list for faster iteration
    full_training_list = training_with_texts_df.to_numpy().tolist()
    training_samples_num = len(full_training_list)
    # TODO: going through a fraction of the entries to iron out the details, expand to full data later
    # for idx, hlex_tuple in enumerate(hlex_texts[:]):
    for idx, hlex_list in enumerate(full_training_list):
        similarity = 0

        hlex_id = hlex_list[0]
        wikidata_id = hlex_list[1]
        should_match = hlex_list[3]
        # if idx % 100 == 0:
        #    print("At index: ", idx, "out of ", training_samples_num)
        print("At index: ", idx, "out of ", training_samples_num)
        hlex_doc = hlex_df[hlex_id]['OriginalText']
        hlex_doc = hlex_doc.replace("\n", " ")
        hlex_sentences = hlex_doc.split('.')
        wiki_sentences = []
        hlex_embeddings = model.encode(hlex_sentences)
        hlex_doc_embedding = hlex_embeddings.mean(axis=0)
        # Test with small sentence, Truncated version
        # Use only first x sentences for hlex as well
        # Add column for which language text was used
        # Doublecheck Texts with high similarity
        # Secondary information may be enough to push similarity very high
        if wikidata_id not in wiki_text_df.keys():
            wikidata_ids_without_pages.append(wikidata_id)

            continue

        wikitext_series = wiki_text_df[wikidata_id]

        doc_lang = ""

        if "de" not in wikitext_series.keys():
            wikidata_ids_no_german_page.append(wikidata_id)
            doc_lang = find_longest_doc_language(wikitext_series)

        if "de" in wikitext_series.keys():
            if type(wikitext_series["de"]) != str:
                wikidata_ids_no_german_page.append(wikidata_id)
                doc_lang = find_longest_doc_language(wikitext_series)
            else:
                doc_lang = "de"

        wiki_doc = wikitext_series[doc_lang]
        # todo add similarities
        wiki_german_doc = wiki_doc.replace("\n", " ")
        wiki_sentences = wiki_doc.split('.')

        if wiki_sentences_limit is not None:
            wiki_embeddings = model.encode(wiki_sentences[:wiki_sentences_limit])
        else:
            wiki_embeddings= model.encode(wiki_sentences)
        # Aggregate sentence embeddings to get document embeddings
        # Here, we use mean pooling
        wiki_doc_embedding = wiki_embeddings.mean(axis=0)

        # Compute cosine similarity between the two document embeddings
        similarity = util.cos_sim(hlex_doc_embedding, wiki_doc_embedding)

        result_str = ";".join([hlex_id, wikidata_id, str(int(should_match)), str(float(similarity))])
        result_list.append(result_str)
    results = "\n".join(result_list)

    print("Wikidata pages without Wikipedia pages:")
    print(len(wikidata_ids_without_pages))
    print(wikidata_ids_without_pages)

    print("Wikidata pages without German pages:")
    print(len(wikidata_ids_no_german_page))
    print(wikidata_ids_no_german_page)

    file_name = ""

    if wiki_sentences_limit is not None:
        file_name = f"training_similarities_first_{wiki_sentences_limit}_sentences.csv"
    else:
        file_name = "training_similarities_all_sentences.csv"

    with open(file_name, "w") as resultfile:
        resultfile.write(results)


print("Starting at: ", str(datetime.datetime.now()))
print("Loading model...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
print("Done")

print("Loading training data...")
training_data_ids_df = pd.read_csv('positive_negative_set.csv', encoding='utf-8', sep=';', index_col=0)
print("Done")
positive_examples_df = training_data_ids_df[training_data_ids_df['ShouldMatch'] == 1]
negative_examples_df = training_data_ids_df[training_data_ids_df['ShouldMatch'] == 0]

# prepare the hlex text data
hlex_df = pd.read_json('../../outputs_to_review/parsed_heiligenlexikon.json')

training_with_texts_df = pd.merge(training_data_ids_df, hlex_df.T[['OriginalText']],
                                  left_on='HeiligenLexikonID', right_index=True, how='left')

# hlex_texts_negatives_df = pd.merge(negative_examples_df['HeiligenLexikonID'], hlex_df.T[['OriginalText']],
#                                    left_on='HeiligenLexikonID', right_index=True, how='left')
# hlex_texts_positives_df = pd.merge(positive_examples_df['HeiligenLexikonID'], hlex_df.T[['OriginalText']],
#                                    left_on='HeiligenLexikonID', right_index=True, how='left')



# Wikidata IDs mapped to dicts of language/wikitext pairs
wiki_text_df = pd.read_json("../../data/3_wikipedia_texts/saints_wikitexts.json")
wikidata_ids = list(positive_examples_df['WikidataID'])
# The following wikidata pages have no wikipedia pages associated with them! (about 58)
wikidata_ids_without_pages = [id for id in wikidata_ids if (id not in wiki_text_df.columns)]
wikidata_ids_with_pages = [id for id in wikidata_ids if (id in wiki_text_df.columns)]

wiki_training_texts_df = wiki_text_df[wikidata_ids_with_pages]
# go through all texts in Wikitext and create list
# total_text_num = len(hlex_texts)
# NOTE: some entries from the traning data are wikidata entries only, meaning they do not have any associated
# Wikipedia pages!


wiki_sentences_max = 10

# TODO compute embeddings for all Hlex descriptions?

for wiki_sentences_num in range(1,wiki_sentences_max):
    calculate_similarities(wiki_sentences_num)

calculate_similarities()