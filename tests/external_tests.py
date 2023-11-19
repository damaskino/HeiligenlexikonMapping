import unittest

from thefuzz import fuzz
from rapidfuzz import fuzz as rfuzz
from rapidfuzz.distance import Levenshtein


class FuzzForEditRatioTestCase(unittest.TestCase):
    def test_thefuzz_ratio(self):
        ratio = fuzz.ratio("Hello", "Hello")
        self.assertEqual(ratio, 100)

        ratio = fuzz.ratio("Hullo", "Hello")
        self.assertEqual(ratio, 80)

        ratio = fuzz.ratio("Hollerö", "Hello")
        self.assertEqual(ratio, 50)

        # WHY?
        ratio = fuzz.ratio("Hollero", "Hello")
        self.assertEqual(ratio, 67)

    def test_rapidfuzz_ratio(self):
        ratio = rfuzz.ratio("Hollero", "Hello")
        self.assertEqual(round(ratio), 67)

    # the underlying implementation
    def test_rapidfuzz_levenshtein(self):
        distance = Levenshtein.distance("Hollerö", "Hello", weights=(1, 1, 2))
        print(distance)

        distance = Levenshtein.distance("Hollero", "Hello", weights=(1, 1, 2))
        print(distance)
