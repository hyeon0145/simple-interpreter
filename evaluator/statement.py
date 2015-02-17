from evaluator import expression

_statement_evaluators = {}

# abstarct abstract evaluator
def evaluate(statement, environment, memory):
    # statement = (statement identifier, ...)
    if statement[0] not in _statement_evaluators:
        raise RuntimeError('invalid statement: {0}'.format(statement))

    # cloning environment
    environment = dict(environment)
    return _statement_evaluators[statement[0]](statement, environment, memory)

def _evaluate_assignment(statement, environment, memory):
    # statement = (=, l-value, r-value)
    if (statement[1] not in environment) or (environment[statement[1]] not in memory):
        raise RuntimeError('undefined variable: {0}'.format(statement[1]))

    memory[environment[statement[1]]] = expression.evaluate(statement[2], environment, memory)
    return memory
_statement_evaluators['='] = _evaluate_assignment

def _evaluate_skip(statement, environment, memory):
    # statement = (skip)
    return memory
_statement_evaluators['skip'] = _evaluate_skip

def _evaluate_statements(statement, environment, memory):
    # statement = (;, statement1, statement2)
    return evaluate(statement[2], environment, evaluate(statement[1], environment, memory))
_statement_evaluators[';'] = _evaluate_statements

def _evaluate_if(statement, environment, memory):
    # statement = (if, expression, statement1, statement2)
    if expression.evaluate(statement[1], environment, memory) != 0:
        return evaluate(statement[2], environment, memory)
    else:
        return evaluate(statement[3], environment, memory)
_statement_evaluators['if'] = _evaluate_if

def _evaluate_while(statement, environment, memory):
    # statement = (while, expression, statement)
    if expression.evaluate(statement[1], environment, memory) != 0:
        next_statement = (';', statement[2], statement)
        return evaluate(next_statement, environment, memory)
    else:
        return memory
_statement_evaluators['while'] = _evaluate_while

def _evaluate_variable_declaration(statement, environment, memory):
    # statement = (var, x, ;, t)
    new_address = _allocate_memory(memory)
    environment[statement[1]] = new_address
    memory[new_address] = 0

    next_memory = evaluate(statement[3], environment, memory)
    del next_memory[new_address]
    return next_memory
_statement_evaluators['var'] = _evaluate_variable_declaration

def _evaluate_procedure_definition(statement, environment, memory):
    # statement = (proc, p, (, x, ), {, statement1, }, ;, statement2)
    new_address = _allocate_memory(memory)
    environment[statement[1]] = new_address
    memory[new_address] = (statement[3], statement[6], environment)

    next_memory = evaluate(statement[9], environment, memory)
    del next_memory[new_address]
    return next_memory
_statement_evaluators['proc'] = _evaluate_procedure_definition

def _evaluate_invocation(statement, environment, memory):
    # statement = ((), p, e)
    if (statement[1] not in environment) or (environment[statement[1]] not in memory):
        raise RuntimeError('undefined procedure: {0}'.format(statement[1]))

    if not _is_procedure(memory[environment[statement[1]]]):
        raise RuntimeError('not a procedure: {0}'.format(statement[1]))

    # procedure = (parameter, statement, environment)
    procedure = memory[environment[statement[1]]]
    procedure_environment = dict(procedure[2]) # cloning procedure environment

    new_address = _allocate_memory(memory)
    procedure_environment[procedure[0]] = new_address
    memory[new_address] = expression.evaluate(statement[2], environment, memory)

    next_memory = evaluate(procedure[1], procedure_environment, memory)
    del next_memory[new_address]
    return next_memory
_statement_evaluators['()'] = _evaluate_invocation

def _evaluate_print(statement, environment, memory):
    print(expression.evaluate(statement[1], environment, memory))

    return memory
_statement_evaluators['print'] = _evaluate_print

# utilities
def _allocate_memory(memory):
    address = 1
    while address in memory:
        address += 1

    return address

def _is_procedure(statement):
    return isinstance(statement, tuple) and (len(statement) == 3)