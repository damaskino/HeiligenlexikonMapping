import unittest

import stanza

from src.parse_transformed_heiligenlex import predict_gender


class OccupationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        stanza.download("de")
        nlp = stanza.Pipeline(
            lang="de", processors='tokenize,mwt,pos'
        )
        cls.nlp = nlp

    def test_predict_gender(self):
        gender = predict_gender("Aaron", self.nlp)
        self.assertEqual(gender, "Masc")
