#coding:utf8

def memo(func):
    cache = {}
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap

@memo
def climb(n, steps):
    count = 0
    if n == 0:
        count =1
    elif n > 0:
        for step in steps:
            count += climb(n - step, steps)
    return count

print(climb(10, (1,2,3)))

