def read_number(line, index):
    """Read a number from the line starting at the given index."""
    number = 0
    start = index
    while index < len(line) and (line[index].isdigit() or line[index] == "."):
        index += 1
    number = float(line[start: index])
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_plus(line, index):
    """Read a plus '+' sign from the line starting at the given index."""
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    """Read a minus '-' sign from the line starting at the given index."""
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiple(line, index):
    """Read a multiplication '*' sign from the line starting at the given index."""
    token = {'type': 'MULTIPLE'}
    return token, index + 1

def read_divide(line, index):
    """Read a division '/' sign from the line starting at the given index."""
    token = {'type': 'DIVIDE'}
    return token, index + 1

def read_parenthesis(line, index):
    """Read a parenthesis '(' or ')' from the line starting at the given index."""
    token = {'type': line[index]}
    return token, index + 1

def read_alpha(line, index):
    """Read an alphabetic operation from the line starting at the given index."""
    start = index
    while index < len(line) and line[index].isalpha():
        index += 1
    operation = line[start: index]
    token = {'type': operation}
    return token, index

def tokenize(line):
    """Convert the input line into a list of tokens."""
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index].isalpha():
            (token, index) = read_alpha(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
            # if unary minus, add a dummy zero before it
            if not tokens or tokens[-1]['type'] == "(":
                tokens.append({'type': 'NUMBER', 'number': 0})
        elif line[index] == '*':
            (token, index) = read_multiple(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(' or line[index] == ')':
            (token, index) = read_parenthesis(line, index)
        elif line[index] == ' ':
            index += 1
            continue
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def calculate(numbers, operations):
    """Perform a basic arithmetic calculation based on the last two numbers and the last operation."""
    if len(numbers) < 2 or not operations:
        return
    number2, number1 = numbers.pop(), numbers.pop()
    op = operations.pop()
    ans = 0
    if op == "PLUS":
        ans = number1 + number2
    elif op == "MINUS":
        ans = number1 - number2  
    elif op == "MULTIPLE":
        ans = number1 * number2        
    elif op == "DIVIDE":
        ans = number1 / number2  
    numbers.append(ans)

def perform_special_operation(numbers, operations):
    """Perform a special operation (abs, int, round) on the last number."""
    if len(numbers) < 1 or not operations:
        return    
    op = operations.pop()
    number = numbers.pop()
    ans = 0
    if op == "abs":
        ans = abs(number)
    elif op == "int":
        ans = int(number)     
    elif op == "round":
        ans = round(number) 
    numbers.append(ans)

def calcualte_parenthesis(numbers, operations):
    """Calculate the value within the parentheses."""
    while operations and operations[-1] != "(":
        calculate(numbers, operations)
    # pop "("
    operations.pop()
    # check if abs() or int() or round()
    if operations and operations[-1] in ["abs", "int", "round"]:
        perform_special_operation(numbers, operations)

def evaluate(tokens):
    """Evaluate the list of tokens and return the result."""
    operation_degrees = {"PLUS": 1, "MINUS": 1, "MULTIPLE": 2, "DIVIDE": 2, "abs": 0, "int": 0, "round": 0}
    # two stacks, one for numbers, one for operations
    numbers, operations = [], []
    index = 0
    while index < len(tokens):
        type = tokens[index]['type']
        if type == "NUMBER":
            numbers.append(tokens[index]['number'])
        # all these operations will be handled after a ")" shows up
        elif type in ["(", "abs", "int", "round"]:
            operations.append(type)
        # once the parenthesis is closed, calculate the value within it
        # then check if it is a sepcial operation (abs, int , round)
        elif type == ")":
            calcualte_parenthesis(numbers, operations)
        else: # type is +-*/
            while operations and operations[-1] != "(":
                prev_op = operations[-1]
                # if the previous operation (i.e., / or *) has higher or same priority than the current one (i.e., + or -)
                # then we can perform the previous operation
                if operation_degrees[prev_op] >= operation_degrees[type]:
                    calculate(numbers, operations)
                else:
                    break
            operations.append(type)
        index += 1        
    
    while operations and operations[-1] != "(":
        calculate(numbers, operations)
    return numbers[-1]


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    
    # Basic arithmetic tests
    test("1+2")
    test("1.0+2.1-3")
    test("2+3*2/3-1")
    test("3*4+5*6-7*8")
    test("3.2*4.1+5.3*6.4-7.9*8.8")
    test("-1.1+2.2*3.3/4.4+5.5-6.6")
    
    # Parentheses tests
    test("-(3+(4+5))")
    test("(1+(4+5+2)-3)+(6+8)")
    
    # Complex expressions
    test("12 + abs(int(round(-1.55) + abs(int(-2.3 + 4))))")
    
    # Mixed operations
    test("3 + 4 * 2 / (1 - 5) * 2")
    test("(1+3) * (2+(3*4))")
    test("1 + 2 * 3 - 4 / 5")
    test("7 + 3 * (10 / (12 / (3 + 1) - 1))")
    
    # Tests with spaces
    test(" 1 + 2 ")
    test("3 +    4 * 2")
    test("   7+8    /2*   3  ")
    
    # Unary minus
    test("-1 + 2")
    test("-(1+2)")
    test("-(-3 + 4)")
    
    # Functions
    test("abs(-5)")
    test("int(5.9)")
    test("round(3.5)")
    test("abs(-5) + int(5.9) - round(3.5)")
    
    # Nested functions
    test("abs(int(round(-1.55)))")
    test("round(int(abs(-5.9)))")
    
    # Combined operations
    test("abs(-5) + int(2.3) * round(2.7) - abs(int(round(-2.8)))")
    
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)