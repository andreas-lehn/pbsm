# StackMachine in Python

from antlr4 import FileStream, Token
from StackMachineLexer import StackMachineLexer

stack = []

class Marker:
    LIST = '()'
    FUNC = '{}'
    SCOPE = '[]'

    def __init__(self, type):
        self.type = type
    
    def __repr__(self):
        return self.type

class Reference:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '->' + self.name

def text2str(text):
    if text[0:3] == '"""':
        return text[3:-3]
    return text[1:-1]

def createList():
    pass

def createFunc(name):
    pass

def executeSymbol(name):
    pass

def execute(token):
    match token.type:
        case StackMachineLexer.TRUE:
            stack.append(True)
        case StackMachineLexer.FALSE:
            stack.append(False)
        case StackMachineLexer.STRING:
            stack.append(text2str(token.text))
        case StackMachineLexer.INTEGER:
            stack.append(int(token.text))
        case StackMachineLexer.FLOAT:
            stack.append(float(token.text))
        case StackMachineLexer.OPEN_PAREN:
            stack.append(Marker(Marker.LIST))
        case StackMachineLexer.CLOSE_PAREN:
            createList()
        case StackMachineLexer.OPEN_BRACE:
            stack.append(Marker(Marker.FUNC))
        case StackMachineLexer.CLOSE_BRACE:
            createFunc(token.text)
        case StackMachineLexer.OPEN_BRACE:
            pass
        case StackMachineLexer.CLOSE_BRACKET:
            pass
        case StackMachineLexer.DOT:
            pass
        case StackMachineLexer.NAME:
            executeSymbol(token.text)
        case StackMachineLexer.NAME_REF:
            stack.append(Reference(token.text[1:]))
        case _:
            pass

def main(argv):
    input = FileStream(argv[1])
    lexer = StackMachineLexer(input)
    while True:
        t = lexer.nextToken()
        if t.type == Token.EOF:
            break
        execute(t)
        print(stack)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
