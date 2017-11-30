import re

def noneorempty(object):
    return object == None or object == ""


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def get_google_stack_overflow_link():
    GOOGLE = "http://www.google.com/search?q=site:stackoverflow.com+"
    return GOOGLE


def get_google_math_exchange_link():
    GOOGLE = "http://www.google.com/search?q=site:math.stackexchange.com+"
    return GOOGLE


def get_feeling_lucky_suffix():
    SUFFIX = "&btnI"
    return SUFFIX


method_mapping = {
    "stackoverflow": get_google_stack_overflow_link,
    "mathexchange": get_google_math_exchange_link
}