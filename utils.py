import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')

def IsNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))

def isValidNumber(string: str):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
def isOperator(string: str):
    if string in '/*-+^':
        return True
    return False

def isEmpty(string: str):
    return string == ''