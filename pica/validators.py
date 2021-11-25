from django.core.exceptions import ValidationError


def validate_empty(value):
    if value == "":
        raise ValidationError("{} tidak boleh dikosongkan.".format(value))
