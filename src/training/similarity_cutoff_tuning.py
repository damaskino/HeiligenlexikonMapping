import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from decimal import Decimal

def calculate_acc_for_similarity_cutoff(training_df, threshold):
    matches_series = training_df['Similarity'].where(training_df['Similarity'] < threshold, 1)
    matches_series.where(matches_series > threshold, 0, inplace=True)
    matches_series = matches_series.astype(int)
    training_df['SystemMatch'] = matches_series

    gold_matches = training_df['ShouldMatch']
    system_matches = training_df['SystemMatch']

    acc = accuracy_score(gold_matches, system_matches)
    return acc


def evaluate_files():
    # training_df = pd.read_csv("training_similarities.csv", sep=";", header=None)

    #Keep track of the max accuracy we've seen
    max_acc = 0
    max_sent_length = 0
    max_sim_cut_off = 0

    acc_results = []


    for sent_length in range(1, 10):

        file_name = f"training_similarities_first_{sent_length}_sentences.csv"

        print(file_name)

        training_df = pd.read_csv(file_name, sep=";", header=None)
        print(training_df)
        training_df.columns = ['HLexID', 'WikidataID', 'ShouldMatch', 'Similarity']

        for threshold in np.arange(0.5, 1.0, 0.01):
            acc = calculate_acc_for_similarity_cutoff(training_df, threshold)

            result_tuple = (str(sent_length), str(round(Decimal(threshold), 2)), str(acc))
            acc_results.append(";".join(result_tuple))

            if acc > max_acc:
                max_acc = acc
                max_acc_sim_thresh = threshold
                max_acc_sent_length = sent_length

    print("Best Accuracy:", max_acc)
    print("Highest Acc at similarity: ", max_sim_cut_off)
    print("Highest Acc at sentence Length: ", max_sent_length)

    # Add precision recall
    # check acc, threshold 0 or 1 should yield 50% acc!
    # print(threshold, acc)
    #Write parameter and accuracy to result file
    results_string = "\n".join(acc_results)
    header = "SentenceLength;SimilarityThreshold;Accuracy\n"
    results_string = header+results_string
    with open("acc_results_across_sent_len_and_similarity_cutoff.csv", "w") as acc_result_file:
        acc_result_file.write(results_string)


if __name__ == '__main__':
    evaluate_files()
