# StackMachine in Python

import sys
import argparse

__author__ = "Andreas Lehn"
from .version import __version__

from .__init__ import Interpreter
from .core import commands as core_commands

from antlr4 import FileStream, Token, InputStream

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', type=str, help='name of input file to be interpreted')
    parser.add_argument('-c', '--command', type=str, help='command to execute')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-n', '--nacked', action='store_true')
    parser.add_argument('-s', '--show_stack', action='store_true', help='show contents of stack in interactive mode')
    parser.add_argument('--stack_length', type=int, help='sets the length of the stack (in character) shown in interactive mode', default=40)
    args = parser.parse_args()

    interpreter = Interpreter()
    interpreter.verbose = args.verbose
    if not args.nacked:
        interpreter.log('core extension loaded.')
        interpreter.register(core_commands)
    if args.command:
        interpreter.log('execution command:', args.command)
        interpreter.interpret(InputStream(args.command))
    elif args.filename:
        interpreter.log('interpreting file', args.filename)
        interpreter.interpret(FileStream(args.filename))
    else:
        interpreter.log('entering interactive mode')
        PROMPT = '> '
        while True:
            stack = ''
            if args.show_stack:
                stack = str(interpreter.stack)[-args.stack_length:]
            prompt = stack + PROMPT
            try:
                line = input(prompt)
                interpreter.interpret(InputStream(line))
            except (EOFError, KeyboardInterrupt):
                break
            except (RuntimeError, KeyError, TypeError, IndexError, ValueError) as err:
                print(type(err).__name__, ':', str(err), file=sys.stderr)
    return 0
        
if __name__ == '__main__':
    sys.exit(main())
