#coding:utf8

def fibonacci(n,cache=None):
    if cache is None:
        cache = {}

    if n in cache:
        return cache[n]

    if n <= 1:
        return 1

    cache[n] = fibonacci(n - 1, cache) + fibonacci(n -2, cache)

    return cache[n]

print(fibonacci(50))

