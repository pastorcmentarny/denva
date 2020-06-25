import unittest

from src.delight import ui_utils


class MyTestCase(unittest.TestCase):
    def test_to_x_should_return_zero_for_15(self):
        # given
        x = 15
        # when
        result = ui_utils.to_x(x)
        self.assertEqual(result, 0)

