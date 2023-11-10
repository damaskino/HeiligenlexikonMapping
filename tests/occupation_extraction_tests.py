import unittest

from bs4 import BeautifulSoup

from src.occupation_extraction import extract_occupation, setup_occupation_dict, get_occupation_category
from src.parse_transformed_heiligenlex import setup_occupation_list


class OccupationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.occupation_list = setup_occupation_list("../resources/occupation_list.txt")
        cls.occupation_dict = setup_occupation_dict("../resources/occupation_list.txt")

    def test_occupation_extraction(self):
        text = "S. Adalardus (Adalhardus), Abb. (2. Jan.), ein Abt zu Corbei in der Picardie. S."
        occupation = extract_occupation(
            paragraph_text=text, occupation_list=self.occupation_list
        )
        self.assertEqual(occupation, "Abb.")
        category = get_occupation_category(occupation, self.occupation_dict)
        self.assertEqual(category, "AbtIssin")

        text = "Actus, Ep. (22. Mai). Der Bischof Actus, den Buc. unter die »Heiligen« zählt, war aus Spanien gebürtig und kam um das Jahr 1125 nach Rom, wo ihm das herrliche Tugendbeispiel der Vallumbrosianer so wohl gefiel, daß er in ihren Orden einzutreten begehrte. Hier zeichnete er sich durch seine Heiligkeit dergestalt aus, daß er nach 5 Jahren zum Abt und später zum Ordensgeneral gewählt wurde. Bald darauf wurde er gegen seinen Willen, auf die Bitte der Einwohner von Pistoja, vom Papst Innocenz II. zum Bischofe dieser Kirche erhoben, in welcher Würde er nicht das Geringste in seiner frühern Lebensweise änderte. Nach zwanzigjähriger segensreicher Verwaltung seines bischöflichen Amtes starb er im Jahre 1155. Bei seinem Grabe geschahen viele Wunder und noch nach 184 Jahren fand man seinen Leib unversehrt. Im Orden der Vallumbrosianer wird sein Andenken auf das Feierlichste begangen. (Buc.)"
        occupation = extract_occupation(
            paragraph_text=text, occupation_list=self.occupation_list
        )
        self.assertEqual(occupation, "Ep.")
        category = get_occupation_category(occupation, self.occupation_dict)
        self.assertEqual(category, "Bischof")
        # soup = BeautifulSoup(entry, features="xml")
        # soup.text

        text = "»Wunderbar ist Gott in Seinen Heiligen.«Psalm 67, 36."
        occupation = extract_occupation(
            paragraph_text=text, occupation_list=self.occupation_list
        )
        self.assertIsNone(occupation)
        category = get_occupation_category(occupation, self.occupation_dict)
        self.assertIsNone(category)

        text = "2S. Aaron, Abb. (22. al. 21. Juni). Der hl. Abt Aaron ward gegen das Ende des fünften Jahrhunderts in England geboren,  und kam nach Frankreich, wo er in der Bretagne auf einer der Stadt Aletha gegenüber liegenden Insel, die von ihm den Namen Monke (Monachus) oder Arem (Aaron) erhielt, einem Kloster vorstand. Als der hl. Machutus (St. Malo) von England aus nach Frankreich überschiffen wollte, um daselbst den Glauben zu predigen, fand er am Ufer ein Schifflein, auf welchem der Heiland in Menschengestalt sich befand. Der Herr lud ihn zu sich auf das Schifflein ein und führte ihn über das Meer, sprechend: »Es ist auf diesem Meere eine Insel, die ein Mönch bewohnt, mit Namen Aaron; zu diesem will ich dich durch meinen Engel geleiten und er wird dich auf das Liebreichste empfangen.« So geschah es auch. Aaron empfing diesen Heiligen auf eine Weise, wie man es von einem wahren Diener Gottes erwarten mußte, und theilte mit ihm die Ehre des Apostelamtes. Er starb in der Mitte des sechsten Jahrhunderts und wird sein Fest in dem Bisthume St. Malo am 22. Juni gefeiert. (An andern Orten am 21. Juni.) Vorzüglich wird er aber im Bisthume St. Brieux verehrt, woselbst auch eine Pfarrkirche ist, die seinen Namen trägt."
        occupation = extract_occupation(
            paragraph_text=text, occupation_list=self.occupation_list
        )
        self.assertEqual(occupation, 'Abb.')
        category = get_occupation_category(occupation, self.occupation_dict)
        self.assertEqual(category, "AbtIssin")

if __name__ == "__main__":
    unittest.main()
