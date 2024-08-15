import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score


training_df = pd.read_csv("training_similarities.csv", sep=";", header=None)
print(training_df)
training_df.columns = ['HLexID', 'WikidataID', 'ShouldMatch', 'Similarity']


for threshold in np.arange(0,1.0, 0.01):

    matches_series = training_df['Similarity'].where(training_df['Similarity'] < threshold, 1)
    matches_series.where(matches_series > threshold, 0, inplace=True)
    matches_series = matches_series.astype(int)
    training_df['SystemMatch'] = matches_series

    #TODO: find a good cut off point, look into using the other languages
    #check if current embedding model works, look into the paper

    gold_matches = training_df['ShouldMatch']
    system_matches = training_df['SystemMatch']


    acc = accuracy_score(gold_matches, system_matches)
    print(threshold, acc)