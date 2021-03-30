from overseer import focus_timer

class FocusTimerTest(TestCase):
    def test_get_time_left_in_minutes_should_return(self):
    # given
    expected_result = '#ff800f'

    # when
    result = dom_utils.to_hex(255, 128, 15)

    # then
    self.assertEqual(expected_result, result)