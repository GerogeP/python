def passed_rate(names, results):

    print(names, results)

    def name_simple(names):
        length = len(names)
        index = 0
        while index < length:
            if names[index][-2:-1] in ['1','2','3','4','5','6','7','8','9']:
                names[index] = names[index][:-1]
            index += + 1

        return names

    name_simple(names)

    not_passed = []
    index = 0
    while index < len(names):
        if names[index] not in not_passed and results[index] != 'passed':
            not_passed.append(names[index])
        
        index += 1

    return 100 * ((len(set(names)) - len(not_passed)) / len(set(names)))

if __name__ == '__main__':
    n = ['test1', 'test2a', 'test2b']
    r = ['passed', 'failed', 'passed']

    print(passed_rate(n,r))

