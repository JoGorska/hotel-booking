'''
each class tests each validator for validaton of incorrect
data as well as correct data
'''

from ..validators import EmailValidator


class TestEmailValidator:
    good_data = 'test@email.me'
    bad_data_1 = 'bad email'
    bad_data_2 = 'bad@email'
    bad_data_3 = 123366
    no_data = ''

    def test_raises_error_when_email_incorrect_format(self):
        result = EmailValidator(
            validated_object=self.bad_data_2,
            object_type='email').result
        assert result is False

    def test_raises_error_when_given_random_string(self):
        result = EmailValidator(
            validated_object=self.bad_data_1,
            object_type='email').result
        assert result is False

    def test_raises_error_when_given_random_numbers(self):
        result = EmailValidator(
            validated_object=self.bad_data_3,
            object_type='email').result
        assert result is False

    def test_passes_good_email(self):
        result = EmailValidator(
            validated_object=self.good_data,
            object_type='email').result
        assert result is True

    def test_fails_on_empty_string(self):
        result = EmailValidator(
            validated_object=self.no_data,
            object_type='email').result
        assert result is False

