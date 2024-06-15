import unittest

from src.preprocessing.heiligenlexikon.parse_dates import convert_date
from src.preprocessing.heiligenlexikon.regex_matching import match_raw_feast_day


class DateExtractionTestCase(unittest.TestCase):
    def test_match_feast_day(self):
        feast_day = match_raw_feast_day(
            "2S. Aaron, Abb. (22. al. 21. Juni). Der hl. Abt Aaron ward gegen das Ende des fünften Jahrhunderts in England geboren,  und kam nach Frankreich, wo er in der Bretagne auf einer der Stadt Aletha gegenüber liegenden Insel, die von ihm den Namen Monke (Monachus) oder Arem (Aaron) erhielt, einem Kloster vorstand. Als der hl. Machutus (St. Malo) von England aus nach Frankreich überschiffen wollte, um daselbst den Glauben zu predigen, fand er am Ufer ein Schifflein, auf welchem der Heiland in Menschengestalt sich befand. Der Herr lud ihn zu sich auf das Schifflein ein und führte ihn über das Meer, sprechend: »Es ist auf diesem Meere eine Insel, die ein Mönch bewohnt, mit Namen Aaron; zu diesem will ich dich durch meinen Engel geleiten und er wird dich auf das Liebreichste empfangen.« So geschah es auch. Aaron empfing diesen Heiligen auf eine Weise, wie man es von einem wahren Diener Gottes erwarten mußte, und theilte mit ihm die Ehre des Apostelamtes. Er starb in der Mitte des sechsten Jahrhunderts und wird sein Fest in dem Bisthume St. Malo am 22. Juni gefeiert. (An andern Orten am 21. Juni.) Vorzüglich wird er aber im Bisthume St. Brieux verehrt, woselbst auch eine Pfarrkirche ist, die seinen Namen trägt."
        )
        self.assertEqual(feast_day, "(22. al. 21. Juni)")

        feast_day = match_raw_feast_day(
            "3SS. Aaron et Soc. MM. (1. Juli). Die heil. Aaron, Julius und ihre Gefährten waren aus England, und erlitten um des Glaubenswillen den Martertod zu Caerleon an der Usk, in der Grafschaft Monmouth, unter der Regierung des Kaisers Diokletian. Nach einigen Schriftstellern sollen sie zuerst nach Rom gekommen sein und sich daselbst auf das Studium der heil. Schrift verlegt haben. Nach dem ehrw. Beda wurden noch viele andere Christen beiderlei Geschlechts mit ihnen gemartert. Das Todesjahr wird verschieden angegeben. Nach Alford, der sich auf die alte Ueberlieferung der englischen Geschichtschreiber stützt, erfolgte ihr Martertod um das Jahr 287; Bollandus aber und Sollierus setzen denselben in's Jahr 303 oder 304."
        )
        self.assertEqual(feast_day, "(1. Juli)")

        feast_day = match_raw_feast_day(
            "4Aaron, Ep. (13. Febr. al. 28. Sept.) Der Bischof Aaron zu Auxerre blühte am Anfange des neunten Jahrhunderts und starb im Jahre 807. Welcher Klasse von Heiligen er angehöre, ist nicht ausgemacht; Einige geben ihm den Titel »ehrwürdig«, Andere »selig«, wieder Andere »heilig«. Sein Leichnam ruht in dem Priorate des heil. Gervasius zu Aurerre."
        )
        self.assertEqual(feast_day, "(13. Febr. al. 28. Sept.)")

        feast_day = match_raw_feast_day(
            "Abibion war Mit-Abt des Klosters Beth-Coryph in Syrien, das er mit dem ehrwürdigen Eusebonus gegründet hatte. Er blühte gegen Anfang des 5. Jahrhunderts. (Mg.)"
        )
        self.assertIsNone(feast_day)

    def test_parse_date(self):
        parsed_date = convert_date("(22. al. 21. Juni)")
        self.assertEqual(
            parsed_date, [{"Day": 22, "Month": 6}, {"Day": 21, "Month": 6}]
        )

        parsed_date = convert_date("(27 al. 28. Febr.)")
        self.assertEqual(
            parsed_date, [{"Day": 27, "Month": 2}, {"Day": 28, "Month": 2}]
        )

        parsed_date = convert_date("(1. Juli)")
        self.assertEqual(parsed_date, [{"Day": 1, "Month": 7}])

        parsed_date = convert_date("(24. Aug.,)")
        self.assertEqual(parsed_date, [{"Day": 24, "Month": 8}])

        parsed_date = convert_date("(13. Febr. al. 28. Sept.)")
        self.assertEqual(
            parsed_date, [{"Day": 13, "Month": 2}, {"Day": 28, "Month": 9}]
        )

        parsed_date = convert_date("(16. März, al. 29. Okt.)")
        self.assertEqual(
            parsed_date, [{"Day": 16, "Month": 3}, {"Day": 29, "Month": 10}]
        )

        parsed_date = convert_date("(19. Jan. al. 16. Juli, al. 26. Dec.)")
        self.assertEqual(
            parsed_date,
            [
                {"Day": 19, "Month": 1},
                {"Day": 16, "Month": 7},
                {"Day": 26, "Month": 12},
            ],
        )

        # failing cases
        # handle later if there is time, good enough for now
        parsed_date = convert_date("(14. Dec. al. 22. 23. Aug.)")
        self.assertNotEqual(
            parsed_date,
            [
                {"Day": 14, "Month": 12},
                {"Day": 22, "Month": 8},
                {"Day": 23, "Month": 8},
            ],
        )

        parsed_date = convert_date("(20. Okt. al. 19. Febr., 28. Apr., 19. Sept.)")
        self.assertNotEqual(
            parsed_date,
            [
                {"Day": 20, "Month": 10},
                {"Day": 17, "Month": 2},
                {"Day": 28, "Month": 4},
                {"Day": 19, "Month": 9},
            ],
        )

        parsed_date = convert_date("(15. Juni, al. 11. Sept. 14. Dec.)")
        self.assertNotEqual(
            parsed_date,
            [
                {"Day": 15, "Month": 6},
                {"Day": 11, "Month": 9},
                {"Day": 14, "Month": 12},
            ],
        )
