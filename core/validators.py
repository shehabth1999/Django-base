from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class EG_PhoneNumberValidator:
    def __call__(self, value):
        if not value.isdigit():
            raise ValidationError(
                _('This is not a valid phone number'),
                params={'value': value},
            )

        if len(value) != 11:
            raise ValidationError(
                _('Phone Number must be 11 digits long'),
                params={'value': value},
            )

        if value[0] != '0' or value[1] != '1':
            raise ValidationError(
                _('Phone Number must start with 01'),
                params={'value': value},
            )

    def __eq__(self, other):
        return isinstance(other, EG_PhoneNumberValidator)

    def deconstruct(self):
        return ('core.validators.EG_PhoneNumberValidator', [], {})


class AlphabeticValidator:
    def __call__(self, value):
        # Strip leading/trailing spaces and split by spaces
        parts = value.strip().split()

        # Check if all parts contain only alphabetic characters
        if not all(part.isalpha() for part in parts):
            raise ValidationError(
                _('This field must contain only alphabetic characters and spaces between them.')
            )

    def __eq__(self, other):
        return isinstance(other, AlphabeticValidator)

    def deconstruct(self):
        return ('core.validators.AlphabeticValidator', [], {})
