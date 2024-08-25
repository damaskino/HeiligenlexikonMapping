import pandas as pd

from src.training.build_trainingset import load_goldstandard_ids, load_devset_ids

max_same_name_candidates = 2
# Alternative way to create negative data
def shuffle_negative_set(hlex_df: pd.DataFrame, wiki_df: pd.DataFrame):
    shuffled_wiki_samples = wiki_df.sample(frac=1, random_state=0).reset_index(drop=True)
    negative_samples_df = hlex_df.join(shuffled_wiki_samples)
    negative_samples_df.to_csv(sep=";", path_or_buf='negative_samples.csv', header=None, index=None)


# Draw from the full dataset by finding entries with the same name
# and if available, the same feast day
def find_same_name_entries(full_set_no_gold_no_dev_df: pd.DataFrame):

    full_dataset_df = pd.read_json("../../outputs_to_review/parsed_heiligenlexikon.json")
    full_set_no_gold_no_dev_df = pd.merge(full_set_no_gold_no_dev_df, full_dataset_df.T['SaintName'], left_on=0,
                                          right_index=True)
    full_set_no_gold_no_dev_df.drop([2, 3], inplace=True, axis=1)
    full_set_no_gold_no_dev_df.rename({0: 'HeiligenLexikonID', 1: 'WikidataID'}, axis="columns", inplace=True)
    full_set_length = len(full_set_no_gold_no_dev_df)
    full_set_no_gold_no_dev_df['ShouldMatch'] = 1
    no_double_found = 0
    negative_examples_found = []
    full_set_df_copy = full_set_no_gold_no_dev_df.copy()

    #Positive examples are taken care of at this point, just need to generate negatives samples from here
    for item in full_set_df_copy.itertuples():

        hlex_id = item[1]
        wiki_id = item[2]

        name = item[3]
        # find an occurence of a saint with the same name and remove the one that we already have in the positive examples
        same_name_candidates = full_dataset_df.T[full_dataset_df.T['SaintName'] == name]
        same_name_candidates = same_name_candidates.drop(index=hlex_id)
        # saint_candidates = same_name_candidates[same_name_candidates["CanonizationStatus"]=='S.']
        if len(same_name_candidates) > 0:
            for saint_idx, same_name_saint_id in enumerate(same_name_candidates.T):
                if saint_idx < max_same_name_candidates:
                    negative_examples_found.append((same_name_saint_id, wiki_id, name, 0))
                else:
                    break
        else:
            no_double_found += 1

        if len(negative_examples_found) >= full_set_length:
            break

    negative_examples_found = negative_examples_found[:full_set_length]
    negative_samples_df = pd.DataFrame(negative_examples_found)

    negative_samples_df.columns = ["HeiligenLexikonID", "WikidataID", "SaintName", "ShouldMatch"]
    positive_negative_samples_df = pd.concat([full_set_no_gold_no_dev_df, negative_samples_df])
    positive_negative_samples_df.reset_index(drop=True, inplace=True)
    print("Negative examples")
    print(negative_examples_found)
    print(len(negative_examples_found))
    print("No doubles found: ", no_double_found)
    return positive_negative_samples_df



if __name__ == '__main__':
    full_set_no_gold_no_dev_df = pd.read_csv('wholeset_match_results_edit_thresh_100_feast_0.csv', sep=";", header=None)
    positive_negative_samples_df = find_same_name_entries(full_set_no_gold_no_dev_df=full_set_no_gold_no_dev_df)
    positive_negative_samples_df.to_csv('positive_negative_set.csv', header=True, index=True, sep=";")
