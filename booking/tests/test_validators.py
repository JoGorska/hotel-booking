'''
each class tests each validator for validaton of incorrect
data as well as correct data
'''

from ..validators import (
    EmailValidator, ReturningClientOptionsValidator,
    NewClientOptionsValidator
)
from ..client_options import ClientOptions

NUMBERS = 123456
EMPTY_STRING = ''
RANDOM_LETTERS = 'asdf ghjkl'


class TestEmailValidator:
    good_data = 'test@email.me'
    bad_data_2 = 'bad@email'

    def test_raises_error_when_email_incorrect_format(self):
        result = EmailValidator(
            validated_object=self.bad_data_2,
            object_type='email').result
        assert result is False

    def test_raises_error_when_given_random_string(self):
        result = EmailValidator(
            validated_object=RANDOM_LETTERS,
            object_type='email').result
        assert result is False

    def test_raises_error_when_given_random_numbers(self):
        result = EmailValidator(
            validated_object=NUMBERS,
            object_type='email').result
        assert result is False

    def test_passes_good_email(self):
        result = EmailValidator(
            validated_object=self.good_data,
            object_type='email').result
        assert result is True

    def test_fails_on_empty_string(self):
        result = EmailValidator(
            validated_object=EMPTY_STRING,
            object_type='email').result
        assert result is False

class TestNewClientOptionsValidator:
    def test_passes_option_add(self):
        result = NewClientOptionsValidator(
            validated_object=ClientOptions.ADD,
            object_type='option'
        ).result
        assert result is True

    def test_passes_option_show(self):
        result = NewClientOptionsValidator(
            validated_object=ClientOptions.SHOW,
            object_type='option'
        ).result
        assert result is True

    def test_fails_option_print(self):
        result = NewClientOptionsValidator(
            validated_object=ClientOptions.PRINT,
            object_type='option'
        ).result
        assert result is False

    def test_fails_option_change(self):
        result = NewClientOptionsValidator(
            validated_object=ClientOptions.CHANGE,
            object_type='option'
        ).result
        assert result is False

    def test_fails_option_cancel(self):
        result = NewClientOptionsValidator(
            validated_object=ClientOptions.CANCEL,
            object_type='option'
        ).result
        assert result is False

    def test_passes_option_quit(self):
        result = NewClientOptionsValidator(
            validated_object=ClientOptions.QUIT,
            object_type='option'
        ).result
        assert result is True

    def test_fails_option_random_numbers(self):
        result = NewClientOptionsValidator(
            validated_object=NUMBERS,
            object_type='option'
        ).result
        assert result is False

    def test_fails_option_empty_string(self):
        result = NewClientOptionsValidator(
            validated_object=EMPTY_STRING,
            object_type='option'
        ).result
        assert result is False

    def test_fails_option_random_letters(self):
        result = NewClientOptionsValidator(
            validated_object=RANDOM_LETTERS,
            object_type='option'
        ).result
        assert result is False


class TestReturningClientOptionsValidator:
    def test_passes_option_add(self):
        result = ReturningClientOptionsValidator(
            validated_object=ClientOptions.ADD,
            object_type='option'
        ).result
        assert result is True

    def test_passes_option_show(self):
        result = ReturningClientOptionsValidator(
            validated_object=ClientOptions.SHOW,
            object_type='option'
        ).result
        assert result is True

    def test_passes_option_print(self):
        result = ReturningClientOptionsValidator(
            validated_object=ClientOptions.PRINT,
            object_type='option'
        ).result
        assert result is True

    def test_passes_option_change(self):
        result = ReturningClientOptionsValidator(
            validated_object=ClientOptions.CHANGE,
            object_type='option'
        ).result
        assert result is True

    def test_passes_option_cancel(self):
        result = ReturningClientOptionsValidator(
            validated_object=ClientOptions.CANCEL,
            object_type='option'
        ).result
        assert result is True

    def test_passes_option_quit(self):
        result = ReturningClientOptionsValidator(
            validated_object=ClientOptions.QUIT,
            object_type='option'
        ).result
        assert result is True

    def test_fails_option_random_numbers(self):
        result = ReturningClientOptionsValidator(
            validated_object=NUMBERS,
            object_type='option'
        ).result
        assert result is False

    def test_fails_option_empty_string(self):
        result = ReturningClientOptionsValidator(
            validated_object=EMPTY_STRING,
            object_type='option'
        ).result
        assert result is False

    def test_fails_option_random_letters(self):
        result = ReturningClientOptionsValidator(
            validated_object=RANDOM_LETTERS,
            object_type='option'
        ).result
        assert result is False
