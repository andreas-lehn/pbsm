# core extension of Python based stack machine

import sys

def add(interp):
    interp.push(interp.pop() + interp.pop())

def sub(interp):
    o = interp.pop()
    interp.push(interp.pop() - o)

def div(interp):
    divisor = interp.pop()
    interp.push(interp.pop() / divisor)

def idiv(interp):
    divisor = interp.pop()
    interp.push(int(interp.pop() // divisor))

def mod(interp):
    divisor = interp.pop()
    interp.push(interp.pop() % divisor)

def mul(interp):
    interp.push(interp.pop() * interp.pop())

def power(interp):
    exp = interp.pop()
    interp.push(interp.pop() ** exp)

def neg(interp):
    interp.push(-interp.pop())

def clear(interp):
    interp.stack.clear()

def dup(interp):
    interp.push(interp.peek())

def exch(interp):
    a = interp.pop()
    b = interp.pop()
    interp.push(a)
    interp.push(b)

def pop(interp):
    return interp.pop()

def roll(interp):
    times = interp.pop(int)
    pos = -interp.pop(int)
    if times < 0:
        for i in range(-times):
            o = interp.pop_n(pos)
            interp.push(o)
    elif times > 0:
        for i in range(times):
            o = interp.pop()
            interp.push_n(pos, o)

def print_(interp):
    print(interp.pop())

def pstack(interp):
    for o in reversed(interp.stack):
        print(o)

def eq(interp):
    interp.push(interp.pop() == interp.pop())

def ne(interp):
    interp.push(interp.pop() != interp.pop())

def lt(interp):
    o = interp.pop()
    interp.push(interp.pop() < o)

def le(interp):
    o = interp.pop()
    interp.push(interp.pop() <= o)

def gt(interp):
    o = interp.pop()
    interp.push(interp.pop() > o)

def ge(interp):
    o = interp.pop()
    interp.push(interp.pop() >= o)

def not_(interp):
    interp.push(not interp.pop())

def if_(interp):
    op = interp.pop()
    if interp.pop():
        interp.execute(op)

def ifelse(interp):
    op2 = interp.pop()
    op1 = interp.pop()
    if interp.pop():
        interp.execute(op1)
    else:
        interp.execute(op2)

class Flag:
    def __init__(self):
        self.flag = False
    def __call__(self, interp):
        self.flag = True
    def __bool__(self):
        return self.flag
    
def repeat(interp):
    op = interp.pop()
    n = interp.pop(int)
    exit_flag = Flag()
    cmd_idx = interp.register({'exit': exit_flag})
    for _ in range(n):
        interp.execute(op)
        if exit_flag: break
    interp.unregister(cmd_idx)

def for_(interp):
    op = interp.pop()
    last = interp.pop(int)
    step = interp.pop(int)
    first = interp.pop(int)
    exit_flag = Flag()
    cmd_idx = interp.register({'exit': exit_flag})
    for i in range(first, last, step):
        interp.push(i)
        interp.execute(op)
        if exit_flag: break
    interp.unregister(cmd_idx)

def loop(interp):
    op = interp.pop()
    exit_flag = Flag()
    cmd_idx = interp.register({'exit': exit_flag})
    while not exit_flag:
        interp.execute(op)
    interp.unregister(cmd_idx)

def forall(interp):
    op = interp.pop()
    array = interp.pop(list)
    exit_flag = Flag()
    cmd_idx = interp.register({'exit': exit_flag})
    for o in array:
        interp.push(o)
        interp.execute(op)
        if exit_flag: break
    interp.unregister(cmd_idx)

def exit(interp):
    sys.exit()

def exit_with_code(interp):
    sys.exit(interp.pop())

def get(interp):
    i = interp.pop(int)
    array = interp.pop(list)
    interp.push(array[i])

def put(interp):
    o = interp.pop()
    i = interp.pop(int)
    array = interp.pop(list)
    array[i] = o

def array(interp):
    n = interp.pop(int)
    interp.push([None] * n)

def length(interp):
    interp.push(len(interp.pop()))

def aload(interp):
    array = interp.pop(list)
    for o in array:
        interp.push(o)
    interp.push(array)

def astore(interp):
    array = interp.pop(list)
    for i in range(len(array)):
        array[-(i + 1)] = interp.pop()
    interp.push(array)

commands = {
    'add': add,
    '+': add,
    '-': sub,
    'sub': sub,
    'div': div,
    '/': div,
    'idiv': idiv,
    '//': idiv,
    'mod': mod,
    '%': mod,
    'mul': mul,
    '*': mul,
    'neg': neg,
    'power': power,
    '**': power,
    'clear': clear,
    'dup': dup,
    'exch': exch,
    'pop': pop,
    'roll': roll,
    'print': print_,
    'pstack': pstack,
    'eq': eq,
    '==': eq,
    'ne': ne,
    '!=': ne,
    'lt': lt,
    '<': lt,
    'gt': gt,
    '>': gt,
    'le': le,
    '<=': le,
    'ge': ge,
    '>=': ge,
    'not': not_,
    '!': not_,
    'if': if_,
    'ifelse': ifelse,
    'repeat': repeat,
    'for': for_,
    'loop': loop,
    'forall': forall,
    'exit': exit,
    'exit_with_code': exit_with_code,
    'get': get,
    'put': put,
    'set': put,
    'array': array,
    'length': length,
    'aload': aload,
    'astore': astore 
}
