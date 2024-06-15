import unittest

from src.wikification.evaluation import calculate_accuracy, calculate_precision


class MetricsTestCase(unittest.TestCase):
    def test_precision(self):
        tp = 2
        tn = 2

        precision = calculate_precision(tp, tn)
        self.assertAlmostEqual(precision, 0.5)
        self.assertNotAlmostEqual(precision, 0.6)
        self.assertNotAlmostEqual(precision, 0.51)
