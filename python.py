# Python extension for Python based stack machine

def append(interp):
    item = interp.pop()
    interp.peek().append(item)

def extend(interp):
    item = interp.pop()
    interp.peek().extend(item)

def get(interp):
    index = int(interp.pop())
    interp.push(interp[-1][index])

def set(interp):
    index = int(interp.pop())
    item = interp.pop()
    interp.peek()[index] = item

def add(interp):
    interp.push(interp.pop() + interp.pop())

def sub(interp):
    operand = interp.pop()
    interp.push(interp.pop() - operand)

def mul(interp):
    interp.push(interp.pop() * interp.pop())

def div(interp):
    operand = interp.pop()
    interp.push(interp.pop() / operand)

def power(interp):
    operand = interp.pop()
    interp.push(interp.pop() ** operand)

def neg(interp):
    interp.push(-interp.pop())

def int_(interp):
    interp.push(int(interp.pop()))

def bool_(interp):
    interp.push(bool(interp.pop()))

def float_(interp):
    interp.push(float(interp.pop()))

def str_(interp):
    interp.push(str(interp.pop()))

def len_(interp):
    interp.push(len(interp.pop()))

def list_(interp):
    result = []
    len = int(interp.pop())
    for i in range(len):
        result.insert(0, interp.pop())
    interp.push(result)

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
