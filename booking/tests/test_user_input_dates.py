from datetime import datetime, timedelta

from .mock_input_output import set_keyboard_input, get_display_output
from ..user_inputs import UserInput


def get_tomorrow():
    now = datetime.now()
    now_plus_1_day = now + timedelta(days=1)
    string = now_plus_1_day.strftime("%d/%m/%Y")
    print(string)
    return string

def get_date_in_three_days():
    now = datetime.now()
    now_plus_1_day = now + timedelta(days=3)
    string = now_plus_1_day.strftime("%d/%m/%Y")
    print(string)
    return string

def get_date_in_a_week():
    now = datetime.now()
    now_plus_7_days = now + timedelta(days=7)
    string = now_plus_7_days.strftime("%d/%m/%Y")
    return string


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
