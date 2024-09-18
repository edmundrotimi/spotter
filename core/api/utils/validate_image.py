from django.core.exceptions import ValidationError

# utility to check model image size


def clean_image(value):
    filesize = value.size
    if filesize > 718848:
        raise ValidationError('Maximum file size is 700KB')
    return value
