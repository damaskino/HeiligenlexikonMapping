from fuzzywuzzy import fuzz


def get_alternative_spellings(name, input_text):
    threshold = 60
    tokens = input_text.strip().replace(",", "").split(" ")
    alternative_spellings = [n for n in tokens if fuzz.ratio(name, n) > threshold]
    alternative_spellings = list(set(alternative_spellings))
    if name in alternative_spellings:
        alternative_spellings.remove(name)

    return alternative_spellings

# todo: maybe try doublemetaphone too
