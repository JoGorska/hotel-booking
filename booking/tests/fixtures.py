from datetime import datetime, timedelta


NUMBERS = 123456
EMPTY_STRING = ''
RANDOM_LETTERS = 'asdf ghjkl'


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