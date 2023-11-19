from thefuzz import fuzz


# Wraps around rapidfuzz, which calculates indel distance, which is equivalent to Levenshtein
# with substitution cost 2
# https://maxbachmann.github.io/RapidFuzz/Usage/distance/Indel.html#normalized-distance
# the ratio provides a normalized value using: 1 - (distance / (len1 + len2))
#


def get_saint_aliases(name, input_text):
    threshold = 60
    tokens = input_text.strip().replace(",", "").split(" ")
    alternative_spellings = [n for n in tokens if fuzz.ratio(name, n) > threshold]
    alternative_spellings = list(set(alternative_spellings))
    if name in alternative_spellings:
        alternative_spellings.remove(name)
    cleaned_aliases = sorted([name for name in alternative_spellings if name.istitle()])

    return cleaned_aliases


# todo: maybe try doublemetaphone too
