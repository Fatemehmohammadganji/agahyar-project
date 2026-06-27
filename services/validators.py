import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def iranian_phone_number_validator(value):
    if not re.match(r"^09\d{9}$", value):
        raise ValidationError(
            _("Phone number must be 11 digits and start with 09."),
        )
