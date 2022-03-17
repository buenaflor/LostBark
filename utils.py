import re


def remove_nonnumeric_chars(s):
    return re.sub("[^0-9]", "", s)


def get_first_occurrence(arr, _s):
    return next(s for s in arr if _s in s)
