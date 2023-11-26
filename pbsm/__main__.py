# StackMachine in Python

import sys
import argparse

__author__ = "Andreas Lehn"
from .version import __version__

from .__init__ import Interpreter
from .core import commands as core_commands

import importlib
from antlr4 import FileStream, InputStream

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', type=str, help='name of input file to be interpreted')
    parser.add_argument('-c', '--command', type=str, help='command to execute')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-n', '--nacked', action='store_true')
    parser.add_argument('-m', '--module', nargs='*', help='extension module to be loaded')
    parser.add_argument('-s', '--show_stack', action='store_true', help='show contents of stack in interactive mode')
    parser.add_argument('--stack_length', type=int, help='sets the length of the stack (in character) shown in interactive mode', default=40)
    args = parser.parse_args()

    interpreter = Interpreter()
    interpreter.verbose = args.verbose
    if not args.nacked:
        interpreter.register(core_commands)
        interpreter.log('core extension loaded.')
    for m in args.module:
        try:
            module = importlib.import_module(m)
            interpreter.register(module.commands)
            interpreter.log(f'module {m} loaded.')
        except (ModuleNotFoundError, AttributeError, TypeError) as err:
            print(f'Error importing module:', err)
    if args.command:
        interpreter.log('executing command:', args.command)
        interpreter.interpret(InputStream(args.command))
    elif args.filename:
        interpreter.log('executing file', args.filename)
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
