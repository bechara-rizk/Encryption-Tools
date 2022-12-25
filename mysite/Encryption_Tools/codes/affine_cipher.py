from extendedEuclid import extendedEuclid

def affine_cipher_enc(text, a, b):
    if extendedEuclid(a, 26) == 'no inverse':
        return f'{a} and 26 are not relatively prime'
    result = ''
    for char in text:
        if (char.isupper()):
            char=char.lower()
        if not char.isnumeric():
            result += chr(((ord(char)-97)*a+b)%26+97) if char != ' ' else ' '
        else:
            result += char
    return result


def affine_cipher_dec(text, a, b):
    inverse = extendedEuclid(a, 26)
    if inverse == 'no inverse':
        return f'{a} and 26 are not relatively prime'
    result = ''
    for char in text:
        if (char.isupper()):
            char=char.lower()
        if not char.isnumeric():
            result += chr(((ord(char)-97-b)*inverse)%26+97) if char != ' ' else ' '
        else:
            result += char
    return result

if __name__ == '__main__':
    print(affine_cipher_enc("ATTACK AT ONCE 3", 5, 3))
    print(affine_cipher_dec("duudnb du vqnx 3", 5, 3))