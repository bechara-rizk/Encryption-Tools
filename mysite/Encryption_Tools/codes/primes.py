from extendedEuclid import extendedEuclid

def prime_list(x):
    """Returns a list of primes up to x"""
    lst=[True for i in range(x+1)]
    lst[0]=False
    lst[1]=False
    percent=x/10
    for i in range(2,x+1):
        if lst[i]:
            for j in range(i*i,x+1,i):
                lst[j]=False
        if i%percent==0:
            print(i/percent*10,"%")
    return [i for i in range(x+1) if lst[i]]

def test_prime(x):
    """Returns True if x is prime"""
    if x==1:
        return False
    if x==2:
        return True
    if x%2==0:
        return False
    for i in range(3,int(x**0.5)+1):
        if x%i==0:
            return False
    return True

def prime_factorization(x,prime_list):
    """Returns a list of prime factors of x"""
    lst=[]
    i=0
    while i<len(prime_list) and x>1:
        if x%prime_list[i]==0:
            lst.append(prime_list[i])
            x=x//prime_list[i]
        else:
            i+=1
    powers=dict()
    for i in lst:
        if i in powers:
            powers[i]+=1
        else:
            powers[i]=1
    return lst, powers

def rel_prime(x,y):
    """Returns True if x and y are relatively prime"""
    if x==1 or y==1:
        return True
    if x==0 or y==0:
        return False
    if x%y==0 or y%x==0:
        return False
    if x>y:
        return rel_prime(x%y,y)
    else:
        return rel_prime(x,y%x)

def totient(x):
    """Returns the totient of x"""
    if x==1:
        return 0
    res=[]
    if test_prime(x):
        return x-1
    for i in range(x):
        if rel_prime(i,x):
            res.append(i)
    return len(res)

from random import randint
from exponentiation import exponentiation

def milller_rabbin(n, rounds=1, a=None):
    if rounds<1 or n<2 or (a is not None and (a<2 or a>=n)):
        return False
    k=0
    q=n-1
    while q%2==0:
        k+=1
        q=q//2
    for i in range(rounds):
        if a is None: a=randint(2,n-2)
        if exponentiation(a,q,n) == 1:
            continue
        for i in range(k):
            exit=False
            if exponentiation(a,2**i*q,n) == n-1:
                exit=True
                break
        if exit:
            continue
        return False
    return True

def primitive_roots(n):
    phi=totient(n)
    roots=[]
    for a in range(1,n):
        if rel_prime(a,n):
            for i in range(1,phi+1):
                if exponentiation(a,i,n)==1:
                    if i==phi:
                        roots.append(a)
                    break
    return roots

def primitive_root_test(n, a):
    phi=totient(n)
    if rel_prime(a,n):
        for i in range(1,phi+1):
            if exponentiation(a,i,n)==1:
                if i==phi:
                    return True
    return False

def disc_log(result, base, mod):
    if not primitive_root_test(mod,base):
        return f'{base} is not a primitive root of {mod}'
    if result<=0 or result>=mod:
        return f'{result} is not a valid result'
    if base<=0 or base>=mod:
        return f'{base} is not a valid base'
    phi=totient(mod)
    if result==1:
        return phi
    temp=base
    for i in range(1,phi+1):
        if temp==result:
            return i
        temp=(temp*base)%mod

def disc_log_table(base, mod):
    result=[]
    for i in range(1,mod):
        result.append((i,disc_log(i,base,mod)))
    return result

def CRT(mi,A):
    M=1
    for i in mi:
        M*=i
    L=len(mi)
    if isinstance(A,int):
        ai=[]
        for i in mi:
            ai.append(A%i)
    elif isinstance(A,list):
        ai=A
        A=None
    Mi=[]
    for i in mi:
        Mi.append(M//i)
    inv_Mi=[]
    for i in range(L):
        inv_Mi.append(extendedEuclid(Mi[i],mi[i]))
        if inv_Mi[i]=='no inverse':
            return 'error in m_i'
    A=0
    for i in range(L):
        A+=(ai[i]*Mi[i]*inv_Mi[i])%M
    return A%M


if __name__=='__main__':
    print(CRT([3,5,7], 233))


if __name__ == "__main__2":
    # p=prime_list(100_000_000)
    # print(len(p))
    # file=open("primes.txt","w")
    # for i in p:
    #     file.write(str(i)+",")
    # file.close()
    
    # file =open("mysite/Encryption_Tools/codes/primes.txt","r")
    # prime=[]
    # x=file.read()
    # for i in x.split(","):
    #     try:
    #         prime.append(int(i))
    #     except:
    #         pass
    # file.close()

    # print(prime_factorization(3600,prime))
    print(rel_prime(7,10))
    print(test_prime(99711907))
    print(totient(13))
    print(milller_rabbin(99711907))
    print(milller_rabbin(221))
    # print(primitive_roots(1021))
    # print(primitive_root_test(1021,538))
    print(primitive_roots(9))
    print(primitive_root_test(9,2))
    print(disc_log(6,2,9))
    print(disc_log_table(2,19))
    print(disc_log_table(2,9))