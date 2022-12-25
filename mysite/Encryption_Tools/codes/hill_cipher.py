from extendedEuclid import extendedEuclid
from numpy import linalg, matrix

def hill_cipher_2_enc(text, key):
    if len(key)!=2 or len(key[0])!=2 or len(key[1])!=2:
        return 'key must be 2x2 matrix'
    det=(key[0][0]*key[1][1]-key[0][1]*key[1][0])%26
    if det==0:
        return 'key is not invertible'
    elif extendedEuclid(det, 26)=='no inverse':
        return 'key is not invertible'
    if any(char.isdigit() for char in text):
        return 'text must be alphabetic only'
    text=text.lower().split(' ')
    for i in range(len(text)):
        if len(text[i])%2==1:
            text[i]+='x'
    result=[]
    for i in text:
        temp=''
        for j in range(0, len(i), 2):
            temp+=chr((key[0][0]*(ord(i[j])-97)+key[0][1]*(ord(i[j+1])-97))%26+97)
            temp+=chr((key[1][0]*(ord(i[j])-97)+key[1][1]*(ord(i[j+1])-97))%26+97)
        result.append(temp)
    return ' '.join(result)


def hill_cipher_2_dec(text, key):
    if len(key)!=2 or len(key[0])!=2 or len(key[1])!=2:
        return 'key must be 2x2 matrix'
    det=(key[0][0]*key[1][1]-key[0][1]*key[1][0])%26
    if det==0:
        return 'key is not invertible'
    elif extendedEuclid(det, 26)=='no inverse':
        return 'key is not invertible'
    if any(char.isdigit() for char in text):
        return 'text must be alphabetic only'
    inv=extendedEuclid(det, 26)
    inverse=[[(inv*key[1][1])%26,(-1*inv*key[0][1])%26],[(-1*inv*key[1][0])%26,(inv*key[0][0])%26]]
    text=text.lower().split(' ')
    result=[]
    for i in text:
        temp=''
        for j in range(0, len(i), 2):
            temp+=chr((inverse[0][0]*(ord(i[j])-97)+inverse[0][1]*(ord(i[j+1])-97))%26+97)
            temp+=chr((inverse[1][0]*(ord(i[j])-97)+inverse[1][1]*(ord(i[j+1])-97))%26+97)
        result.append(temp)
    return ' '.join(result)


def hill_cipher_3_enc(text, key):
    if len(key)!=3 or len(key[0])!=3 or len(key[1])!=3 or len(key[2])!=3:
        return 'key must be 3x3 matrix'
    det=linalg.det(matrix(key))%26
    if det==0:
        return 'key is not invertible'
    elif extendedEuclid(det, 26)=='no inverse':
        return 'key is not invertible'
    if any(char.isdigit() for char in text):
        return 'text must be alphabetic only'
    text=text.lower().split(' ')
    for i in range(len(text)):
        if len(text[i])%3==1:
            text[i]+='xx'
        elif len(text[i])%3==2:
            text[i]+='x'
    result=[]
    for i in text:
        temp=''
        for j in range(0, len(i), 3):
            temp+=chr((key[0][0]*(ord(i[j])-97)+key[0][1]*(ord(i[j+1])-97)+key[0][2]*(ord(i[j+2])-97))%26+97)
            temp+=chr((key[1][0]*(ord(i[j])-97)+key[1][1]*(ord(i[j+1])-97)+key[1][2]*(ord(i[j+2])-97))%26+97)
            temp+=chr((key[2][0]*(ord(i[j])-97)+key[2][1]*(ord(i[j+1])-97)+key[2][2]*(ord(i[j+2])-97))%26+97)
        result.append(temp)
    return ' '.join(result)


def invert_matrix_mod(mx, mod):
    det=linalg.det(mx)%mod
    if det==0:
        return 'key is not invertible'
    elif extendedEuclid(det, mod)=='no inverse':
        return 'key is not invertible'
    inv=extendedEuclid(int(det), mod)
    adj=[[None for i in range(5)] for i in range(5)]
    for i in range(3):
        adj[i]=[mx[i][0], mx[i][1], mx[i][2], mx[i][0], mx[i][1]]
    adj[3]=adj[0].copy()
    adj[4]=adj[1].copy()
    adj=[[adj[i][j] for j in range(1,5)] for i in range(1,5)]
    inverse=[[None for i in range(3)] for i in range(3)]
    for i in range(3):
        inverse[i]=[adj[0][i]*adj[1][i+1]-adj[0][i+1]*adj[1][i], adj[1][i]*adj[2][i+1]-adj[2][i]*adj[1][i+1], adj[2][i]*adj[3][i+1]-adj[3][i]*adj[2][i+1]]
    for i in range(3):
        for j in range(3):
            inverse[i][j]=(inverse[i][j]*inv)%mod
    return inverse


def hill_cipher_3_dec(text, key):
    if len(key)!=3 or len(key[0])!=3 or len(key[1])!=3 or len(key[2])!=3:
        return 'key must be 3x3 matrix'
    det=linalg.det(matrix(key))%26
    if det==0:
        return 'key is not invertible'
    elif extendedEuclid(det, 26)=='no inverse':
        return 'key is not invertible'
    if any(char.isdigit() for char in text):
        return 'text must be alphabetic only'
    inverse=invert_matrix_mod(key, 26)
    text=text.lower().split(' ')
    result=[]
    for i in text:
        temp=''
        for j in range(0, len(i), 3):
            temp+=chr((inverse[0][0]*(ord(i[j])-97)+inverse[0][1]*(ord(i[j+1])-97)+inverse[0][2]*(ord(i[j+2])-97))%26+97)
            temp+=chr((inverse[1][0]*(ord(i[j])-97)+inverse[1][1]*(ord(i[j+1])-97)+inverse[1][2]*(ord(i[j+2])-97))%26+97)
            temp+=chr((inverse[2][0]*(ord(i[j])-97)+inverse[2][1]*(ord(i[j+1])-97)+inverse[2][2]*(ord(i[j+2])-97))%26+97)
        result.append(temp)
    return ' '.join(result)

if __name__ == '__main__':
    print(hill_cipher_2_enc("we are discovered save yourself", [[5, 8], [17, 3]]))
    print(hill_cipher_2_dec("mw gzwh bxcaepapsz muhf yicbsgru", [[5, 8], [17, 3]]))
    print(hill_cipher_3_enc("pay more money", [[17,17,5],[21,18,21],[2,2,19]]))
    print(hill_cipher_3_dec("lns hdlctx nxntlz", [[17,17,5],[21,18,21],[2,2,19]]))