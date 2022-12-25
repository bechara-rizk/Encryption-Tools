

def rail_fence_cipher_enc(text, depth):
    if not str(depth).isdigit():
        return 'depth must be an integer'
    result=['' for i in range(depth)]
    for i in range(len(text)):
        result[i%depth]+=text[i]
    return ''.join(result)


def rail_fence_cipher_dec(text, depth):
    if not str(depth).isdigit():
        return 'depth must be an integer'
    div=len(text)//depth
    rem=len(text)%depth    
    partitioned=['' for i in range(depth)]
    taken=0
    for i in range(depth):
        partitioned[i]=text[taken:taken+div]
        taken+=div
        if rem>0:
            partitioned[i]+=text[taken]
            taken+=1
            rem-=1
    result=''
    for i in range(len(partitioned[0])):
        for j in range(depth):
            if len(partitioned[j])<i+1:
                break
            result+=partitioned[j][i]
    return result


if __name__ == '__main__':
    print(rail_fence_cipher_enc('meet me after the toga party', 5))
    print(rail_fence_cipher_dec('mmthgreeeeate r  yta tp ftoa', 5))