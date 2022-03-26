from src.models.model import *
import unittest


class TestModel(unittest.TestCase):
    def test_generate_exp_data(self):
        exponent = 2
        base = 2
        exp_data = generate_exp_data(base, exponent)
        self.assertEqual(exp_data[1][0], 0)
        self.assertEqual(exp_data[1][-1], 400)
        self.assertEqual(exp_data[0][0], 0)
        self.assertEqual(exp_data[0][-1], 10)
