# StackMachine in Python

import sys
import argparse

from antlr4 import FileStream, Token, InputStream
from StackMachineLexer import StackMachineLexer

import core
import python

def mark(stack):
    stack.append(Interpreter.Marker())

def counttomark(stack):
    last = len(stack) - 1
    i = last
    while (i > 0):
        if type(object) == Interpreter.Marker:
            break
        i -= 1
    stack.append(last - i)

def cvlit(stack):
    f = stack.pop()
    if not type(f) == Interpreter.Procedure:
        stack.append(f)
        raise TypeError("Object is not a function")
    stack.append(f.sequence)

def def_func(interp, stack):
    """Takes a symbol and an object from the stack and store the object in the dictionary with the symbols name as key"""
    procedure = stack.pop()
    interp.symbol_table[stack.pop().name] = procedure

def exec_func(interp, stack):
    """Takes an object from the stack and executes it"""
    interp.execute(stack.pop())

def cvx(interp, stack):
    list_ = stack.pop()
    if type(list_) != list:
        raise TypeError('Object is not a list')
    stack.append(Interpreter.Procedure(interp, list_))


class Interpreter:

    def __init__(self, verbose=False):
        self.stack = []
        self.symbol_table = { 
            'def': lambda stack: def_func(self, stack),
            'exec': lambda stack: exec_func(self, stack),
            'mark': mark,
            'counttomark': counttomark,
            'cvlit': cvlit,
            'cvx': lambda stack: cvx(self, stack)
        }
        self.deffered_mode = 0
        self.verbose = verbose

    def register(self, symbols):
        self.symbol_table = { **self.symbol_table, **symbols }

    class Marker:
        def __repr__(self):
            return '.'

    class Procedure:
        def __init__(self, interpreter, sequence):
            if type(sequence) != list:
                raise TypeError('Object is not a list')
            self.sequence = sequence
            self.interpreter = interpreter
    
        def __call__(self, stack):
            for object in self.sequence:
                self.interpreter.execute(object)

        def __repr__(self):
            return 'x' + str(self.sequence)

    class Symbol:
        def __init__(self, interp, name):
            self.name = name
            self.interp = interp

        def __call__(self, stack):
            self.interp.execute(self.interp.lookup(self))

        def __repr__(self):
            return self.name

    class Reference():
        def __init__(self, symbol):
            self.symbol = symbol

        def __repr__(self):
            return '&' + str(self.symbol)
        
        def __call__(self, stack):
            stack.append(self.symbol)

    def create_list(self):
        result = []
        object = self.stack.pop()
        while type(object) != Interpreter.Marker:
            result.insert(0, object)
            object = self.stack.pop()
        self.stack.append(result)

    def lookup(self, symbol):
        return self.symbol_table[symbol.name]

    def execute(self, object):
        if self.deffered_mode:
            self.stack.append(object)
        else:
            if callable(object):
                object(self.stack)            
            else:
                self.stack.append(object)

    def process_token(self, token):
        self.log(token)
        match token.type:
            case StackMachineLexer.TRUE:
                self.execute(True)
            case StackMachineLexer.FALSE:
                self.execute(False)
            case StackMachineLexer.STRING:
                if token.text[0:3] == '"""':
                    self.execute(token.text[3:-3])
                else:
                    self.execute(token.text[1:-1])
            case StackMachineLexer.INTEGER:
                self.execute(int(token.text))
            case StackMachineLexer.FLOAT:
                self.execute(float(token.text))
            case StackMachineLexer.LIST_START:
                self.execute(Interpreter.Marker())
            case StackMachineLexer.XLIST_START:
                self.deffered_mode += 1
                self.log('Deffered mode:', self.deffered_mode)
                self.execute(Interpreter.Marker())
            case StackMachineLexer.LIST:
                self.create_list()
            case StackMachineLexer.XLIST:
                self.create_list()
                cvx(self, self.stack)
                self.deffered_mode -= 1
                self.log('Deffered mode:', self.deffered_mode)
            case StackMachineLexer.NAME:
                self.execute(Interpreter.Symbol(self, token.text))
            case StackMachineLexer.NAME_REF:
                self.execute(Interpreter.Reference(Interpreter.Symbol(self, token.text[1:])))
    
    def log(self, *args):
        if (self.verbose):
            print(*args)
    
    def interpret_file(self, filename):
        input = FileStream(filename)
        self.interpret_stream(input)
    
    def interpret_stream(self, input):
        lexer = StackMachineLexer(input)
        while True:
            token = lexer.nextToken()
            self.log(token)
            if token.type == Token.EOF:
                break
            self.process_token(token)

    def interpret_command(self, command):
        input = InputStream(command)
        self.interpret_stream(input)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', type=str, help='name of input file to be interpreted')
    parser.add_argument('-c', '--command', type=str, help='command to execute')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-s', '--show_stack', action='store_true', help='show contents of stack in interactive mode')
    parser.add_argument('--stack_length', type=int, help='sets the length of the stack (in character) shown in interactive mode', default=40)
    args = parser.parse_args()

    interpreter = Interpreter()
    interpreter.register(core.commands)
    interpreter.register(python.commands)
    interpreter.verbose = args.verbose
    if args.command:
        interpreter.interpret_command(args.command)
    elif args.filename:
        interpreter.interpret_file(args.filename)
    else:
        # interactive mode
        PROMPT = '> '
        while True:
            stack = ''
            if args.show_stack:
                stack = str(interpreter.stack)[-args.stack_length:]
            prompt = stack + PROMPT
            try:
                line = input(prompt)
                interpreter.log(line)      
                interpreter.interpret_command(line)
            except (EOFError, KeyboardInterrupt):
                return
            except (RuntimeError, KeyError, TypeError, IndexError) as err:
                print(type(err).__name__, ':', str(err))
        
if __name__ == '__main__':
    sys.exit(main(sys.argv))
