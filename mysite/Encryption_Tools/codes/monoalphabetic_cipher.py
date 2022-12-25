

def monoalphabetic_cipher_enc(text, key):
    if any(char.isdigit() for char in text) or any(char.isdigit() for char in key):
        return 'text and key must be alphabetic only'
    result = ''
    for char in text:
        if (char.isupper()):
            char=char.lower()
        result += key[ord(char)-97] if char != ' ' else ' '

    return result

def monoalphabetic_cipher_dec(text, key):
    if any(char.isdigit() for char in text) or any(char.isdigit() for char in key):
        return 'text and key must be alphabetic only'
    result = ''
    for char in text:
        if (char.isupper()):
            char=char.lower()
        result += chr(key.index(char)+97) if char != ' ' else ' '

    return result

if __name__ == '__main__':
    print(monoalphabetic_cipher_enc('if we wish to replace letters', 'dkvqfibjwpescxhtmyauolrgzn'))
    print(monoalphabetic_cipher_dec('wi rf rwaj uh yftsdvf sfuufya', 'dkvqfibjwpescxhtmyauolrgzn'))