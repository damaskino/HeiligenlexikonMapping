import random


# load and Remove the devset and goldstandard entries
def load_goldstandard_ids():
    with open(
        "../../data/2_annotated_data_gold_and_dev/gold_standard_hand_annotated_eschbach_li.txt",
        "r",
    ) as gold_standard_file:
        entry_ids = []
        for line in gold_standard_file.readlines():
            if len(line) == 0 or ";" not in line or line.startswith("#"):
                continue
            else:
                entry_ids.append(line.split(";")[0])
        return entry_ids


def load_devset_ids():
    with open(
        "../../data/2_annotated_data_gold_and_dev/dev_set.txt", "r"
    ) as gold_standard_file:
        entry_ids = []
        for line in gold_standard_file.readlines():
            entry_ids.append(line.split(";")[0])
        return entry_ids


# Use the rulebased matches as a baseline to build a training set
def load_rulebased_results(ids_to_remove: list):
    with open(
        "matching_results/match_results_edit_dist_thresh_100_feast_tolerance_0_devmode_False.csv"
    ) as result_file:
        result_list = result_file.readlines()
        random.seed(1)
        random.shuffle(result_list)
        print(result_list)

        wholeset_string = ""
        for match_line in result_list:
            entry_id = match_line.split(";")[0]
            match = match_line.split(";")[2].rstrip()
            entry_link = (
                "https://damaskino.github.io/HeiligenlexikonMapping?id=" + entry_id
            )
            match_link = "https://www.wikidata.org/wiki/" + match

            if entry_id in ids_to_remove or len(match.strip()) == 0:
                continue
            else:
                wholeset_string += (
                    ";".join([entry_id, match, entry_link, match_link]) + "\n"
                )

        with open(
            "wholeset_match_results_edit_thresh_100_feast_0.csv", "w"
        ) as wholeset_file:
            wholeset_file.write(wholeset_string)


if __name__ == "__main__":
    gold_ids = load_goldstandard_ids()
    dev_ids = load_devset_ids()
    ids_to_remove = gold_ids + dev_ids
    load_rulebased_results(ids_to_remove=ids_to_remove)
