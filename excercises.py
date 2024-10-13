# 1.
# def my_decorator(func):
#     def wrapper():
#         print("before calling a func")
#         func()
#         print("after calling a func")
#     return wrapper
#
# @my_decorator
# def say_hello():
#     print("Hello, world!")
#
# say_hello()


# 2.
# def greeting_decorator(func):
#     def wrapper(name):
#         print(f'Hello {name}')
#         func(name)
#     return wrapper
#
# @greeting_decorator
# def greet(name):
#     print(f"How are you today, {name}?")
#
# greet("Alice")

# # 3.
# def log_arguments(func):
#     def wrapper(*args, **kwargs):
#         print(f"starting function: {func.__name__} with arguments: {args} {kwargs}")
#         result = func(*args, **kwargs)
#         print(f"function {func.__name__} returned {result}")
#     return wrapper
#
# @log_arguments
# def add(a, b):
#     return a + b
#
# add(5, 10)
# add(a=7, b=9)

# # 4.
# def double_result(func):
#     def wrapper(n):
#         return func(n) * 2
#     return wrapper
#
# @double_result
# def square(n):
#     return n * n
#
# print(square(4))  # Should print 32

# 5.
from functools import wraps

def simple_decorator(func):
    @wraps(func)
    def wrapper():
        result = func()
        return result
    return wrapper

@simple_decorator
def my_function():
    """This is my function's docstring"""
    print("Function is running")

print(my_function.__name__)
print(my_function.__doc__)

from functools import wraps
import time

# 6. ===========================
def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        time_before = time.time()
        result = func(*args, **kwargs)
        time_after = time.time()
        print(f"function {func.__name__} was running for {time_after - time_before}s")
        return result
    return wrapper

@log_time
def slow_function(seconds:int):
    time.sleep(seconds)
    print("Function is done")
# slow_function = log_time(slow_function)
slow_function(1)


# 7.
def cache_decorator(func):
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args in cache:
            print('fetching from cache')
            return cache[args]
        else:
            print('computing')
            result = func(*args)
            cache[args] = result
            return result
    return wrapper


@cache_decorator
def expensive_computation(x):
    print(f"Computing for {x}")
    return x * 10

print(expensive_computation(5))  # Should compute
print(expensive_computation(5))  # Should fetch from cache
print(expensive_computation(10))  # Should compute


# 8.
import time

def rate_limit(func):
    l = 0
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal l
        time_between = time.time() - l
        if time_between <= 5:
            print(f"you must wait for {time_between}s")
            return None
        else:
            func(*args, **kwargs)
            l = time.time()
    return wrapper


@rate_limit
def send_message(message):
    print(f"Sending message: {message}")

send_message("Hello!")  # Should work
time.sleep(2)
send_message("Hello again!")  # Should be rate-limited
time.sleep(5)
send_message("Final message!")  # Should work

# 9.
def log_call(func):
    @wraps(func)
    def wrapper(*args):
        print(f"starting a function called {func.__name__} with {args} arguments")
        result = func(*args)
        if result[1] == "restored from cache":
            print(f"result restored from cache: {result[0]}")
            return result[0]
        elif result[1] == "computed":
            print(f"function was executed and returned a value of {result[0]}")
            return result[0]
    return wrapper

def cache_result(func):
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args], "restored from cache"
        else:
            result = func(*args)
            cache[args] = result
            return result, "computed"
    return wrapper

@log_call
@cache_result
def multiply(a, b):
    return a * b

multiply(3, 4)
multiply(3, 4)
multiply(5, 6)

@log_call
@cache_result
def fibo(n):
    if n <= 1:
        return n
    else:
        return fibo(n-1) + fibo(n-2)

fibo(40)


# 12.
import time

def throttle(limit, window):
    def decorator(func):
        recent_call_times = []
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal recent_call_times
            for a in recent_call_times:
                if time.time() - a > window:
                    recent_call_times.remove(a)
            if len(recent_call_times) < limit:
                recent_call_times.append(time.time())
                return func(*args, **kwargs)
            else:
                print("block")
                return None
        return wrapper
    return decorator

@throttle(3, 10)  # Allow 3 calls per 10 seconds
def process_request():
    print("Request processed")
s = 1
for _ in range(15):
    process_request()
    time.sleep(s)
