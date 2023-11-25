# StackMachine in Python

__author__ = "Andreas Lehn"
from .version import __version__

from antlr4 import FileStream, Token, InputStream
from .Lexer import Lexer
from .core import commands as core_commands

class Interpreter:

    def __init__(self, verbose=False):
        self.stack = []
        self.symbol_tables = []
        self.register({ 
            '{': Interpreter.start_proc,
            '[': Interpreter.mark,
            '}': Interpreter.make_proc,
            ']': Interpreter.make_list
        })
        self.register({ 
            'def': Interpreter.def_,
            'exec': Interpreter.exec,
            'mark': Interpreter.mark,
            'counttomark': Interpreter.count_to_mark,
            'cleartomark': Interpreter.pop_to_mark,
            'cvlit': Interpreter.cvlit,
            'cvx': Interpreter.cvx
        })
        self.deffered_mode = 0
        self.verbose = verbose

    def register(self, symbols):
        self.symbol_tables.append(symbols)

    def enter_deffered_mode(self):
        self.deffered_mode += 1

    def exit_deffered_mode(self):
        self.deffered_mode -= 1

    def in_deffered_mode(self):
        return self.deffered_mode > 0
    
    def push(self, item):
        self.stack.append(item)
    
    def pop(self, type=object):
        item = self.stack.pop()
        if not isinstance(item, type):
            raise TypeError(f'item {item} ({type(item)} is not an instance of {type}')
        return item
    
    def peek(self, offset=0):
        return self.stack[offset - 1]
    
    def append(self, item):
        self.stack.append(item)

    def __get__(self, index):
        return self.stack[index]
    
    def __set__(self, index, item):
        self.stack[index] = item

    class Marker:
        def __repr__(self):
            return '.'

    def mark(self):
        self.push(Interpreter.Marker())

    def pop_to_mark(self):
        result = []
        while not isinstance(self.peek(), Interpreter.Marker):
            result.insert(0, self.pop())
        return result

    def count_to_mark(self):
        count = 0
        for obj in reversed(self.stack):
            if isinstance(obj, Interpreter.Marker): break
            count += 1
        self.push(count)

    def make_list(self):
        sequence = self.pop_to_mark()
        self.pop() # drop mark
        self.push(sequence)
    
    class Symbol:
        def __init__(self, interp, name):
            self.name = name
            self.interp = interp

        def lookup(self, dict):
            if self.name in dict.keys():
                return dict[self.name]
            return None
        
        def __repr__(self):
            return self.name

    def def_(self):
        """Takes a symbol and an object from the stack and store the object in the dictionary with the symbols name as key"""
        item = self.pop()
        symbol = self.pop(Interpreter.Symbol)
        self.symbol_tables[-1][symbol.name] = item

    def lookup(self, symbol):
        assert(isinstance(symbol, Interpreter.Symbol))
        result = None
        if self.in_deffered_mode():
            result = symbol.lookup(self.symbol_tables[0])
        else:
            for i in range(-1, -len(self.symbol_tables) - 1, -1):
                result = symbol.lookup(self.symbol_tables[i])
                if result:
                    break
        return result
    
    class Procedure:
        def __init__(self, sequence):
            if not isinstance(sequence, list):
                raise TypeError('Object is not a list')
            self.sequence = sequence
    
        def __call__(self, interp):
            for object in self.sequence:
                interp.execute(object)

        def __repr__(self):
            return 'x' + str(self.sequence)

    def start_proc(self):
        self.mark()
        self.enter_deffered_mode()
    
    def make_proc(self):
        self.make_list()
        self.cvx()
        self.exit_deffered_mode()

    def cvlit(self):
        """convert to literatl"""
        proc = self.pop(Interpreter.Procedure)
        self.push(proc.sequence)

    def cvx(self):
        """convert to executable"""
        self.push(Interpreter.Procedure(self.pop(list)))

    def exec(self):
        """executes the object on the stack"""
        self.execute(self.pop())

    class Reference():
        def __init__(self, symbol):
            self.symbol = symbol

        def __repr__(self):
            return "'" + str(self.symbol)
        
        def __call__(self, stack):
            stack.append(self.symbol)

    def execute(self, obj):
        if self.in_deffered_mode():
            if isinstance(obj, Interpreter.Symbol):
                referee = self.lookup(obj)
                if referee:
                    referee(self)
                else:
                    self.push(obj)
            else:
                self.push(obj)
        else:
            if callable(obj):
                obj(self)
            elif type(obj) == Interpreter.Symbol:
                referee = self.lookup(obj)
                if not referee:
                    raise KeyError(f'symbol {obj} not defined.')
                self.execute(referee)      
            else:
                self.push(obj)

    def process_token(self, token):
        self.log('processing token:', token)
        match token.type:
            case Lexer.TRUE:
                self.execute(True)
            case Lexer.FALSE:
                self.execute(False)
            case Lexer.STRING:
                if token.text[0:3] == '"""':
                    self.execute(token.text[3:-3])
                else:
                    self.execute(token.text[1:-1])
            case Lexer.INTEGER:
                self.execute(int(token.text))
            case Lexer.FLOAT:
                self.execute(float(token.text))
            case Lexer.NAME:
                self.execute(Interpreter.Symbol(self, token.text))
            case Lexer.NAME_REF:
                self.execute(Interpreter.Reference(Interpreter.Symbol(self, token.text[1:])))
    
    def log(self, *args):
        if (self.verbose):
            print(*args)
    
    def interpret(self, input):
        lexer = Lexer(input)
        while True:
            token = lexer.nextToken()
            if token.type == Token.EOF:
                break
            self.process_token(token)
