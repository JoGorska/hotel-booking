import re
from colorama import Fore
class Validator:

    def email(email):
        """
        Inside try raises ValueError if the email fails validation
        and returns False, prints information for the user about the error
        if no error - returns True
        validate email code and regex:
        https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
        """
        regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        try:
            if(not re.fullmatch(regex_email, email)):
                raise ValueError(f"The address '{email}' does not seem to be "
                                "correct")

        except ValueError as e:
            print(f"{Fore.RED}Invalid email: {e} please try again.\n")
            return False

        return True