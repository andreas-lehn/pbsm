# core extension of Python based interp machine

import sys

def dup(interp):
    interp.push(interp.peek())

def ndup(interp):
    n = int(interp.pop())
    object = interp.peek()
    for _ in range(n):
        interp.push(object)

def swap(interp):
    a = interp.pop()
    b = interp.pop()
    interp.push(a)
    interp.push(b)

def pop(interp):
    interp.pop()

def exit(interp):
    sys.exit()

def exit_with_code(interp):
    sys.exit(interp.pop())

commands = {
    'dup': dup,
    'ndup': ndup,
    'swap': swap,
    'pop': pop,
    'exit': exit,
    'exit_with_code': exit_with_code
}
