

def partition_pad(data, length):
    binary = bin(int(data, 16))[2:].zfill(len(data)*4)
    multiple = len(binary)//length+1
    missing = length-len(binary) % length
    if missing == length:
        missing = ''.zfill(length)
        binary += missing
    else:
        multiple += 1
        missing = bin(missing)[2:].zfill(length)
        # need to fill zeroes then add missing
        binary += '0'*(length-len(binary) % length)
        binary += missing

    data = hex(int(binary, 2))[2:].zfill(len(binary)//4)
    result = []
    for i in range(multiple):
        result.append(data[i*length//4:(i+1)*length//4])
    return result


def partition_unpad(data, length):
    binary = bin(int(data, 16))[2:].zfill(len(data)*4)
    temp = binary
    binary = []
    for i in range(len(temp)//length):
        binary.append(temp[i*length:(i+1)*length])
    missing = binary.pop()
    missing = int(missing, 2)
    if missing == 0:
        result = ''.join(binary)
        result = hex(int(result, 2))[2:].zfill(len(result)//4)
    else:
        binary[-1] = binary[-1][:-missing]
        result = ''.join(binary)
        result = hex(int(result, 2))[2:].zfill(len(result)//4)
    return result


if __name__ == '__main__':
    test = '0123456789abcdef0123456789ab'
    length=64
    result=partition_pad(test, length)
    print(result)
    res=partition_unpad(''.join(result), length)
    print(res)
    print(res==test)
