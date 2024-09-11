import datetime

import pandas as pd
from sentence_transformers import SentenceTransformer, util

#NOTE: copied from supervised_training.py, should be refactored if time allows
def find_longest_doc_language(wiki_text_series):
    longest_doc_lang = ""
    longest_doc_length = 0
    for lang in wiki_text_series.keys():
        if type(wiki_text_series[lang]) == str:
            if longest_doc_length < len(wiki_text_series[lang]):
                longest_doc_length = len(wiki_text_series[lang])
                longest_doc_lang = lang
    return longest_doc_lang


#go through all Wikipedia texts and calculate their respective embeddings
#return a wiki ID and an embedding, maybe the information which language was used
def calculate_embeddings(wiki_text_df):

    print("Calculating Wikipedia text embeddings")
    wikidata_ids_without_pages = []
    wikidata_ids_no_german_page = []

    wiki_id_embedding_language_tuples = []
    for wikidata_id in wiki_text_df[:20]:

        wikitext_series = wiki_text_df[wikidata_id]

        doc_lang = ""

        # TODO better to perform this check during the embedding calculations
        if "de" not in wikitext_series.keys():
            wikidata_ids_no_german_page.append(wikidata_id)
            doc_lang = find_longest_doc_language(wikitext_series)

        if "de" in wikitext_series.keys():
            if type(wikitext_series["de"]) != str:
                wikidata_ids_no_german_page.append(wikidata_id)
                doc_lang = find_longest_doc_language(wikitext_series)
            # Edge Case: german is available, but is nan -> use other longest language
            # other languages are also all nan --> skip entry
            if doc_lang == "":
                wikidata_ids_without_pages.append(wikidata_id)
                continue

        wiki_doc = wikitext_series[doc_lang]
        # todo add similarities
        wiki_german_doc = wiki_doc.replace("\n", " ")
        wiki_sentences = wiki_doc.split('.')

        wiki_embeddings = model.encode(wiki_sentences)
        # Aggregate sentence embeddings to get document embeddings
        # Here, we use mean pooling
        wiki_doc_embedding = wiki_embeddings.mean(axis=0)

        wiki_id_embedding_language_tuples.append((wikidata_id, wiki_doc_embedding, doc_lang))

    print("Wikidata pages without Wikipedia pages:")
    print(len(wikidata_ids_without_pages))
    print(wikidata_ids_without_pages)

    print("Wikidata pages without German pages:")
    print(len(wikidata_ids_no_german_page))
    print(wikidata_ids_no_german_page)

    print("Finished calculating embeddings")


    return wiki_id_embedding_language_tuples


