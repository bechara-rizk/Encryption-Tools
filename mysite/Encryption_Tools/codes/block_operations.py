from aes import AES
from des import DES
from partition import partition_pad, partition_unpad


def ECB(sch, key, data, op):
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

def CBC(sch, key, data, op):
    pass

def CFB(sch, key, data, op):
    pass

def OFB(sch, key, data, op):
    pass
    
def CTR(sch, key, data, op):
    pass


def operation(scheme, mode, key, data, op):
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
        return mode(scheme, key, data, op)
    else:
        return 'Invalid Operation'
    

if __name__=='__main__':
    key = '0f1571c947d9e8590cb7add6af7f67980f1571c947d9e859'
    data='6bc1bee22e409f172a372832949392020830947823984723'
    result=operation('aes', 'ecb', key, data, 'encrypt')
    res2=operation('aes', 'ecb', key, result, 'decrypt')
    print('AES, ECB',res2==data)

    key = '0f1571c947d9e859'
    data='6bc1bee22e409f172a372832949392020830947823984723'
    result=operation('des', 'ecb', key, data, 'encrypt')
    res2=operation('des', 'ecb', key, result, 'decrypt')
    print('DES, ECB',res2==data)