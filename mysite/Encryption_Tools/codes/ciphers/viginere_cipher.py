

def viginere_cipher_enc(text, key):
    if any(char.isdigit() for char in text) or any(char.isdigit() for char in key):
        return 'text and key must be alphabetic only'
    result = ''
    for i, char in enumerate(text):
        if (char.isupper()):
            char=char.lower()
        result += chr((ord(char) + ord(key[i % len(key)]) - 97 - 97) % 26 + 97) if char != ' ' else ' '

    return result

def viginere_cipher_dec(text, key):
    if any(char.isdigit() for char in text) or any(char.isdigit() for char in key):
        return 'text and key must be alphabetic only'
    result = ''
    for i, char in enumerate(text):
        if (char.isupper()):
            char=char.lower()
        result += chr((ord(char) - ord(key[i % len(key)])) % 26 + 97) if char != ' ' else ' '

    return result

if __name__ == '__main__':
    print(viginere_cipher_enc("we are discovered save yourself", "deceptive"))
    print(viginere_cipher_dec("zi egx ymvgqztkmy vexi rwpvvinj", "deceptive"))
