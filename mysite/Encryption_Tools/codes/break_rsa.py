

from math import ceil, sqrt
try:
    import primes
    import extendedEuclid
except:
    from . import primes
    from . import extendedEuclid

def break_rsa(n, e=None):
    a=ceil(sqrt(n))
    test=100
    for i in range(test):
        b2=a*a-n
        b=ceil(sqrt(b2))
        if b*b==b2:
            break
        a+=1
    p=a+b
    q=a-b

    #can check if p and q are primes:
    # print(primes.test_prime(p))
    # print(primes.test_prime(q))

    phi=(p-1)*(q-1)
    if e is None:
        return p, q, phi
    d=extendedEuclid.extendedEuclid(e,phi)
    return p, q, phi, d


if __name__=='__main__':
    p=108037
    q=106441
    n=p*q
    print(n)
    print(break_rsa(n))
