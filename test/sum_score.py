def solution(a):
    # Write your answer
    current = []
    counter = 0
    while counter < len(a):
        if a[counter].isnumeric():
            current.append(a[counter])

        if a[counter] == 'C':
            current = current[:-1]

        if a[counter] == 'D':
            current.append(int(current[-1]) * 2)

        if a[counter] == '+':
            current.append(int(current[-1]) + int(current[-2]))

        counter += 1

    sum = 0
    for s in current:
        sum += int(s)

    return sum


if __name__ == '__main__':

    print(solution(['5', '2', 'C', 'D', '+']))
    # print(['5', '2', 'C', 'D', '+'][-1])
