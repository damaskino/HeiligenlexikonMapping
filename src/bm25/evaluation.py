import os

matching_results_path = "matching_results"

def calculate_metrics_of_results(result_list):
    true_positives = []
    false_positives = []
    true_negatives = []
    false_negatives = []

    for prediction in result_list:
        prediction = prediction.rstrip()
        prediction_split = prediction.split(';')
        hlex_id = prediction_split[0]
        gold_standard_match = prediction_split[1]
        system_match = prediction_split[2]

        prediction_dict = {hlex_id: [gold_standard_match, system_match]}

        if gold_standard_match == '':
            if gold_standard_match == system_match:
                true_negatives.append(prediction_dict)
            if gold_standard_match != system_match:
                false_positives.append(prediction_dict)
        else:
            if gold_standard_match == system_match:
                true_positives.append(prediction_dict)
            if gold_standard_match != system_match:
                if system_match == '':
                    false_negatives.append(prediction_dict)
                else:
                    false_positives.append(prediction_dict)
    tp = len(true_positives)
    tn = len(true_negatives)
    fp = len(false_positives)
    fn = len(false_negatives)
    accuracy = calculate_accuracy(true_positives=tp, true_negatives=tn, false_positives=fp, false_negatives=fn)
    precision = calculate_precision(true_positives = tp, false_positives=fn)
    recall = calculate_recall(true_positives= tp, false_negatives=fn)
    return accuracy, precision, recall

# Accuracy = (TP + TN) / (TP + TN + FP + FN)
def calculate_accuracy(true_negatives:int, true_positives:int, false_positives:int, false_negatives):
    return (true_positives + true_negatives) / (true_positives+true_negatives+false_positives+false_negatives)

def calculate_precision(true_positives:int, false_positives:int):
    return true_positives / (true_positives+false_positives)

def calculate_recall(true_positives:int, false_negatives:int):
    return true_positives / (true_positives+false_negatives)

for result_file in os.listdir(matching_results_path):
    current_path = os.path.join(matching_results_path, result_file)
    with open(current_path, encoding='utf-8') as current_file:
        results = current_file.readlines()
        accuracy, precision, recall = calculate_metrics_of_results(result_list=results)
        print(f"Accuracy of file: {current_file.name}: Acc: {accuracy}, P: {precision}, R: {recall} ")
