import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score


def calculate_acc_for_similarity_cutoff(training_df, threshold):
    matches_series = training_df['Similarity'].where(training_df['Similarity'] < threshold, 1)
    matches_series.where(matches_series > threshold, 0, inplace=True)
    matches_series = matches_series.astype(int)
    training_df['SystemMatch'] = matches_series

    gold_matches = training_df['ShouldMatch']
    system_matches = training_df['SystemMatch']

    acc = accuracy_score(gold_matches, system_matches)


def evaluate_files():
    # training_df = pd.read_csv("training_similarities.csv", sep=";", header=None)
    max_acc = 0
    max_sent_length = 0
    max_sim_cut_off = 0

    for sent_length in range(1, 10):

        file_name = f"training_similarities_first_{sent_length}_sentences.csv"

        print(file_name)

        training_df = pd.read_csv(file_name, sep=";", header=None)
        print(training_df)
        training_df.columns = ['HLexID', 'WikidataID', 'ShouldMatch', 'Similarity']

        for threshold in np.arange(0.5, 1.0, 0.01):
            acc = calculate_acc_for_similarity_cutoff(threshold)
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


if __name__ == '__main__':
    evaluate_files()
