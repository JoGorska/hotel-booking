from .mock_input_output import set_keyboard_input, get_display_output
from ..user_inputs import UserInput
from .fixtures import get_tomorrow, get_date_in_three_days, get_date_in_a_week


class TestStartDateInput:
    def test_date_tomorrow(self):
        tomorrow = get_tomorrow()
        set_keyboard_input([tomorrow])
        UserInput.start_date()
        output = get_display_output()
        assert len(output) > 0
        assert 'Your date is in valid format' in output[2]

    def test_date_in_a_week(self):
        date_in_a_week = get_date_in_a_week()
        set_keyboard_input([date_in_a_week])
        UserInput.start_date()
        output = get_display_output()
        assert len(output) > 0
        assert 'Your date is in valid format' in output[2]


class TestEndDateInput:
    def test_end_date_in_a_week(self):
        tomorrow = get_tomorrow()
        date_in_a_week = get_date_in_a_week()
        set_keyboard_input([date_in_a_week])
        UserInput.end_date(tomorrow)
        output = get_display_output()
        assert len(output) > 0
        assert 'Your date is in valid format' in output[2]

    def test_date_in_three_days(self):
        tomorrow = get_tomorrow()
        date_in_three_days = get_date_in_three_days()
        set_keyboard_input([date_in_three_days])
        UserInput.end_date(tomorrow)
        output = get_display_output()
        assert len(output) > 0
        assert 'Your date is in valid format' in output[2]
