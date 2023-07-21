from .mock_input_output import set_keyboard_input, get_display_output
from ..user_inputs import UserInput


def test_prompt_get_email():
    good_email = 'my_little@email.com'
    set_keyboard_input([good_email])
    UserInput.get_email()
    output = get_display_output()

    assert len(output) > 0
    assert output[0] == "Please enter your email address"
    assert output[1] == "Example: email@domain.uk\n"
    assert output[2] == 'Enter your email here: \n'
    assert output[3] == f'You entered "{good_email}"\n'
    assert 'Your email is valid' in output[4]  # colorama adding code to output

# zwiesza sie
# def test_prompt_get_email_wrong_email():
#     wrong_email = 'my_little.email.com'
#     set_keyboard_input([wrong_email])
#     UserPrompt.get_email()
#     output = get_display_output()

#     assert len(output) > 0
#     assert output[3] == f"You entered {wrong_email}\n"
#     assert 'll' in output[4]
