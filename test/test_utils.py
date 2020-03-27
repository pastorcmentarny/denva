from unittest import TestCase

#DO NOT REMOVE 'from src import  *' as test do not run without this

import utils


class Test(TestCase):

    def test_get_int_number_from_text(self):
        self.assertEqual(utils.get_int_number_from_text('250MB'), 250)

    def test_get_float_number_from_text(self):
        self.assertEqual(utils.get_float_number_from_text('2.1 kB'), '2.1')
