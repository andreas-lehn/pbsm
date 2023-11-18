# core extension of Python based stack machine

import sys

def dup(stack):
    stack.append(stack[-1])

def ndup(stack):
    n = int(stack.pop())
    object = stack[-1]
    for i in range(n):
        stack.append(object)

def swap(stack):
    a = stack.pop()
    b = stack.pop()
    stack.append(a)
    stack.append(b)

def pop(stack):
    stack.pop()

def exit(stack):
    sys.exit()

def exit_with_code(stack):
    sys.exit(stack.pop())

commands = {
    'dup': dup,
    'ndup': ndup,
    'swap': swap,
    'pop': pop,
    'exit': exit,
    'exit_with_code': exit_with_code
}
