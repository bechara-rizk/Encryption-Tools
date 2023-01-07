

def exponentiation(base, exponent, mod):
    exponent=bin(exponent)[2:]
    result=1
    for i in exponent:
        result=(result*result)%mod
        if i=='1':
            result=(result*base)%mod
    return result


if __name__=='__main__':
    print(exponentiation(983,19271893,19019))
    print(exponentiation(984,19271893,19019))
    print(exponentiation(985,19271893,19019))
    print(exponentiation(986,19271893,19019))
    print(exponentiation(987,19271893,19019))
    print(exponentiation(988,19271893,19019))
    print(exponentiation(989,19271893,19019))
    print(exponentiation(990,19271893,19019))
    print(exponentiation(3,3786278,32))