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

# Separate the females with duplicate names
sorted_saints_df_females_duplicate_names = sorted_saints_df_females[
    sorted_saints_df_females.duplicated(keep=False, subset="SaintName")
]
duplicate_female_names = sorted_saints_df_females_duplicate_names["SaintName"].unique()

sorted_females_no_duplicate_names = sorted_saints_df_females[
    ~sorted_saints_df_females["SaintName"].isin(duplicate_female_names)
]

# Separate the males with duplicate names
sorted_saints_df_males_duplicate_names = sorted_saints_df_males[
    sorted_saints_df_males.duplicated(keep=False, subset="SaintName")
]
duplicate_male_names = sorted_saints_df_males_duplicate_names["SaintName"].unique()

sorted_males_no_duplicate_names = sorted_saints_df_males[
    ~sorted_saints_df_males["SaintName"].isin(duplicate_male_names)
]

males_no_duplicates_sample = sorted_males_no_duplicate_names.sample(
    n=40, random_state=1
)
females_no_duplicates_sample = sorted_females_no_duplicate_names.sample(
    n=40, random_state=1
)

males_with_duplicates_sample = sorted_saints_df_males_duplicate_names.sample(
    n=10, random_state=1
)
females_with_duplicates_sample = sorted_saints_df_females_duplicate_names.sample(
    n=10, random_state=1
)

gold_standard_set_df = pd.concat(
    [
        males_no_duplicates_sample,
        males_with_duplicates_sample,
        females_no_duplicates_sample,
        females_with_duplicates_sample,
    ],
    sort=False,
)

gold_standard_set_df.to_json("gold_standard.json", orient="index")


print(saints_df)
