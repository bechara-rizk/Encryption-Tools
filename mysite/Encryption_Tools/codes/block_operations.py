try:
    from aes import AES
    from des import DES
    from partition import partition_pad, partition_unpad
except:
    from .aes import AES
    from .des import DES
    from .partition import partition_pad, partition_unpad
from random import randint


def ECB(sch, key, data, op,iv=None):
    result = []
    cipher=sch(key)
    if op == 'encrypt':
        data=partition_pad(data, cipher.blocksize)
        for i in data:
            result.append(cipher.encrypt(i))
        return ''.join(result)
    else:
        temp=data
        data=[]
        for i in range(len(temp)//(cipher.blocksize//4)):
            data.append(temp[i*(cipher.blocksize//4):(i+1)*(cipher.blocksize//4)])
        for i in data:
            result.append(cipher.decrypt(i))
        result = ''.join(result)
        result=partition_unpad(result, cipher.blocksize)
        return result

def CBC(sch, key, data, op, iv=None):
    result=[]
    cipher=sch(key)
    if op == 'encrypt':
        if iv is None:
            temp=randint(0, 2**(cipher.blocksize)-1)
            iv=hex(temp)[2:].zfill(cipher.blocksize//4)
        data=partition_pad(data, cipher.blocksize)
        for i in range(len(data)):
            if i==0:
                temp=hex(int(data[i], 16) ^ int(iv, 16))[2:].zfill(cipher.blocksize//4)
            else:
                temp=hex(int(data[i], 16) ^ int(result[-1], 16))[2:].zfill(cipher.blocksize//4)
            temp=cipher.encrypt(temp)
            result.append(temp)
        return iv,''.join(result)
    else:
        if iv is None or len(iv) != cipher.blocksize//4:
            return 'Invalid IV'
        temp = data
        data = []
        for i in range(len(temp)//(cipher.blocksize//4)):
            data.append(temp[i*(cipher.blocksize//4):(i+1)*(cipher.blocksize//4)])
        for i in range(len(data)):
            result.append(cipher.decrypt(data[i]))
            if i==0:
                result[i]=hex(int(result[i], 16) ^ int(iv, 16))[2:].zfill(cipher.blocksize//4)
            else:
                result[i]=hex(int(result[i], 16) ^ int(data[i-1], 16))[2:].zfill(cipher.blocksize//4)
        result = ''.join(result)
        result=partition_unpad(result, cipher.blocksize)
        return iv,result

def CFB(sch, key, data, op, iv=None):
    return 'Not Implemented'

def OFB(sch, key, data, op ,nonce=None):
    result=[]
    cipher=sch(key)
    if op == 'encrypt':
        if nonce is None:
            temp=randint(0, 2**(cipher.blocksize)-1)
            nonce=hex(temp)[2:].zfill(cipher.blocksize//4)
        data=partition_pad(data, cipher.blocksize)
        for i in range(len(data)):
            if i==0:
                temp=cipher.encrypt(nonce)
            else:
                temp=cipher.encrypt(result[-1])
            result.append(temp)
        for i in range(len(result)):
            result[i]=hex(int(result[i], 16) ^ int(data[i], 16))[2:].zfill(cipher.blocksize//4)
        return nonce,''.join(result)
    else:
        if nonce is None or len(nonce) != cipher.blocksize//4:
            return 'Invalid Nonce'
        temp = data
        data = []
        for i in range(len(temp)//(cipher.blocksize//4)):
            data.append(temp[i*(cipher.blocksize//4):(i+1)*(cipher.blocksize//4)])
        for i in range(len(data)):
            if i==0:
                temp=cipher.encrypt(nonce)
            else:
                temp=cipher.encrypt(result[-1])
            result.append(temp)
        for i in range(len(result)):
            result[i]=hex(int(result[i], 16) ^ int(data[i], 16))[2:].zfill(cipher.blocksize//4)
        result = ''.join(result)
        result=partition_unpad(result, cipher.blocksize)
        return nonce,result
    
def CTR(sch, key, data, op):
    return 'Not Implemented'


def operation(scheme, mode, key, data, op, iv=None):
    scheme=scheme.lower()
    schemes={'aes':AES, 'des':DES}
    if scheme in schemes:
        scheme=schemes[scheme]
    else:
        return 'Invalid Scheme'
    mode=mode.lower()
    modes={'ecb':ECB, 'cbc':CBC, 'cfb':CFB, 'ofb':OFB, 'ctr':CTR}
    if mode in modes:
        mode=modes[mode]
    else:
        return 'Invalid Mode'
    op=op.lower()
    if op == 'encrypt' or op == 'decrypt':
        return mode(scheme, key, data, op, iv)
    else:
        return 'Invalid Operation'
    

if __name__=='__main__':
    key = '0f1571c947d9e8590cb7add6af7f6798'
    data='6bc1bee22e409f172a372832949392020830947823984723'
    result=operation('aes', 'ecb', key, data, 'encrypt')
    print(result)
    res2=operation('aes', 'ecb', key, result, 'decrypt')
    print('AES, ECB',res2==data)

    key = '0f1571c947d9e859'
    data='6bc1bee22e409f172a372832949392020830947823984723'
    result=operation('des', 'ecb', key, data, 'encrypt')
    res2=operation('des', 'ecb', key, result, 'decrypt')
    print('DES, ECB',res2==data)

    key = '0f1571c947d9e8590cb7add6af7f6798'
    # key=key+key
    data='6bc1bee22e409f172a372832949392020830947823984723'
    iv,result=operation('aes', 'cbc', key, data, 'encrypt')
    # print(result,iv)
    res2=operation('aes', 'cbc', key, result, 'decrypt', iv)
    print('AES, CBC',res2==data)

    key = '0f1571c947d9e859'
    data='6bc1bee22e409f172a372832949392020830947823984723'
    iv,result=operation('des', 'cbc', key, data, 'encrypt')
    res2=operation('des', 'cbc', key, result, 'decrypt',iv)
    print('DES, CBC',res2==data)

    key = '0f1571c947d9e8590cb7add6af7f6798'
    # key=key+key
    data='6bc1bee22e409f172a372832949392020830947823984723'
    nonce,result=operation('aes', 'ofb', key, data, 'encrypt')
    # print(result,iv)
    res2=operation('aes', 'ofb', key, result, 'decrypt', nonce)
    print('AES, OFB',res2==data)

    key = '0f1571c947d9e859'
    data='6bc1bee22e409f172a372832949392020830947823984723'
    nonce,result=operation('des', 'ofb', key, data, 'encrypt')
    res2=operation('des', 'ofb', key, result, 'decrypt',nonce)
    print('DES, OFB',res2==data)