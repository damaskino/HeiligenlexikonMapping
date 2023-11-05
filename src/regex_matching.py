import re


def match_saint_name(raw_term: str) -> str:
    saint_name = None
    gender = None
    saint_pattern = r"((\w|\s|-)+\w)\,?\(?"
    saint_match = re.search(saint_pattern, raw_term)
    if saint_match:
        saint_name = saint_match.group(1)

    else:
        print("No match found for ", raw_term)
    return saint_name


def match_canonization(raw_term: str) -> str:
    canonization_pattern = r"(((S|V|B)+\.+)+)"
    canonization_status = None

    # If term has one or multiple commas, only take the last part and
    # assume canonization is in there
    if "," in raw_term:
        parts = raw_term.split(",")
        raw_term = parts[-1]

    canonization_match = re.search(canonization_pattern, raw_term)
    if canonization_match:
        canonization_status = canonization_match.group()

    # For "Caecus S. Pantaleonis, SS."
    if "S." in raw_term and "SS." in raw_term:
        canonization_status = "SS."

    return canonization_status


def match_hlex_number(raw_term: str) -> str:
    number_pattern = r"\([0-9\-\s\.]*\)"
    hlex_number = None
    num_match = re.search(number_pattern, raw_term)
    if num_match:
        hlex_number = num_match.group()
    return hlex_number


def match_second_hlex_number(raw_term: str) -> str:
    second_hlex_number_pattern = r"\[.*\]"
    second_hlex_number = None
    second_hlex_number_match = re.search(second_hlex_number_pattern, raw_term)
    if second_hlex_number_match:
        second_hlex_number = second_hlex_number_match.group()
    return second_hlex_number


def match_feast_day(raw_paragraph: str) -> str:
    feast_day_pattern = r"\(.?[0-9][0-9]?.*?\)"
    feast_day = None

    feast_day_match = re.search(feast_day_pattern, raw_paragraph)
    if feast_day_match:
        feast_day = feast_day_match.group()
    return feast_day
