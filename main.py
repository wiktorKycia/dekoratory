
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator
#
#
# def my_decorator(func):
#     def wrapper():
#         print("before")
#         func()
#         print("after")
#     return wrapper
#
# @my_decorator
# @repeat(3)
# def say_hello():
#     print("hello")


# say_hello()
from functools import wraps
def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"We are calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def hello(name:str):
    return f"Hello {name}"

@my_decorator
def hello_name(name:str):
    """
    Returns a string that greets name
    :param name: string
    :return: Hello <name>
    """
    return f"Hello {name}"

# print(hello("Wiktor"))
# print(hello_name("John"))
# print(hello_name.__doc__) #gdyby nie było @wraps w dekoratorze, to zwróciłoby None



def memoize(func):
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args[0] in cache:
            return cache[args[0]]
        result = func(args[0])
        cache[args[0]] = result
        return result
    return wrapper
from functools import cache
@memoize
# @cache
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(499))
