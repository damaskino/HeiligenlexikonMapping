import pandas as pd


df = pd.read_json("../../outputs_to_review/parsed_heiligenlexikon.json", orient="index")

# get only the saints
saints_df = df[
    (df["CanonizationStatus"] == "S.")
    | (df["CanonizationStatus"] == "SS.")
    | (df["CanonizationStatus"] == "S.S.")
    ]


def sort_df_by_entry_length(input_df):
    return input_df.sort_values(by=["EntryLength"])


def split_df_by_gender(input_df):
    males = input_df[input_df["Gender"] == "Masc"]
    females = input_df[input_df["Gender"] == "Fem"]
    neutrals = input_df[input_df["Gender"] == "Neut"]
    return males, females, neutrals


def separate_duplicate_names_df(input_df):
    duplicate_names_df = input_df[input_df.duplicated(keep=False, subset="SaintName")]
    duplicate_names = duplicate_names_df["SaintName"].unique()
    df_without_duplicate_names = input_df[~input_df["SaintName"].isin(duplicate_names)]
    return df_without_duplicate_names, duplicate_names_df


def remove_sampled_df(input_df, sampled_df):
    input_df = pd.concat([input_df, sampled_df])
    reduced_df = input_df[~input_df.index.duplicated(keep=False)]
    return reduced_df


sorted_saints_df = sort_df_by_entry_length(saints_df)

(
    sorted_saints_df_males,
    sorted_saints_df_females,
    sorted_saints_df_neut,
) = split_df_by_gender(sorted_saints_df)

# Separate the females with duplicate names
(
    sorted_females_no_duplicate_names,
    sorted_saints_df_females_duplicate_names,
) = separate_duplicate_names_df(sorted_saints_df_females)

# Separate the males with duplicate names
(
    sorted_males_no_duplicate_names,
    sorted_saints_df_males_duplicate_names,
) = separate_duplicate_names_df(sorted_saints_df_males)


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

# To expand our dataset we are sampling some more
# first we remove the entries from the first pass
reduced_males_without_duplicates = remove_sampled_df(sorted_males_no_duplicate_names, males_no_duplicates_sample)
reduced_females_without_duplicates = remove_sampled_df(sorted_females_no_duplicate_names, females_no_duplicates_sample)

reduced_males_with_duplicates = remove_sampled_df(sorted_saints_df_males_duplicate_names, males_with_duplicates_sample)
reduced_females_with_duplicates = remove_sampled_df(sorted_saints_df_females_duplicate_names,
                                                    females_with_duplicates_sample)

# Now we sample again

males_no_duplicates_part2 = reduced_males_without_duplicates.sample(
    n=40, random_state=1
)
males_with_duplicates_part2 = reduced_males_with_duplicates.sample(n=10, random_state=1)

females_no_duplicates_part2 = reduced_females_without_duplicates.sample(
    n=40, random_state=1
)
females_with_duplicates_part2 = reduced_females_with_duplicates.sample(
    n=10, random_state=1
)

gold_standard_set_part2_df = pd.concat(
    [
        males_no_duplicates_part2,
        males_with_duplicates_part2,
        females_no_duplicates_part2,
        females_with_duplicates_part2,
    ],
    sort=False,
)

gold_standard_set_df.to_json("gold_standard.json", orient="index")
gold_standard_set_part2_df.to_json("gold_standard_part2.json", orient="index")
