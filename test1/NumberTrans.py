# NumberTrans.py
I = input()
A = "零一二三四五六七八九"
for N in I:
    print(A[eval(N)], end="")
