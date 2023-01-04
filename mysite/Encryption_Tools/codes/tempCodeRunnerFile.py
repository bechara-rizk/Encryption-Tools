 a is None: a=random.randint(2,n-2)
        if exponentiation(a,q,n) == 1:
            return True
        for i in range(k):
            if exponentiation(a,2**i*q,n) == n-1:
                return True