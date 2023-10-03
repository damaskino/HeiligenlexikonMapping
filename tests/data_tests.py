import sys
import unittest
from tqdm import tqdm
from src.parse_transformed_heiligenlex import HlexParser


# some tests to confirm some key assumptions about the data
class DataTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        hlex_parser = HlexParser()
        cls.soup = hlex_parser.load_transformed_hlex_to_soup()
        print("Loading soup...")
        cls.entries = cls.soup.find_all("entry")

    # make a pass through the data to ensure that all entries only contain one sense
    def test_ensure_singular_sense_in_entry(self):

        multiple_senses_found = False
        print("Checking entries for multiple senses...")
        for e in tqdm(self.entries):
            entry_id = e.get('xml:id')
            if len(e.find_all('sense')) > 1:
                print("Error: More than one sense found in entry!")
                multiple_senses_found = True

        self.assertFalse(multiple_senses_found)  # add assertion here

    def test_ensure_singular_terms_in_entry(self):

        multiple_terms_found = False
        print("Checking entries for multiple terms...")
        for e in tqdm(self.entries):
            entry_id = e.get('xml:id')
            if len(e.find_all('terms')) > 1:
                print("Error: More than one term found in entry!")
                multiple_terms_found = True
                break

        self.assertFalse(multiple_terms_found)

    def test_ensure_unique_entry_ids(self):

        print("Checking entries for duplicate ids...")
        duplicate_ids_found = False
        entry_ids = []
        for e in tqdm(self.entries):
            entry_id = e.get('xml:id')

            if entry_id in entry_ids:
                print("ERROR: Duplicate entry id found!", entry_id)
                duplicate_ids_found = True

            entry_ids.append(entry_id)

        self.assertFalse(duplicate_ids_found)


if __name__ == '__main__':
    unittest.main()
