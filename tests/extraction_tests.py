import unittest

from src.parse_transformed_heiligenlex import match_saint_name


class ExtractionTestCase(unittest.TestCase):

    def test_saint_name_extraction(self):
        # Name only
        saint_name = match_saint_name("Abesan")
        self.assertEqual(saint_name, "Abesan")

        saint_name = match_saint_name("Adolius Oliverius")
        self.assertEqual(saint_name, "Adolius Oliverius")

        saint_name = match_saint_name("Dimitri, Dmitri")
        self.assertEqual(saint_name, "Dimitri")

        # Name with hyphen
        saint_name = match_saint_name("Dubhtachus de Druim-dhearbb")
        self.assertEqual(saint_name, "Dubhtachus de Druim-dhearbb")

        # With Canonization
        saint_name = match_saint_name("Azirianus, SS.")
        self.assertEqual(saint_name, "Azirianus")

        saint_name = match_saint_name("Maclongus, S.")
        self.assertEqual(saint_name, "Maclongus")

        saint_name = match_saint_name("Gurdianus, Criscentia cum aliis SS.")
        self.assertEqual(saint_name, "Gurdianus")

        # With numbers, no comma
        saint_name = match_saint_name("Abbo (4)")
        self.assertEqual(saint_name, "Abbo")

        saint_name = match_saint_name("Adelheidis de Frauenberg (8)")
        self.assertEqual(saint_name, "Adelheidis de Frauenberg")

        saint_name = match_saint_name("Zozimus (6. 7)")
        self.assertEqual(saint_name, "Zozimus")

        # With Canonization and numbers
        saint_name = match_saint_name("Adrianus Becanus, S. (15)")
        self.assertEqual(saint_name, "Adrianus Becanus")

        saint_name = match_saint_name("Asclepiodorus, S. (3)")
        self.assertEqual(saint_name, "Asclepiodorus")

        saint_name = match_saint_name("Virianus, S.S. (1-2)")
        self.assertEqual(saint_name, "Virianus")

        saint_name = match_saint_name("Wilhelmus (67-68)")
        self.assertEqual(saint_name, "Wilhelmus")

        saint_name = match_saint_name("Zoërardus, SS. (1-2)")
        self.assertEqual(saint_name, "Zoërardus")


if __name__ == "__main__":
    unittest.main()
