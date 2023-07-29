'''
I am only able to test happy path for user input,
because invalid input leads to while loop,
invalid input is tested in test_validators
'''
from .mock_input_output import set_keyboard_input, get_display_output
from ..user_inputs import UserInput


def test_user_input_email():
    good_email = 'my_little@email.com'
    set_keyboard_input([good_email])
    UserInput.email()
    output = get_display_output()

    assert len(output) > 0
    assert "Please enter your email address" in output[0]
    assert "Example: email@domain.uk\n" in output[0]
    assert output[1] == 'Enter your email here: \n'
    assert output[2] == f'You entered "{good_email}"\n'
    assert 'Your email is valid' in output[3]  # colorama adding code to output


class TestNewClientOptions:
    def test_option_add(self):
        set_keyboard_input(['add'])
        UserInput.new_client_option()
        output = get_display_output()
        assert len(output) > 0
        assert "Please choose one of the following options:" in output[0]
        assert "Your option is valid" in output[2]

    def test_option_show(self):
        set_keyboard_input(['show'])
        UserInput.new_client_option()
        output = get_display_output()
        assert len(output) > 0
        assert "Your option is valid" in output[2]

    def test_option_quit(self):
        set_keyboard_input(['quit'])
        UserInput.new_client_option()
        output = get_display_output()
        assert len(output) > 0
        assert "Your option is valid" in output[2]


class TestReturningClientOptions:
    def test_option_add(self):
        set_keyboard_input(['add'])
        UserInput.returning_client_option()
        output = get_display_output()
        assert len(output) > 0
        assert "Please choose one of the following options:" in output[0]
        assert "change your booking (change)," in output[0]
        assert "Your option is valid" in output[2]

    def test_option_show(self):
        set_keyboard_input(['show'])
        UserInput.returning_client_option()
        output = get_display_output()
        assert len(output) > 0
        assert "Your option is valid" in output[2]

    def test_option_quit(self):
        set_keyboard_input(['quit'])
        UserInput.returning_client_option()
        output = get_display_output()
        assert len(output) > 0
        assert "Your option is valid" in output[2]

    def test_option_print(self):
        set_keyboard_input(['print'])
        UserInput.returning_client_option()
        output = get_display_output()
        assert len(output) > 0
        assert "Your option is valid" in output[2]

    def test_option_change(self):
        set_keyboard_input(['change'])
        UserInput.returning_client_option()
        output = get_display_output()
        assert len(output) > 0
        assert "Your option is valid" in output[2]

    def test_option_cancel(self):
        set_keyboard_input(['cancel'])
        UserInput.returning_client_option()
        output = get_display_output()
        assert len(output) > 0
        assert "Your option is valid" in output[2]
