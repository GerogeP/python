#!/bin/python3

import math
import os
import random
import re
import sys


#
# Complete the 'getMin' function below.
#
# The function is expected to return an INTEGER.
# The function accepts STRING s as parameter.
#

def getMin(s):
    # Write your code here
    parens = len(s)
    lefts = 0
    rights = 0
    for i in range(len(s)):
        if s[i] == '(':
            lefts += 1
        if s[i] == ')':
            rights += 1

    return rights - lefts


if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = '()))'

    result = getMin(s)
    print(result)
    # fptr.write(str(result) + '\n')
    #
    # fptr.close()
