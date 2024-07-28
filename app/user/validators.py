"""
Define custom validators.
"""

from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^(\+\d{1,3})?\d{9,13}$", message="""Please enter a valid mobile number."""
)
