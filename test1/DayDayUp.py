# DayDayUp.py
dayUp = 1
factor = 0.01
A = round(pow(dayUp * (1 + factor), 365), 3)


def res(factor):
    dayUp = 1
    for i in [365]:
        if i % 7 in [0, 6]:
            dayUp *= (1 - factor)
        else:
            dayUp *= (1 + factor)
    return dayUp


print(A)
f = 0.01
while res(f) < A:
    f += 0.001
print("{:.3f}".format(f))
