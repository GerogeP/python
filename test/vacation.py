def solution(a):
    # Write your answer here
    short = len(a)
    counter = 1
    while counter < len(a):
        cut = a[:counter]
        if set(cut) == set(a):
            short = len(set(cut)) if len(set(cut)) < short else short
        counter += 1
    return short


if __name__ == '__main__':
    a = [1, 2, 23,6, 17]
    print(solution(a))
    print('adfadf'[-1].isalpha())
