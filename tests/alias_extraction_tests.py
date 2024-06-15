import unittest

from src.preprocessing.heiligenlexikon.saint_alias_extraction import get_saint_aliases


class AlternativeNameSpellingTestCase(unittest.TestCase):
    def test_alternative_name_extraction(self):
        name = "Abda"
        text = "1S. Abdas, M. (31. März). Chald. Abda, d.i. Diener. – Der hl. Abdas, Martyrer in Afrika, litt mit dem hl. Anesus. S. "
        alternative_names = get_saint_aliases(name, text)
        self.assertEqual(alternative_names, ["Abdas"])

        name = "Kumman"
        text = "Mart. Taml. finden sich an verschiedenen Tagen 17 Heilige unter den Namen Cumman, Cuman, Cummin, Cummine, Cuimmine etc. verzeichnet, von denen jedoch nichts Näheres angegeben ist, und Einige bei uns schon aufgeführt sind als S. Cumenus, Cumianus, Cumineus, Cuminus, Cummenus und Cumminus. Die von uns am 29. Mai erwähnte Cumania findet sich dort am 29. Mai als Cumne, Vir., Inghen Alleain, in Aird Ulladh (The Ards, Down). – Auch 23 mit dem Namen Cronan finden sich dort an verschiedenen Tagen (vgl. die Note zu S. Cronanus5) und 16 mit dem Namen Cruimthir, von denen wir Einige als Crumtharus  und Crumtherus haben, so wie auch noch einige andere Namen, die wir aber übergehen wollen, da man doch etwas Näheres über sie zur Zeit nicht weiß. †"
        alternative_names = get_saint_aliases(name, text)
        self.assertEqual(
            alternative_names, ["Cuman", "Cumania", "Cumman", "Cummin", "Cummine"]
        )
