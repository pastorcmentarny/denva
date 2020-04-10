import io
import sys
import utils

from unittest import TestCase
from zeroeighttrack import leaderboard_ui


class LeaderboardUITest(TestCase):

    def test_show_on_cli(self):
        # given
        date = utils.get_timestamp_title(False)
        data = [{
            'date': '31.3',
            'time': '26.21.9',
            'lap': 1,
            'id': 2
        }, {
            'date': '30.3',
            'time': '30.53.1',
            'lap': 1,
            'id': 1
        }]
        expected_result = """Current Highscore Table {}
Id:2 @ 31.3 [Lap:1]...... 26.21.9 ds.
Id:1 @ 30.3 [Lap:1]...... 30.53.1 ds.
-----------------------------------------
Zeroeight Track Info: Length: 2.6km. Ascent: 55m
""".format(date)

        # when
        result = leaderboard_ui.generate_highscore_as_text(data)

        # then
        self.assertEqual(utils.to_multiline(result), expected_result)  # Now works as before.
