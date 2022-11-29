# CeaserCode.py
I = input()
for P in I:
    print(P, end='')
    if P == ' ':
        C = ' '
    else:
        C = chr((ord(P) + 3) % 26)
    print(C, end='')
