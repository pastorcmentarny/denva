import unittest

from server import rules_service


class RulesServiceTestCases(unittest.TestCase):

    def test_get_all_rules_should_random_rule_acceptance_test(self):
        # when
        random_rule = rules_service.get_random_rule()

        # then
        self.assertGreater(len(random_rule), 1)

        # debug
        print(random_rule)

    def test_get_random_rule_should_return_a_rule_acceptance_test(self):
        rule = rules_service.get_random_rule()
        self.assertNotEqual(rule, '')
        self.assertNotEqual(rule, None)


if __name__ == '__main__':
    unittest.main()
