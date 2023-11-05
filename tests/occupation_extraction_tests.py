import unittest

from bs4 import BeautifulSoup

from src.parse_transformed_heiligenlex import setup_occupation_list


class OccupationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.occupation_list = setup_occupation_list()

    def test_occupation_extraction(self):
        entries = []
        with open("testcases/20_entries.txt", encoding="utf-8") as entries_file:
            entries_string = entries_file.read()
            entries = entries_string.split("\n#\n#\n#\n")

        for entry in entries:
            soup = BeautifulSoup(entry, features="xml")
            soup.text
            print("\n\n")

        print(len(entries))
        print(entries)


if __name__ == "__main__":
    unittest.main()
