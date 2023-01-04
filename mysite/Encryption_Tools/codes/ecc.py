from extendedEuclid import extendedEuclid
from random import randint, random

class ECCPrime:
    def __init__(self, a, b, p):
        self.a=a
        self.b=b
        self.p=p
        self.O=('inf','inf')
        self.points=None
    
    def all_points(self):
        if self.points is not None:
            return self.points
        self.points=[]
        for x in range(self.p):
            temp=(x*x*x+x*self.a+self.b)%self.p
            if temp==0:
                self.points.append((x,temp))
            else:
                for y in range(self.p):
                    if (y*y)%self.p==temp:
                        self.points.append((x,y))
                        self.points.append((x,self.p-y))
                        break
        self.points.append(self.O)
        return self.points

    def add(self,P,Q):
        if P==self.O:
            return Q
        if Q==self.O:
            return P
        if P[0]==Q[0]:
            if (P[1]+Q[1])%self.p==0:
                return self.O
            else:
                inv=extendedEuclid(2*P[1],self.p)
                lam=((3*P[0]*P[0]+self.a)*inv)%self.p
        else:
            inv=extendedEuclid(Q[0]-P[0],self.p)
            lam=((Q[1]-P[1])*inv)%self.p
        x=(lam*lam-P[0]-Q[0])%self.p
        y=(lam*(P[0]-x)-P[1])%self.p
        return (x,y)

    def mul(self,n,P):
        if n==0:
            return self.O
        if n==1:
            return P
        if n%2==0:
            return self.mul(n//2,self.add(P,P))
        else:
            return self.add(P,self.mul(n-1,P))

    def sub(self,P,Q):
        return self.add(P,(Q[0],(-Q[1])%self.p))

def ECC_DH_setup(curve, G, nA=None, nB=None):
    if G not in curve.all_points():
        return 'G is not a point on the curve'
    search=300
    for i in range(1,search+1):
        if curve.mul(i,G)==('inf','inf'):
            order=i
            break
        order=search

    if nA is None:
        nA=randint(1,order-1)
    if nB is None:
        nB=randint(1,order-1)
    PA=curve.mul(nA,G)
    PB=curve.mul(nB,G)
    K=curve.mul(nA,PB)
    return (nA,nB,PA,PB,K)

def ECC_DH_encrypt(curve, G, Pm, P, k=None):
    if G not in curve.all_points():
        return 'G is not a point on the curve'
    if k is None:
        k=int(random()*randint(100,10000))
    Cm=(curve.mul(k,G),curve.add(Pm,curve.mul(k,P)))
    return Cm

def ECC_DH_decrypt(curve, n, Cm):
    Pm=curve.sub(Cm[1],curve.mul(n,Cm[0]))
    return Pm


if __name__=='__main__':
    curve=ECCPrime(2,3,67)
    G=(2,22)
    print(len(curve.all_points()))
    print(ECC_DH_setup(curve,G, 121, 4))
    print(ECC_DH_encrypt(curve, G, (24,26), (13,45)))
    print(ECC_DH_decrypt(curve, 4, ((13, 22), (55, 44))))
