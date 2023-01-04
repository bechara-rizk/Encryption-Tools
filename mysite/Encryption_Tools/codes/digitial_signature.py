from primes import test_prime, primitive_root_test, rel_prime
from random import randint
from exponentiation import exponentiation
from extendedEuclid import extendedEuclid
from ecc import ECCPrime

def elgamal_ds_setup(q,a,m,xA=None,k=None):
    if not test_prime(q):
        return False
    if not primitive_root_test(q,a):
        return False
    if (k is not None) and (not rel_prime(k,q-1)):
        return False
    if xA is None:
        xA=randint(2,q-2)
    yA=exponentiation(a,xA,q)
    while (k is None) or (not rel_prime(k,q-1)):
        k=randint(1,q-1)
    S1=exponentiation(a,k,q)
    invK=extendedEuclid(k,q-1)
    S2=(invK*(m-xA*S1))%(q-1)
    return (yA,S1,S2)

def elgamal_ds_verify(q,a,m,yA,S):
    V1=exponentiation(a,m,q)
    V2=((yA**S[0])*(S[0]**S[1]))%q
    return V1==V2

def ECDSA_setup(curve,G,e,d=None,k=None):
    if G not in curve.all_points():
        return 'G is not a point on the curve'
    search = 1000
    for i in range(1, search+1):
        if curve.mul(i, G) == ('inf', 'inf'):
            order = i
            break
        order = search
    if d is None: d=randint(1,order-1)
    Q=curve.mul(d,G)
    #private key d, public key Q
    r=0
    while r==0:
        if k is None or (not rel_prime(k,order)): k=randint(1,order-1)
        P=curve.mul(k,G)
        r=P[0]%order
        t=extendedEuclid(k,order)
        if r==0 or t=='no inverse':
            k = randint(1, order-1)
            r=0 #force loop re-entry 
    s=(t*(e+d*r))%order
    if extendedEuclid(s,order)=='no inverse':
        return ECDSA_setup(curve,G,e,d,k)
    return Q, r, s, order,d,k

def ECDSA_verify(curve,G,Q,e,r,s,n):
    w=extendedEuclid(s,n)
    u1=e*w
    u2=r*w
    X=curve.add(curve.mul(u1,G),curve.mul(u2,Q))
    v=X[0]%n
    return v==r


if __name__=='__main__':
    yA,S1,S2=elgamal_ds_setup(19,10,14)
    print(yA,S1,S2)
    print(elgamal_ds_verify(19,10,14,yA,(S1,S2)))
    curve=ECCPrime(2,1,113)
    # print(curve.all_points())
    G = (34, 106)
    e=21
    Q, r, s, n,d,k = ECDSA_setup(curve, G, e)
    print(Q,r,s,n)
    print(ECDSA_verify(curve,G,Q,e,r,s,n))
    