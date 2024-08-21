import pandas as pd

from src.training.build_trainingset import load_goldstandard_ids, load_devset_ids


# Alternative way to create negative data
def shuffle_negative_set(hlex_df: pd.DataFrame, wiki_df: pd.DataFrame):
    shuffled_wiki_samples = wiki_df.sample(frac=1, random_state=0).reset_index(drop=True)
    negative_samples_df = hlex_df.join(shuffled_wiki_samples)
    negative_samples_df.to_csv(sep=";", path_or_buf='negative_samples.csv', header=None, index=None)


# Draw from the full dataset by finding entries with the same name
# and if available, the same feast day
def find_same_name_entries(wholeset_df: pd.DataFrame, ids_to_remove: list[str]):

    git_base_url = "https://damaskino.github.io/HeiligenlexikonMapping?id="
    wholeset_df.insert(loc=2, column='NegativeExample', value='')

    full_dataset_df = pd.read_json("../../outputs_to_review/parsed_heiligenlexikon.json")
    full_dataset_df.drop(ids_to_remove, axis=1, inplace=True)
    #wholeset_df = pd.merge(wholeset_df, full_dataset_df.T[['SaintName']], left_on=0, right_index=True)
    wholeset_df = pd.merge(wholeset_df, full_dataset_df.T['SaintName'], left_on=0, right_index=True)
    wholeset_df.drop([2, 3], inplace=True, axis=1)
    wholeset_df.rename({0: 'HeiligenLexikonID', 1: 'WikidataID'}, axis="columns", inplace=True)
    wholeset_length = len(wholeset_df)
    no_double_found = 0
    negative_examples_found = []
    wholeset_df_copy = wholeset_df.copy()

    # TODO Rather than awkwardly trying to insert negative examples, just build up a new dataframe with maybe up to 2 or 3 same name saints

    for item in wholeset_df_copy.itertuples():

        hlex_id = item[1]
        entry = full_dataset_df[hlex_id]
        name = entry['SaintName']
        # find an occurence of a saint with the same name
        same_name_candidates = full_dataset_df.T[full_dataset_df.T['SaintName'] == name]
        same_name_candidates = same_name_candidates.drop(index=hlex_id)
        # saint_candidates = same_name_candidates[same_name_candidates["CanonizationStatus"]=='S.']
        same_name_saint = same_name_candidates.head(1)
        if len(same_name_saint) > 0:
            hlex_new_id = same_name_saint.index.values[0]
            negative_examples_found.append((hlex_id, hlex_new_id))
            #TODO: name columns for better readability
            # index_to_replace = hlex_df.index[hlex_df[0] == hlex_new_id]
            # index_to_replace = index_to_replace.values[0]
            # name_at_index = hlex_df.iloc[index_to_replace][0]
            # print("Replacing ", name_at_index, " with ", hlex_new_id)
            # print("Adding new name")
            #wholeset_df.loc[len(wholeset_df) + 1] = pd.Series([hlex_new_id, git_base_url + hlex_new_id, 1, name],
            #                                                  index=[0, 2, 'NegativeExample','SaintName'])
            wholeset_df.at[hlex_id,'NegativeExample']=hlex_new_id
            # wholeset_df.at[hlex_id, 'NegativeExampleLink'] = git_base_url + hlex_new_id

            #wholeset_df.loc[len(wholeset_df)+1] = full_dataset_df[hlex_new_id]



            #if len(negative_examples_found) >= int(wholeset_length / 2):
            if len(negative_examples_found) >= int(wholeset_length):
                print("Found enough negatives samples!")
                break
        else:
            no_double_found += 1

    print(wholeset_df)
    print("Negative examples")
    print(negative_examples_found)
    print(len(negative_examples_found))
    print("No doubles found: ", no_double_found)
    return wholeset_df


# TODO filter out devset and goldstandard set entries
if __name__ == '__main__':
    wholeset_df = pd.read_csv('wholeset_match_results_edit_thresh_100_feast_0.csv', sep=";", header=None)
    # hlex_columns_df = wholeset_df.loc[:, (0, 2)]
    # wiki_columns_df = wholeset_df.loc[:, (1, 3)]
    gold_ids = load_goldstandard_ids()
    dev_ids = load_devset_ids()
    ids_to_remove = gold_ids + dev_ids

    positive_negative_samples_df = find_same_name_entries(wholeset_df=wholeset_df, ids_to_remove=ids_to_remove)
    positive_negative_samples_df.to_csv('positive_negative_set.csv', header=True, index=True, sep=";")
    positive_negative_samples_df.to_json('positive_negative_set.json')