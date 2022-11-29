#!/bin/python3

import math
import os
import random
import re
import sys


#
# Complete the 'isPrime' function below.
#
# The function is expected to return an INTEGER.
# The function accepts LONG_INTEGER n as parameter.
#

def isPrime(n):
    # Write your code here
    is_prime = False
    for i in range(2, n - 1):
        if n % i == 0:
            is_prime = True
            return i
    # if not is_prime:
    return 1


if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = 11

    result = isPrime(n)
    print(result)
    # fptr.write(str(result) + '\n')

    # fptr.close()