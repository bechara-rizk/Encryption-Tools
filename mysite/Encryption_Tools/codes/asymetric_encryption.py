from random import randint
from .primes import rel_prime, test_prime, primitive_root_test
from .extendedEuclid import extendedEuclid
from .exponentiation import exponentiation

def RSA_setup(p, q, e=None):
    n=p*q
    phi=(p-1)*(q-1)
    if e is None:
        e=randint(2,phi-1)
        while not rel_prime(e,phi):
            e=randint(2,phi-1)
    d=extendedEuclid(e,phi)
    return (n,phi,e,d)

def RSA_encrypt(m, e, n):
    return exponentiation(m,e,n)

def RSA_decrypt(c, d, n):
    return exponentiation(c,d,n)

def DH_key_exchange(q, a, xa, xb):
    if not test_prime(q):
        return False
    if a is None:
        a=randint(2,q-2)
        while not primitive_root_test(q,a):
            a=randint(2,q-2)
    else:
        if not primitive_root_test(q,a):
            return False
    if xa is None:
        xa=randint(2,q-2)
    else:
        if xa<2 or xa>=q:
            return False
    if xb is None:
        xb=randint(2,q-2)
    else:
        if xb<2 or xb>=q:
            return False
    ya=exponentiation(a,xa,q)
    yb=exponentiation(a,xb,q)
    key=exponentiation(yb,xa,q)
    return (a,xa,xb,ya,yb,key)

def el_gamal_setup(q, a=None, xa=None):
    if not test_prime(q):
        return False
    if a is None:
        a=randint(2,q-2)
        while not primitive_root_test(q,a):
            a=randint(2,q-2)
    else:
        if not primitive_root_test(q,a):
            return False
    if xa is None:
        xa=randint(2,q-2)
    ya=exponentiation(a,xa,q)
    return (q,a,xa,ya)

def el_gamal_encrypt(m, q, a, ya):
    if m<0 or m>=q:
        return False
    r=randint(1,q-1)
    k=exponentiation(ya,r,q)
    c1=exponentiation(a,r,q)
    c2=(m*k)%q
    return (c1,c2)

def el_gamal_decrypt(c1, c2, q, xa):
    k=exponentiation(c1,xa,q)
    inv_k=extendedEuclid(k,q)
    m=(c2*inv_k)%q
    return m


if __name__=='__main__':
    p=11
    q=17
    n,e,d=RSA_setup(p,q)
    print(n,e,d)
    M=88
    C=RSA_encrypt(M,e,n)
    print(C)
    m=RSA_decrypt(C,d,n)
    print(m)
    print(DH_key_exchange(353,3,97,233))
    print(el_gamal_setup(19,10,5))
    c1,c2=el_gamal_encrypt(17,19,10,3)
    print(c1,c2)
    print(el_gamal_decrypt(c1,c2,19,5))