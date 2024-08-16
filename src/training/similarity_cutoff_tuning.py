import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

# training_df = pd.read_csv("training_similarities.csv", sep=";", header=None)
training_df = pd.read_csv("training_similarities_first_3_sentences.csv", sep=";", header=None)
print(training_df)
training_df.columns = ['HLexID', 'WikidataID', 'ShouldMatch', 'Similarity']


for threshold in np.arange(0,1.0, 0.01):

    matches_series = training_df['Similarity'].where(training_df['Similarity'] < threshold, 1)
    matches_series.where(matches_series > threshold, 0, inplace=True)
    matches_series = matches_series.astype(int)
    training_df['SystemMatch'] = matches_series

    gold_matches = training_df['ShouldMatch']
    system_matches = training_df['SystemMatch']


    acc = accuracy_score(gold_matches, system_matches)
    # Add precision recall
    #check acc, threshold 0 or 1 should yield 50% acc!
    print(threshold, acc)