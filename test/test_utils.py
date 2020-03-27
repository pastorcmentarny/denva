import unittest

from src import  * #DO NOT REMOVE IT
import utils


class TestEngine(unittest.TestCase):


    def test_get_int_number_from_text(self):
        self.assertEqual(utils.get_int_number_from_text('250MB'), 250)

    def test_get_float_number_from_text(self):
        self.assertEqual(utils.get_float_number_from_text('2.1 kB'), '2.1')


if __name__ == '__main__':
    unittest.main()
