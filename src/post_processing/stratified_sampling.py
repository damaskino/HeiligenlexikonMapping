import pandas as pd

df = pd.read_json("../../outputs_to_review/parsed_heiligenlexikon.json", orient="index")

# get only the saints
saints_df = df[
    (df["CanonizationStatus"] == "S.")
    | (df["CanonizationStatus"] == "SS.")
    | (df["CanonizationStatus"] == "S.S.")
    ]

sorted_saints_df = saints_df.sort_values(by=["EntryLength"])

sorted_saints_df_males = sorted_saints_df[sorted_saints_df["Gender"] == "Masc"]

sorted_saints_df_females = sorted_saints_df[sorted_saints_df["Gender"] == "Fem"]

sorted_saints_df_neut = sorted_saints_df[sorted_saints_df["Gender"] == "Neut"]

males_sample = sorted_saints_df_males.sample(n=50, random_state=1)
females_sample = sorted_saints_df_females.sample(n=50, random_state=1)

males_sample.to_json("males_sample.json", orient="index")
males_sample.to_csv("males_sample.csv")

females_sample.to_json("females_sample.json", orient="index")
females_sample.to_csv("females_sample.csv")

print(saints_df)
