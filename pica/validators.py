from django.core.exceptions import ValidationError


# Digunakan untuk memvalidasi fields yang ada di models.py

def validate_empty(value):
    if value == "":
        raise ValidationError("{} tidak boleh dikosongkan.".format(value))
