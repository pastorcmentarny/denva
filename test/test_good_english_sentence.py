import unittest

from server import good_english_sentence


class EnglishSentenceTestCases(unittest.TestCase):

    # stupid test but useful for my flaky mind
    def test_get_random_english_sentence_(self):
        # when
        for i in range(1, 100):
            result = good_english_sentence.get_random_english_sentence()

            # then it is not produce config.EMPTY result or out of index crash
            self.assertTrue(result)
