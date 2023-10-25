import unittest

from src.parse_transformed_heiligenlex import match_saint_name, match_canonization, match_hlex_number, \
    match_second_hlex_number


class RegexExtractionTestCase(unittest.TestCase):
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

    def test_canonization_extraction(self):
        canonization = match_canonization("Adolius Oliverius")
        self.assertIsNone(canonization)

        canonization = match_canonization("Dimitri, Dmitri")
        self.assertIsNone(canonization)

        # NOTE: Try to handle this too if there is time
        canonization = match_canonization("S. Valabonsus")
        self.assertIsNotNone(canonization)

        # With Canonization
        canonization = match_canonization("Azirianus, SS.")
        self.assertEqual(canonization, "SS.")

        canonization = match_canonization("Maclongus, S.")
        self.assertEqual(canonization, "S.")

        canonization = match_canonization("Gurdianus, Criscentia cum aliis SS.")
        self.assertEqual(canonization, "SS.")

        # With numbers, no comma
        canonization = match_canonization("Abbo (4)")
        self.assertIsNone(canonization)

        canonization = match_canonization("Zozimus (6. 7)")
        self.assertIsNone(canonization)

        canonization = match_canonization("Caecus S. Pantaleonis, SS.")
        self.assertEqual(canonization, "SS.")

        canonization = match_canonization("Donatus, Secundus, Papias, SS. (4)")
        self.assertEqual(canonization, "SS.")

        # With Canonization and numbers
        canonization = match_canonization("Adrianus Becanus, S. (15)")
        self.assertEqual(canonization, "S.")

        canonization = match_canonization("Asclepiodorus, S. (3)")
        self.assertEqual(canonization, "S.")

        canonization = match_canonization("Virianus, S.S. (1-2)")
        self.assertEqual(canonization, "S.S.")

        canonization = match_canonization("Zoërardus, SS. (1-2)")
        self.assertEqual(canonization, "SS.")

        canonization = match_canonization("Elisabeth a S. Ludovico, B. (18)")
        self.assertEqual(canonization, "B.")

        canonization = match_canonization("Guilielmus Arnaldus BB. (28)")
        self.assertEqual(canonization, "BB.")

    def test_match_hlex_number(self):
        hlex_number = match_hlex_number("Adolius Oliverius")
        self.assertIsNone(hlex_number)

        # With numbers, no comma
        hlex_number = match_hlex_number("Abbo (4)")
        self.assertEqual(hlex_number, "(4)")

        hlex_number = match_hlex_number("Zozimus (6. 7)")
        self.assertEqual(hlex_number, "(6. 7)")

        hlex_number = match_hlex_number("Adrianus Becanus, S. (15)")
        self.assertEqual(hlex_number, "(15)")

        hlex_number = match_hlex_number("Virianus, S.S. (1-2)")
        self.assertEqual(hlex_number, "(1-2)")

    def test_match_second_hlex_number(self):
        second_hlex_number = match_second_hlex_number("Zetula, S.")
        self.assertIsNone(second_hlex_number)

        second_hlex_number = match_second_hlex_number("Zetula, S. [2]")
        self.assertEqual(second_hlex_number, "[2]")


if __name__ == "__main__":
    unittest.main()
