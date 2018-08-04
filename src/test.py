import json


def decor(func):
    def wrapper(a, b):
        if a is None:
            a =5
        return func(a,b)

    return wrapper


@decor
def foo(a=None, b=None):
    return [a,b]

print(foo(None,2))