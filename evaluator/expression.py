_operator_evaluators = {
    'unary': {},
    'binary': {}
}

# abstarct abstract evaluator
def evaluate(expression, environment, memory):
    if _is_variable(expression):
        evaluator = _evaluate_variable
    elif _is_integer(expression):
        evaluator = _evaluate_integer
    elif _is_unary_operator(expression):
        evaluator = _evaluate_unary_operator
    elif _is_binary_operator(expression):
        evaluator = _evaluate_binary_operator
    else:
        raise RuntimeError('invalid expression: {0}'.format(expression))

    # casting all results to integer because this language supports only integer
    # this casting will affect division operator and boolean operators
    return int(evaluator(expression, environment, memory))


# abstract evaluators
def _evaluate_unary_operator(expression, environment, memory):
    # expression = (unary operator, operand)
    if expression[0] not in _operator_evaluators['unary']:
        raise RuntimeError('invalid unary operator: {0}'.format(expression[0]))

    return _operator_evaluators['unary'][expression[0]](expression, environment, memory)

def _evaluate_binary_operator(expression, environment, memory):
    # expression = (binary operator, left operand, right operand)
    if expression[0] not in _operator_evaluators['binary']:
        raise RuntimeError('invalid binary operator: {0}'.format(expression[0]))
        
    return _operator_evaluators['binary'][expression[0]](expression, environment, memory)


# concrete evaluators
## variable evaluator
def _evaluate_variable(expression, environment, memory):
    # expression = str()
    if expression not in environment:
        raise RuntimeError('undefined varaible: {0}'.format(expression))
    elif not _is_integer(memory[environment[expression]]):
        raise RuntimeError('not an integer variable: {0}'.format(expression))

    return memory[environment[expression]]

## integer evaluator
def _evaluate_integer(expression, environment, memory):
    # expression = int()
    return expression

## unary operator evaluators
def _evaluate_negation_operator(expression, environment, memory):
    return not evaluate(expression[1], environment, memory)
_operator_evaluators['unary']['!'] = _evaluate_negation_operator

def _evaluate_minus_operator(expression, environment, memory):
    return -evaluate(expression[1], environment, memory)
_operator_evaluators['unary']['-'] = _evaluate_minus_operator

## binary operator evaluators
def _evaluate_addition_operator(expression, environment, memory):
    return evaluate(expression[1], environment, memory) + evaluate(expression[2], environment, memory)
_operator_evaluators['binary']['+'] = _evaluate_addition_operator

def _evaluate_subtraction_operator(expression, environment, memory):
    return evaluate(expression[1], environment, memory) - evaluate(expression[2], environment, memory)
_operator_evaluators['binary']['-'] = _evaluate_subtraction_operator

def _evaluate_multiplication_operator(expression, environment, memory):
    return evaluate(expression[1], environment, memory) * evaluate(expression[2], environment, memory)
_operator_evaluators['binary']['*'] = _evaluate_multiplication_operator

def _evaluate_division_operator(expression, environment, memory):
    return evaluate(expression[1], environment, memory) / evaluate(expression[2], environment, memory)
_operator_evaluators['binary']['/'] = _evaluate_division_operator

def _evaluate_equality_operator(expression, environment, memory):
    return evaluate(expression[1], environment, memory) == evaluate(expression[2], environment, memory)
_operator_evaluators['binary']['=='] = _evaluate_equality_operator

def _evaluate_less_than_operator(expression, environment, memory):
    return evaluate(expression[1], environment, memory) < evaluate(expression[2], environment, memory)
_operator_evaluators['binary']['<'] = _evaluate_less_than_operator

def _evaluate_and_operator(expression, environment, memory):
    if evaluate(expression[1], environment, memory) == 0:
        return 0
    else:
        return evaluate(expression[2], environment, memory)
_operator_evaluators['binary']['&&'] = _evaluate_and_operator

# utilities
def _is_variable(expression):
    return isinstance(expression, str)

def _is_integer(expression):
    return isinstance(expression, int)

def _is_unary_operator(expression):
    return isinstance(expression, tuple) and (len(expression) == 2)

def _is_binary_operator(expression):
    return isinstance(expression, tuple) and (len(expression) == 3)