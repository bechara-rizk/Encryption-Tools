
def caesar_cipher_enc(text, key):
    result = ""
    for char in text:
        if (char.isupper()):
            char=char.lower()
        if not char.isnumeric():
            result += chr((ord(char) + key - 97) % 26 + 97) if char != " " else " "
        else:
            result += char
    return result

def caesar_cipher_dec(text, key):
    result = ""
    for char in text:
        if (char.isupper()):
            char=char.lower()
        if not char.isnumeric():
            result += chr((ord(char) - key - 97) % 26 + 97) if char != " " else " "
        else:
            result += char
    return result

if __name__ == '__main__':
    print(caesar_cipher_enc("ATTACK AT ONCE 3", 6))
    print(caesar_cipher_dec("gzzgiq gz utik 3", 6))