from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify as django_slugify
from tidylib import tidy_document

alphabet = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
    'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
    'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
    'я': 'ya'
}


def slugify(s):
    """
    Transliterate string to slug for cyrillic alphabet.

    :param s: string to transliterate.
    :return: transliterated string.
    """
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


def code_validator(value):
    """
    Validate HTML code.

    :param value: HTML code.
    :return: None or raise ValidationError.
    """
    document, errors = tidy_document(value, options={
        "output-xhtml": True,  # Output XHTML.
        "numeric-entities": True,  # Use numeric entities instead of named entities.
        "doctype": "omit",  # To ignore <!DOCTYPE html> missing warning.
        "show-body-only": True,  # To ignore inserting implicit <body> tag and missing <title> tag warnings.
    })
    if errors:
        print(errors)
        raise ValidationError(errors)
