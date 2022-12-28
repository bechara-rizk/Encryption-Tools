

def find_position(mx, letter):
    for i in range(5):
        for j in range(5):
            if mx[i][j] == letter:
                return (i, j)


def playfair_cipher_enc(text, key):
    if any(char.isdigit() for char in text) or any(char.isdigit() for char in key):
        return 'text and key must be alphabetic only'
    key=key.lower()
    text=text.lower()
    letters=[chr(i) for i in range(97, 123)]
    letters.remove('j')
    mx=[[None for i in range(5)] for i in range(5)]
    for i in range(len(key)):
        if key[i] == 'j': key[i] = 'i'
        mx[i//5][i%5]=key[i]
        letters.remove(key[i])
    for i in range(len(key), 25):
        mx[i//5][i%5]=letters[i-len(key)]
    
    for i in range(len(text)):
        if text[i] == 'j': text=text[:i]+'i'+text[i+1:]
    text=text.split(' ')
    i=0
    for i in range(len(text)):
        j=0
        while j<len(text[i])-1:
            if text[i][j]==text[i][j+1]:
                if text[i][j]!='x':
                    text[i]=text[i][:j+1]+'x'+text[i][j+1:]
                else:
                    text[i]=text[i][:j+1]+'w'+text[i][j+1:]
            j+=2
        if len(text[i])%2==1:
            if text[i][-1]!='x':
                text[i]+='x'
            else:
                text[i]+='w'

    result=[]
    for i in text:
        temp=''
        for j in range(0, len(i), 2):
            pos1=find_position(mx, i[j])
            pos2=find_position(mx, i[j+1])
            if pos1[0]==pos2[0]:
                temp+=mx[pos1[0]][(pos1[1]+1)%5]+mx[pos2[0]][(pos2[1]+1)%5]
            elif pos1[1]==pos2[1]:
                temp+=mx[(pos1[0]+1)%5][pos1[1]]+mx[(pos2[0]+1)%5][pos2[1]]
            else:
                temp+=mx[pos1[0]][pos2[1]]+mx[pos2[0]][pos1[1]]
        result.append(temp)
    return ' '.join(result)

def playfair_cipher_dec(text, key):
    if any(char.isdigit() for char in text) or any(char.isdigit() for char in key):
        return 'text and key must be alphabetic only'
    key=key.lower()
    text=text.lower()
    letters=[chr(i) for i in range(97, 123)]
    letters.remove('j')
    mx=[[None for i in range(5)] for i in range(5)]
    for i in range(len(key)):
        if key[i] == 'j': key[i] = 'i'
        mx[i//5][i%5]=key[i]
        letters.remove(key[i])
    for i in range(len(key), 25):
        mx[i//5][i%5]=letters[i-len(key)]

    for i in range(len(text)):
        if text[i] == 'j': text=text[:i]+'i'+text[i+1:]
    text=text.split(' ')
    i=0
    for i in range(len(text)):
        j=0
        while j<len(text[i])-1:
            if text[i][j]==text[i][j+1]:
                if text[i][j]!='x':
                    text[i]=text[i][:j+1]+'x'+text[i][j+1:]
                else:
                    text[i]=text[i][:j+1]+'w'+text[i][j+1:]
            j+=2
        if len(text[i])%2==1:
            if text[i][-1]!='x':
                text[i]+='x'
            else:
                text[i]+='w'
    
    result=[]
    for i in text:
        temp=''
        for j in range(0, len(i), 2):
            pos1=find_position(mx, i[j])
            pos2=find_position(mx, i[j+1])
            if pos1[0]==pos2[0]:
                temp+=mx[pos1[0]][(pos1[1]-1)%5]+mx[pos2[0]][(pos2[1]-1)%5]
            elif pos1[1]==pos2[1]:
                temp+=mx[(pos1[0]-1)%5][pos1[1]]+mx[(pos2[0]-1)%5][pos2[1]]
            else:
                temp+=mx[pos1[0]][pos2[1]]+mx[pos2[0]][pos1[1]]
        result.append(temp)
    #might add later function to remove fillers x and w
    return ' '.join(result)

if __name__ == '__main__':
    print(playfair_cipher_enc("ATTACK AT ONE", "monarchy"))
    print(playfair_cipher_dec("rssrde rs naiu", "monarchy"))