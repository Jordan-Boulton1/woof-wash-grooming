import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Validators():

    def validate_string_input(value):
        """
        This validator checks if a given string contains only letters (a-z, A-Z).
        If the string contains anything other than letters, it raises a ValidationError.
        """
        # You can use regular expressions to validate the input.
        if not re.match("^[a-zA-Z]+$", value):
            raise ValidationError(_("This field must contain only letters."))
    
    def validate_phone_number(value):
        """
        This validator checks if a given string contains only digits (0-9).
        If the string contains anything other than digits, it raises a ValidationError.
        """
        # Validate phone number (simple example: ensuring it contains only digits)
        if not re.match(r"^\d+$", value):
            raise ValidationError("Phone number can contain only digits.")