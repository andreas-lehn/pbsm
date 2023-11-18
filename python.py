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

commands = {
    'append': append,
    'extend': extend,
    'get': get,
    'set': set
}

