__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "24.03.2018"
__app__ = "django_rest_social"
__status__ = "Development"

import math
import re

from django.utils.html import strip_tags


def count_words(html_string):
    string = strip_tags(html_string)
    match_words = re.findall(r'\w+', string)
    count = len(match_words)
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    read_time_minutes = math.ceil(count / 100.0)
    return int(read_time_minutes)
