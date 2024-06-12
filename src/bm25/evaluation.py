import os

matching_results_path = "matching_results"


def calculate_metric_components_of_results(result_list: object) -> list:
    true_positives = []
    false_positives = []
    true_negatives = []
    false_negatives = []

    for prediction in result_list:
        prediction = prediction.rstrip()
        prediction_split = prediction.split(";")
        hlex_id = prediction_split[0]
        gold_standard_match = prediction_split[1]
        system_match = prediction_split[2]

        prediction_tuple = (hlex_id, gold_standard_match, system_match)

        # TODO use system match for identifying

        if gold_standard_match == "":
            if gold_standard_match == system_match:
                true_negatives.append(prediction_tuple)
            if gold_standard_match != system_match:
                false_positives.append(prediction_tuple)
        else:
            if gold_standard_match == system_match:
                true_positives.append(prediction_tuple)
            if gold_standard_match != system_match:
                if system_match == "":
                    false_negatives.append(prediction_tuple)
                else:
                    false_positives.append(prediction_tuple)
    return true_positives, true_negatives, false_positives, false_negatives


def calculate_metrics(tp, tn, fp, fn):
    accuracy = calculate_accuracy(
        true_positives=tp, true_negatives=tn, false_positives=fp, false_negatives=fn
    )
    precision = calculate_precision(true_positives=tp, false_positives=fp)
    recall = calculate_recall(true_positives=tp, false_negatives=fn)
    return accuracy, precision, recall


# Accuracy = (TP + TN) / (TP + TN + FP + FN)
def calculate_accuracy(
        true_positives: int, true_negatives: int, false_positives: int, false_negatives
):
    return (true_positives + true_negatives) / (
            true_positives + true_negatives + false_positives + false_negatives
    )


# TODO doublecheck
def calculate_precision(true_positives: int, false_positives: int):
    return true_positives / (true_positives + false_positives)


# TODO doublecheck
def calculate_recall(true_positives: int, false_negatives: int):
    return true_positives / (true_positives + false_negatives)


def get_metric_components_from_result_file(filepath: str):
    with open(current_path, encoding="utf-8") as current_file:
        results = current_file.readlines()
        (
            true_positives,
            true_negatives,
            false_positives,
            false_negatives,
        ) = calculate_metric_components_of_results(result_list=results)
        return true_positives, true_negatives, false_positives, false_negatives


def write_metric_component_entries_to_str(metric_component_list: str):
    result_string = ""
    for entry_tuple in metric_component_list:
        result_string += (
                ";".join([entry_tuple[0], entry_tuple[1], entry_tuple[2]]) + "\n"
        )
    return result_string


if __name__ == "__main__":
    for result_file in os.listdir(matching_results_path):
        current_path = os.path.join(matching_results_path, result_file)

        (
            true_positives,
            true_negatives,
            false_positives,
            false_negatives,
        ) = get_metric_components_from_result_file(current_path)

        tp_count = len(true_positives)
        fp_count = len(false_positives)
        tn_count = len(true_negatives)
        fn_count = len(false_negatives)

        accuracy, precision, recall = calculate_metrics(
            tp=tp_count, fp=fp_count, tn=tn_count, fn=fn_count
        )
        print(
            f"Accuracy of file: {result_file}: Acc: {accuracy}, P: {precision}, R: {recall} "
        )
        print("True positives", true_positives)

        evaluation_dir = "evaluation"
        evaluation_filename = result_file.split(".")[0] + "_eval.csv"
        eval_file_path = os.path.join(evaluation_dir, evaluation_filename)
        with open(eval_file_path, encoding="utf-8", mode="w") as output_file:
            output_string = (
                    "File;Accuracy;Precision;Recall\n"
                    + ";".join([result_file, str(accuracy), str(precision), str(recall)])
                    + "\n"
            )
            output_string += "\n;Gold Standard Match; System Match"
            output_string += "\nTrue Positives\n"
            output_string += write_metric_component_entries_to_str(true_positives)
            output_string += "\nTrue Negatives\n"
            output_string += write_metric_component_entries_to_str(true_negatives)
            output_string += "\nFalse Positives\n"
            output_string += write_metric_component_entries_to_str(false_positives)
            output_string += "\nFalse Negatives\n"
            output_string += write_metric_component_entries_to_str(false_negatives)

            output_file.write(output_string)
