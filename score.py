def solution(a):
    # Write your answer
    if len(a) == 1:
        return a[0]
    if len(a) > 1000:
        return
    new_a = []
    counter = 0
    
    while counter < len(a) -1:
        if a[counter].isnumeric():
            new_a.append(int(a[counter]))
        if counter > 0 and a[counter] == 'D':
            new_a.append(2 * int(new_a[-1]))
        if counter > 0 and a[counter] == 'C':
            new_a.pop()
        if counter > 1 and a[counter] == '+':
            new_a.append(int(new_a[-2]) + int(new_a[-1]))
        counter += 1

        print('{}---{}:'.format(counter, new_a))
        
    result = 0
    
    if len(new_a) > 1:
        for num in new_a:
            result += num
    else:
        result = new_a[0]
    return result

if __name__ == '__main__':
    print(solution(["5"]))
    print(solution(["5","2","C","D","+"]))
    print(solution([5]))
    
