# StackMachine in Python

import sys
import argparse

from antlr4 import FileStream, Token, InputStream
from StackMachineLexer import StackMachineLexer

class Marker:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.text

    def __eq__(self, other):
        return isinstance(other, Marker) and self.text == other.text

START_LIST  = Marker('[')
END_LIST    = Marker(']')
START_FUNC  = Marker('(')
END_FUNC    = Marker(')')
START_SCOPE = Marker('{')
END_SCOPE   = Marker('}')

def pop_to_marker(stack, marker):
    result = list()
    object = stack.pop()
    while object != marker:
        result.insert(0, object)
        object = stack.pop()
    return result

def start_list_func(stack):
    stack.append(START_LIST)
    
def end_list_func(stack):
    stack.append(pop_to_marker(stack, START_LIST))

class Interpreter:

    def __init__(self, verbose=False):
        self.stack = []
        self.symbol_table = { 
            'def': lambda stack: self.def_func(stack),
            'exec': lambda stack: self.exec_func(stack),
            str(START_LIST): start_list_func,
            str(END_LIST): end_list_func
        }
        self.deffered_mode = 0
        self.verbose = verbose

    def def_func(self, stack):
        """Takes a symbol and an object from the stack and store the object in the dictionary with the symbols name as key"""
        symbol = stack.pop()
        self.symbol_table[symbol.name] = stack.pop()

    def exec_func(self, stack):
        """Takes an object from the stack and executes it"""
        self.execute(stack.pop())

    def register(self, symbols):
        self.symbol_table = { **self.symbol_table, **symbols }

    class Function:
        def __init__(self, interpreter, sequence):
            self.sequence = sequence
            self.interpreter = interpreter
    
        def __call__(self, stack):
            for object in self.sequence:
                self.interpreter.execute(object)

        def __repr__(self):
            return 'f(' + str(self.sequence) + ')'

    class Symbol:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return self.name

    class Reference():
        def __init__(self, symbol):
            self.symbol = symbol

        def __repr__(self):
            return '!' + str(self.symbol)

    def create_func(self):
        self.stack.append(Interpreter.Function(self, pop_to_marker(self.stack, START_FUNC)))

    def lookup_object(self, symbol):
        return self.symbol_table[symbol.name]

    def start_scope(self):
        self.log('Not implemented yet')
    
    def end_scope(self):
        self.log('Not implemented yet')
    
    def execute(self, object):
        if self.deffered_mode:
            if object == END_FUNC:
                self.create_func()
                self.deffered_mode = False
                self.log('Deffered mode: OFF')
            else:
                self.stack.append(object)
        else:
            if object == START_FUNC:
                self.deffered_mode = True
                self.stack.append(object)
                self.log('Deffered mode: ON')
            elif object == START_SCOPE:
                self.start_scope()
            elif object == END_SCOPE:
                self.end_scope()
            elif callable(object):
                object(self.stack)            
            elif type(object) == Interpreter.Symbol:
                self.execute(self.lookup_object(object))
            elif type(object) == Interpreter.Reference:
                self.stack.append(object.symbol)
            else:
                self.stack.append(object)

    def token_to_object(token):
        match token.type:
            case StackMachineLexer.TRUE:
                return True
            case StackMachineLexer.FALSE:
                return False
            case StackMachineLexer.STRING:
                if token.text[0:3] == '"""':
                    return token.text[3:-3]
                return token.text[1:-1]
            case StackMachineLexer.INTEGER:
                return int(token.text)
            case StackMachineLexer.FLOAT:
                return float(token.text)
            case StackMachineLexer.MARKER:
                return Marker(token.text)
            case StackMachineLexer.NAME:
                return Interpreter.Symbol(token.text)
            case StackMachineLexer.NAME_REF:
                return Interpreter.Reference(Interpreter.Symbol(token.text[1:]))
            case _:
                return None
    
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
            object = Interpreter.token_to_object(token)
            if object is not None:
                self.execute(object)

    def interpret_command(self, command):
        input = InputStream(command)
        self.interpret_stream(input)

def append_func(stack):
    item = stack.pop()
    stack[-1].append(item)

def extend_func(stack):
    item = stack.pop()
    stack[-1].extend(item)

def get_func(stack):
    index = int(stack.pop())
    stack.append(stack[-1][index])

def set_func(stack):
    index = int(stack.pop())
    item = stack.pop()
    stack[-1][index] = item

python_extension = {
    'append': append_func,
    'extend': extend_func,
    'get': get_func,
    'set': set_func
}

def dup_func(stack):
    stack.append(stack[-1])

def ndup_func(stack):
    n = int(stack.pop())
    object = stack[-1]
    for i in range(n):
        stack.append(object)

def swap_func(stack):
    a = stack.pop()
    b = stack.pop()
    stack.append(a)
    stack.append(b)

stack_extension = {
    'dup': dup_func,
    'ndup': ndup_func,
    'swap': swap_func
}

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', type=str, help='name of input file to be interpreted')
    parser.add_argument('-c', '--command', type=str, help='command to execute')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-s', '--showstack', action='store_true', help='show contents of stack in interactive mode')
    parser.add_argument('--stack_lenght', type=int, help='sets the length of the stack (in character) shown in interactive mode', default=40)
    args = parser.parse_args()

    interpreter = Interpreter()
    interpreter.register(python_extension)
    interpreter.register(stack_extension)
    interpreter.verbose = args.verbose
    if args.command:
        interpreter.interpret_command(args.command)
    elif args.filename:
        interpreter.interpret_file(args.filename)
    else:
        for line in sys.stdin:
            try:
                interpreter.interpret_command(line)
            except (RuntimeError, KeyError, TypeError, IndexError) as err:
                print(type(err).__name__, ':', str(err))
            print(interpreter.stack)
        
if __name__ == '__main__':
    sys.exit(main(sys.argv))
