from collections import OrderedDict
from functools import wraps

def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]
    return fibonacci

# Better solution (Universal Memo Decorator)
# React dev says hi 👋
# def useMemo(func = None, *, maxCacheSize=None):
#     def decorator(f):
#         cache = OrderedDict()
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             key = (args, tuple(sorted(kwargs.items())))
#             if key in cache:
#                 cache.move_to_end(key)
#                 return cache[key]
#             result = f(*args, **kwargs)
#             cache[key] = result
#             if maxCacheSize is not None and len(cache) > maxCacheSize:
#                 cache.popitem(last=False)
#             return result
#         return wrapper
#
#     if func is None:
#         return decorator
#     else:
#         return decorator(func)
#
# @useMemo
# def fibonacci(n):
#     if n <= 0:
#         return 0
#     if n == 1:
#         return 1
#
#     return fibonacci(n - 1) + fibonacci(n - 2)



if __name__ == '__main__':
    fib = caching_fibonacci()
    while True:
        print(f"Result: {fib(int(input('Print number: ')))}")