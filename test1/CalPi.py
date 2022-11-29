# CalPi.py
import random
DARTS = eval(input())
random.seed(123)
hits = 0
for i in range(1, DARTS + 1):
    x, y = random.random(), random.random()
    dist = pow(x ** 2 + y ** 2, 0.5)
    if dist <= 1:
        hits += 1
pi = 4 * (hits / DARTS)
print("{:.6f}".format(pi))
