import evaluator

def evaluate(code, environement = {}, memory = {}):
    evaluator.statement.evaluate(code, environement, memory)

    return {
        'environement': environement,
        'memory': memory
    }