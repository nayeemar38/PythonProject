import sys
import os

# Global variables
tokenList = []
variableDict = {}
nextToken = None
index = -1

# Constants for dictionary values
VALUE = 0
TYPE = 1

# Function to parse and evaluate a program
def program():
    global variableDict
    while index < len(tokenList) - 1:
        let_in_end()
    variableDict.clear()
    if nextToken == 'none':
        return
    else:
        sys.exit('Error')

# Function to handle a let-in-end block
def let_in_end():
    match('let')
    declaration_list()
    match('in')
    result_type = type()
    result = expression(result_type)
    match('end')
    if nextToken == ';':
        print(result)
    else:
        sys.exit('Error')

# Function to parse a list of variable declarations
def declaration_list():
    while nextToken != 'in':
        declaration()

# Function to parse and store a variable declaration
def declaration():
    global variableDict
    var_type, var_value = None, None
    var_name = nextToken
    consume_token()
    if nextToken == ':':
        consume_token()
        var_type = type()
        if nextToken == '=':
            consume_token()
            var_value = expression(var_type)
            match(';')
        else:
            sys.exit('Error: Wrong declaration format')
    else:
        sys.exit('Error: Wrong declaration format')
    variableDict[var_name] = (var_value, var_type)

# Function to parse and return the type of a variable
def type():
    if nextToken == 'int' or nextToken == 'real':
        return_value = nextToken
        consume_token()
        return return_value
    else:
        sys.exit('Error: Wrong type')

# Function to parse and evaluate an expression
def expression(expected_type):
    left_term = term(expected_type)
    while nextToken in ('+', '-', '*', '/'):
        operator = nextToken
        consume_token()
        right_term = term(expected_type)
        left_term = evaluate(left_term, operator, right_term)
    return left_term

# Function to parse and evaluate a term
def term(expected_type):
    left_factor = factor(expected_type)
    while nextToken in ('*', '/'):
        operator = nextToken
        consume_token()
        right_factor = factor(expected_type)
        left_factor = evaluate(left_factor, operator, right_factor)
    return left_factor

# Function to parse and evaluate a factor
def factor(expected_type):
    if nextToken == '(':
        consume_token()
        result = expression(expected_type)
        match(')')
        return result
    elif nextToken.isdigit() or (nextToken[0] == '-' and nextToken[1:].isdigit()):
        return cast_to_type(nextToken, expected_type)
    elif nextToken.isalpha():
        if nextToken in variableDict:
            var_value, var_type = variableDict[nextToken]
            if var_type == expected_type:
                consume_token()
                return var_value
            else:
                sys.exit('Error: Type mismatch')
        else:
            sys.exit(f'Error: Variable "{nextToken}" is not defined')
    else:
        sys.exit(f'Error: Unexpected factor: {nextToken}')

# Function to match the current token with an expected token
def match(expected_token):
    if expected_token == nextToken:
        consume_token()
    else:
        sys.exit(f'Error: Expected "{expected_token}", Got: {nextToken}')

# Function to consume the current token
def consume_token():
    global index, nextToken
    index += 1
    if index < len(tokenList):
        nextToken = tokenList[index]
    else:
        nextToken = 'none'

# Function to evaluate an arithmetic operation
def evaluate(left, operator, right):
    try:
        left = cast_to_numeric(left)
        right = cast_to_numeric(right)
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                sys.exit('Error: Division by zero')
            return left / right
        else:
            sys.exit('Error: Invalid operation')
    except ValueError:
        sys.exit('Error: Operands are not numeric')

# Function to cast a value to a specified type
def cast_to_type(value, expected_type):
    try:
        if expected_type == 'int':
            return int(value)
        elif expected_type == 'real':
            return float(value)
    except ValueError:
        sys.exit('Error: Type mismatch')

# Function to check if a value is numeric
def cast_to_numeric(value):
    if is_numeric(value):
        return value
    else:
        sys.exit('Error: Operands are not numeric')

# Function to check if a value is numeric
def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Main function to read the input file and start the parsing process
def main():
    global tokenList
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'sample.tiny.txt')

    try:
        with open(file_path, 'r') as file:
            tokenList = file.read().split()
            nextToken = tokenList[0]
            program()  # Start parsing the program
    except FileNotFoundError:
        sys.exit(f'Error: Input file "{file_path}" not found')

if __name__ == "__main__":
    main()
