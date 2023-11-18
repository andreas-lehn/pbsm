# Python extension for Python based stack machine

def append(stack):
    item = stack.pop()
    stack[-1].append(item)

def extend(stack):
    item = stack.pop()
    stack[-1].extend(item)

def get(stack):
    index = int(stack.pop())
    stack.append(stack[-1][index])

def set(stack):
    index = int(stack.pop())
    item = stack.pop()
    stack[-1][index] = item

def add(stack):
    stack.append(stack.pop() + stack.pop())

def sub(stack):
    operand = stack.pop()
    stack.append(stack.pop() - operand)

def mul(stack):
    stack.append(stack.pop() * stack.pop())

def div(stack):
    operand = stack.pop()
    stack.append(stack.pop() / operand)

def power(stack):
    operand = stack.pop()
    stack.append(stack.pop() ** operand)

def neg(stack):
    stack.append(-stack.pop())

def int_(stack):
    stack.append(int(stack.pop()))

def bool_(stack):
    stack.append(bool(stack.pop()))

def float_(stack):
    stack.append(float(stack.pop()))

def str_(stack):
    stack.append(str(stack.pop()))

def len_(stack):
    stack.append(len(stack.pop()))

def list_(stack):
    result = []
    len = int(stack.pop())
    for i in range(len):
        result.insert(0, stack.pop())
    stack.append(result)

commands = {
    'append': append,
    'extend': extend,
    'get': get,
    'set': set,
    'add': add,
    '+': add,
    'sub': sub,
    '-': sub,
    'mul': mul,
    '*': mul,
    'div': div,
    '/': div,
    'power': power,
    '**': power,
    'neg': neg,
    'bool': bool_,
    'float': float_,
    'str': str_,
    'int': int_,
    'len': len_,
    'list': list_
}

