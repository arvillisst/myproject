import unidecode # pip install unidecode
from django.utils.text import slugify as _slugify, Truncator

def slugify(value, truncate_chars):
    '''Truncator и slugify - стандартные утилиты Django. Функция ограничивает текст до заданного количества символов.'''
    return Truncator(_slugify(unidecode.unidecode(value))).chars(truncate_chars, truncate='')