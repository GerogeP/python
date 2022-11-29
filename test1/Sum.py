sum = 1
for i in range(1, 100):
    isSu = 1
    for j in range(1, i):
        if j != 1 and i != j and i % j == 0:
            isSu = 0
            break
    if isSu == 1:
        sum += i
print(sum)
