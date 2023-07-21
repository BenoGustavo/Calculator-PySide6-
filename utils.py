import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')

def IsNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))

def removeOperators(equation:str):
    numbers = re.sub(r'[/*().\-+\^%]', '', equation)
    return numbers

def isValidNumber(string: str):
    try:
        if '(' in string:
            string = string.replace('(','')
        if ')' in string:
            string = string.replace(')','')

        float(string)
        return True
    except ValueError:
        return False
    
def isOperator(string: str):
    if string in '÷x-+^%':
        return True
    return False

def isEmpty(string: str):
    return string == ''

def deleteLastChar(string: str):
    if len(string) > 0:
        return string[:-1]
    else:
        return string
    
def addDotAfterZero(string: str):
    equation_list = list(string)

    # Insert the dot at the desired position (between index 1 and 2)
    equation_list.insert(2, '.')

    # Join the elements back into a string
    equation_with_dot = ''.join(equation_list)
    return equation_with_dot