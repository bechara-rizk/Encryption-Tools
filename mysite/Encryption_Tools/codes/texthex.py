

def text_to_hex(text):
    result = ''
    for i in text:
        result += hex(ord(i))[2:]
    return result


def hex_to_text(hex):
    if len(hex)%2!=0:
        hex= '0' + hex
    result = ''
    for i in range(0, len(hex), 2):
        result += chr(int(hex[i:i+2], 16))
    return result

if __name__=='__main__':
    print(text_to_hex('hello world!'))
    print(hex_to_text('68656c6c6f20776f726c6421'))