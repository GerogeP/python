#coding:utf8

def memo(func):
    cache = {}
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap

@memo
def fibonacci(n):
    if n <= 1:
        return 1
    return fibonacci(n-1) + fibonacci(n - 2)

#fibonacci = memo(fibonacci)
print(fibonacci(50))

