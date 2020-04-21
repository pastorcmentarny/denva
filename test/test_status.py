import unittest

from common import status


class StatusCase(unittest.TestCase):
    def test_status_is_green(self):
        s = status.Status(2)

        # when
        result = s.get_status_as_light_colour()

        # then
        self.assertEqual('GREEN', result)

    def test_status_is_yellow(self):
        s = status.Status(1)

        # when
        result = s.get_status_as_light_colour()

        # then
        self.assertEqual('ORANGE', result)

    def test_status_is_red(self):
        s = status.Status(0)

        # when
        result = s.get_status_as_light_colour()

        # then
        self.assertEqual('RED', result)

    def test_status_set_to_warn(self):
        s = status.Status(2)

        # when
        s.set_warn()
        result = s.get_status_as_light_colour()

        # then
        self.assertEqual('ORANGE', result)

    def test_status_set_to_error(self):
        s = status.Status(2)

        # when
        s.set_error()

        # then
        self.assertEqual('RED', s.get_status_as_light_colour())

    def test_status_do_not_set_to_warn_if_status_is_set_to_error(self):
        s = status.Status(2)
        s.set_error()

        # when
        s.set_warn()

        # then
        self.assertEqual('RED', s.get_status_as_light_colour())
