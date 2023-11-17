# StackMachine in Python

from antlr4 import FileStream, Token
from StackMachineLexer import StackMachineLexer

class Marker:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.text

    def __eq__(self, other):
        return isinstance(other, Marker) and self.text == other.text

def pop_to_marker(stack, marker):
    result = list()
    object = stack.pop()
    while object != marker:
        result.insert(0, object)
        object = stack.pop()
    return result

class Interpreter:

    def __init__(self):
        self.stack = []
        self.symbol_table = { 'def': lambda stack: self.def_func(stack) }
        self.deffered_mode = 0

    def def_func(self, stack):
        symbol = stack.pop()
        self.symbol_table[symbol.name] = stack.pop()
    
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

    class Reference(Symbol):
        def __repr__(self):
            return '`' + self.name

    START_FUNC = Marker('{')
    END_FUNC   = Marker('}')
    
    def create_func(self):
        self.stack.append(Interpreter.Function(self, pop_to_marker(self.stack, Interpreter.START_FUNC)))

    def lookup_object(self, symbol):
        return self.symbol_table[symbol.name]

    def execute(self, object):
        if object == Interpreter.START_FUNC:
            self.deffered_mode += 1
        
        if object == Interpreter.END_FUNC:
            self.create_func()
            self.deffered_mode -= 1
            return
        
        if callable(object) and not self.deffered_mode:
            object(self.stack)
            return
            
        if type(object) == Interpreter.Symbol and not self.deffered_mode:
            self.execute(self.lookup_object(object))
            return
        
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
                return Interpreter.Reference(token.text[1:])
            case _:
                return None
    
    def interpret_file(self, filename):
        input = FileStream(filename)
        lexer = StackMachineLexer(input)
        while True:
            token = lexer.nextToken()
            if token.type == Token.EOF:
                break
            object = Interpreter.token_to_object(token)
            if object:
                self.execute(object)
                print(self.stack)

START_LIST = Marker('(')

def start_list_func(stack):
    stack.append(START_LIST)
    
def end_list_func(stack):
    stack.append(pop_to_marker(stack, START_LIST))

list_extension = { '(': start_list_func, ')': end_list_func }

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
    interpreter = Interpreter()
    interpreter.register(list_extension)
    interpreter.register(stack_extension)
    interpreter.interpret_file(argv[1])

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))