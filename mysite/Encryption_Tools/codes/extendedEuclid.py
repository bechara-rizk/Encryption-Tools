

def extendedEuclid(inverse, mod):
    A=(1,0,mod)
    B=(0,1,inverse%mod)
    while True:
        if B[2]==0:
            return 'no inverse'
        if B[2]==1:
            return B[1]
        Q=A[2]//B[2]
        C=((A[0]-Q*B[0])%mod,(A[1]-Q*B[1])%mod,(A[2]-Q*B[2])%mod)
        A=B
        B=C

if __name__=='__main__':
    print(extendedEuclid(983,19019))
    print(extendedEuclid(984,19019))
    print(extendedEuclid(985,19019))
    print(extendedEuclid(986,19019))
    print(extendedEuclid(987,19019))
    print(extendedEuclid(988,19019))
    print(extendedEuclid(989,19019))
    print(extendedEuclid(990,19019))