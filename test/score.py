def solution(n, r):
    # Write your answer here
    groups = []
    for group in n:
        if group[-1].isalpha():
            g = group[:-1]
            groups.append(g)
        else:
            groups.append(group)

    groups = set(groups)
    total = len(groups)
    passed = 0
    for g in groups:
        if g[-1].isnumeric():
            counter = 0
            while counter < len(n) - 1:
                counter += 1
                if n[counter] == g and r[counter] == 'passed':
                    passed += 1
        else:
            counter = 0
            while counter < len(n) - 1:
                counter += 1
                if n[counter][:-1] == g:
                    if r[counter] == 'failed':
                        break
            passed += 1

    return passed * 100 / total


if __name__ == '__main__':
    print(solution(['sfsf','adaa1a', 'adaa1b'], ['passed', 'passed', 'failed']))
