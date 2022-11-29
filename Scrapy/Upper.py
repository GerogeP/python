def upper_right(words):

    # All lower
    if words.islower():
        return True
    # All  upper
    if words.isupper():
        return True

    # only first letter upper
    first_letter = words[:1]
    if first_letter.isupper():
        if words[1:].islower():
            return True

    return False


print('USA', upper_right('USA'))
print('FlaG', upper_right('FlaG'))
print('FlaG', upper_right('Flag'))
print('FlaG', upper_right('Flag2'))
print('FlaG', upper_right('flag2'))