#NOTE: partially copied from supervised_training.py, should be refactored if time allows
#TODO: go through all gold standard entries,
# for every entry, compare all the texts, based on highest similarity, assign an entry, if all entries fall below our calculated threshold, do not match anything
#TODO: don't need to calculate all embeddings everytime, makes more sense to go through once on the wikipedia side and get the embeddings ready
def calculate_similarities(gold_standard_df, wikitexts_df, threshold = 0.00):

    result_list = []



    wiki_embeddings = calculate_embeddings(wikitexts_df)

    gold_standard_df["SystemMatch"]=""
    gold_standard_df["SystemMatchLanguage"]=""
    gold_standard_df["SystemMatchSimilarity"]=""

    # converting to list for faster iteration
    gold_standard_list = gold_standard_df.to_numpy().tolist()
    gold_standard_samples_num = len(gold_standard_list)
    # TODO: going through a fraction of the entries to iron out the details, expand to full data later
    # for idx, hlex_tuple in enumerate(hlex_texts[:]):
    for idx, hlex_list in enumerate(gold_standard_list):
        max_similarity = 0.0
        max_sim_wiki_id = ""
        max_sim_wiki_lang = ""


        hlex_id = hlex_list[0]
        wikidata_id = hlex_list[1]

        print("At index: ", idx, "out of ", gold_standard_samples_num)
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

        for wiki_doc_embedding_tuple in wiki_embeddings:

            wiki_data_id = wiki_doc_embedding_tuple[0]
            wiki_doc_embedding = wiki_doc_embedding_tuple[1]
            wiki_doc_lang = wiki_doc_embedding_tuple[2]
            # Compute cosine similarity between the two document embeddings
            similarity = util.cos_sim(hlex_doc_embedding, wiki_doc_embedding)
            if max_similarity < similarity:
                max_similarity=similarity
                max_sim_wiki_id = wiki_data_id
                max_sim_wiki_lang = wiki_doc_lang

        if max_similarity < threshold:
            continue
        else:
            #update dataframe with system_match
            print("System match:", max_sim_wiki_id)
            gold_standard_df.loc[gold_standard_df['HeiligenLexikonID'] == hlex_id, 'SystemMatch'] = max_sim_wiki_id
            gold_standard_df.loc[gold_standard_df['HeiligenLexikonID'] == hlex_id, 'SystemMatchLanguage'] = max_sim_wiki_lang
            gold_standard_df.loc[gold_standard_df['HeiligenLexikonID'] == hlex_id, 'SystemMatchSimilarity'] = str(float(max_similarity))
    file_name = "gold_standard_sbert_results.csv"

    gold_standard_df.to_csv(file_name, sep=";")

if __name__ == "__main__":

    print("Starting at: ", str(datetime.datetime.now()))
    print("Loading model...")
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    print("Done")

    print("Loading gold_standard data...")
    gold_standard_data_df = pd.read_csv('../../data/2_annotated_data_gold_and_dev/gold_standard_hand_annotated_eschbach_li_no_comments.csv', encoding='utf-8', sep=';')
    gold_standard_data_df.drop(["SampleWikiPage"], axis=1, inplace=True)
    print("Done")



    # prepare the hlex text data
    hlex_df = pd.read_json('../../outputs_to_review/parsed_heiligenlexikon.json')


    #TODO add texts to the gold standard entries




    gold_standard_with_hlex_texts_df = pd.merge(gold_standard_data_df, hlex_df.T[['OriginalText']],
                                      left_on='HeiligenLexikonID', right_index=True, how='left')

    wiki_text_df = pd.read_json("../../data/3_wikipedia_texts/saints_wikitexts.json")
    wikidata_ids = list(gold_standard_data_df['GoldWikidataID'])
    # Preflight check: look for wikidata pages that have no wikipedia pages associated with them!
    wikidata_ids_without_pages = [id for id in wikidata_ids if (id not in wiki_text_df.columns)]
    wikidata_ids_with_pages = [id for id in wikidata_ids if (id in wiki_text_df.columns)]


    calculate_similarities(gold_standard_with_hlex_texts_df, wiki_text_df, threshold=0.81)
    # hlex_texts_negatives_df = pd.merge(negative_examples_df['HeiligenLexikonID'], hlex_df.T[['OriginalText']],
    #                                    left_on='HeiligenLexikonID', right_index=True, how='left')
    # hlex_texts_positives_df = pd.merge(positive_examples_df['HeiligenLexikonID'], hlex_df.T[['OriginalText']],
    #                                    left_on='HeiligenLexikonID', right_index=True, how='left')



    # Wikidata IDs mapped to dicts of language/wikitext pairs
    #wiki_text_df = pd.read_json("../../data/3_wikipedia_texts/saints_wikitexts.json")
    #wikidata_ids = list(positive_examples_df['WikidataID'])
    # The following wikidata pages have no wikipedia pages associated with them! (about 58)
    #wikidata_ids_without_pages = [id for id in wikidata_ids if (id not in wiki_text_df.columns)]
    #wikidata_ids_with_pages = [id for id in wikidata_ids if (id in wiki_text_df.columns)]

    #wiki_training_texts_df = wiki_text_df[wikidata_ids_with_pages]
