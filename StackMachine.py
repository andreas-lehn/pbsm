# StackMachine in Python

from antlr4 import FileStream, Token
from StackMachineLexer import StackMachineLexer

stack = []
symbol_table = dict()

def def_func(stack):
    symbol = stack.pop()
    object = stack.pop()
    symbol_table[symbol.name] = object

symbol_table['def'] = def_func

class Marker:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.text
    
    def __eq__(self, other):
        return isinstance(other, Marker) and self.text == other.text
    
START_LIST = Marker('(')
END_LIST   = Marker(')')
START_FUNC = Marker('{')
END_FUNC   = Marker('}')

class Function:
    def __init__(self, sequence):
        self.sequence = sequence
    
    def __call__(self, stack):
        for object in self.sequence:
            execute(object)

    def __repr__(self):
        return 'f(' + str(self.sequence) + ')'

class Symbol:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Reference(Symbol):
    def __repr__(self):
        return '*' + self.name

def text_to_str(text):
    if text[0:3] == '"""':
        return text[3:-3]
    return text[1:-1]

def pop_to_marker(stack, marker):
    result = list()
    object = stack.pop()
    while object != marker:
        result.insert(0, object)
        object = stack.pop()
    return result

def create_list(stack):
    stack.append(pop_to_marker(stack, START_LIST))

def create_func(stack):
    stack.append(Function(pop_to_marker(stack, START_FUNC)))

def lookup_object(symbol):
    return symbol_table[symbol.name]

deffered_mode = 0

def execute(object):
    global deffered_mode
    
    if not object: return

    if object == END_LIST:
        create_list(stack)
        return
    
    if object == START_FUNC:
        deffered_mode += 1
    
    if object == END_FUNC:
        create_func(stack)
        deffered_mode -= 1
        return
    
    if callable(object) and not deffered_mode:
        object(stack)
        return
        
    if type(object) == Symbol and not deffered_mode:
        execute(lookup_object(object))
        return
    
    stack.append(object)


def token_to_object(token):
    match token.type:
        case StackMachineLexer.TRUE:
            return True
        case StackMachineLexer.FALSE:
            return False
        case StackMachineLexer.STRING:
            return text_to_str(token.text)
        case StackMachineLexer.INTEGER:
            return int(token.text)
        case StackMachineLexer.FLOAT:
            return float(token.text)
        case StackMachineLexer.MARKER:
            return Marker(token.text)
        case StackMachineLexer.NAME:
            return Symbol(token.text)
        case StackMachineLexer.NAME_REF:
            return Reference(token.text[1:])
        case _:
            return None

def main(argv):
    input = FileStream(argv[1])
    lexer = StackMachineLexer(input)
    while True:
        token = lexer.nextToken()
        if token.type == Token.EOF:
            break
        object = token_to_object(token)
        if object:
            execute(object)
            print(stack)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
