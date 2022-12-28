

def row_transposition_cipher_enc(text, key):
    if any(char.isalpha() for char in key):
        return 'key must be numeric only'
    check_key=[False for i in range(len(key))]
    for i in key:
        check_key[int(i)-1]=True
    if not all(check_key):
        return 'key must be permutation of 1 to n'
    range_partitioned=len(text)//len(key) if len(text)%len(key)==0 else len(text)//len(key)+1
    partitioned=['' for i in range(range_partitioned)]
    for i in range(0, len(text), len(key)):
        partitioned[i//len(key)]+=text[i:i+len(key)]
    longest=len(partitioned[0])
    result=''
    for i in range(longest):
        idx=key.index(str(i+1))
        for j in range(range_partitioned):
            if idx<len(partitioned[j]):
                result+=partitioned[j][idx]
    return result


def row_transposition_cipher_dec(text, key):
    if any(char.isalpha() for char in key):
        return 'key must be numeric only'
    check_key=[False for i in range(len(key))]
    for i in key:
        check_key[int(i)-1]=True
    if not all(check_key):
        return 'key must be permutation of 1 to n'
    partitioned=['' for i in range(len(key))]
    divided=len(text)//len(key)
    rem_start=len(text)%len(key)
    rem=rem_start
    for i in range(len(key)):
        key_index=int(key[i])-1
        jump=0
        if rem>0:
            for j in range(rem):
                jump+=1 if int(key[i+j])-1<key_index else 0
            for j in range(0,i):
                jump+=1 if int(key[j])-1<key_index else 0
            partitioned[i]+=text[key_index*divided+jump:divided+key_index*divided+jump+1]
            rem-=1
        else:
            for j in range(rem_start):
                jump+=1 if int(key[j])-1<key_index else 0
            partitioned[i]+=text[key_index*divided+jump:divided+key_index*divided+jump]
    result=''
    for i in range(len(partitioned[0])):
        for j in range(len(key)):
            if len(partitioned[j])<i+1:
                break
            result+=partitioned[j][i]
    return result


if __name__ == '__main__':
    print(row_transposition_cipher_enc('ATTACK POSTPONED UNTIL TWO AM', '4312567'))
    print(row_transposition_cipher_dec('TS TATUWTOD APELMCPNOKOT  NIA', '4312567'))