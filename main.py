import sys

import interpreter
import program

if len(sys.argv) < 2:
    sys.exit('usage: python3 {0} <number>'.format(sys.argv[0]))

if not sys.argv[1].isdigit():
	sys.exit('error: <number> should be integer');

environment = {'in': 0}
memory = {0: int(sys.argv[1])}

try:
	interpreter.evaluate(program.code, environment, memory)
except RuntimeError as error:
	print('error:', error.args[0])