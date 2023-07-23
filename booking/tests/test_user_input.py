'''
I am only able to test happy path for user input,
because invalid input leads to while loop,
invalid input is tested in test_validators
'''
from .mock_input_output import set_keyboard_input, get_display_output
from ..user_inputs import UserInput


def test_prompt_get_email():
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
