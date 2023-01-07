


class GF:
    def __init__(self, p, n=None, m=None):
        self.p = p
        self.n = n
        self.m = m

    def __remove_leading_zeros(self, a):
        a=bin(int(a, 2))[2:]
        return a

    def add(self, a, b):
        #take strings input and add them using mod self.p
        a=self.__remove_leading_zeros(a)
        b=self.__remove_leading_zeros(b)
        #first let a be the longer string
        if len(a) < len(b):
            a, b = b, a
        difference = len(a) - len(b)
        b = '0' * difference + b
        result=''
        for i in range(len(a)):
            result += str((int(a[i]) + int(b[i])) % self.p)
        return result

    def sub(self, a, b):
        #take strings input and subtract them using mod self.p
        a=self.__remove_leading_zeros(a)
        b=self.__remove_leading_zeros(b)
        #first let a be the longer string
        if len(a) < len(b):
            a, b = b, a
        difference = len(a) - len(b)
        b = '0' * difference + b
        result=''
        for i in range(len(a)):
            result += str((int(a[i]) - int(b[i])) % self.p)
        return result

    def mul2(self, a, b):
        #take strings input and multiply them using mod self.p
        a=self.__remove_leading_zeros(a)
        b=self.__remove_leading_zeros(b)
        #first let a be the longer string
        if len(a) < len(b):
            a, b = b, a

        result='0'
        for i in range(len(b)-1,-1,-1):
            if b[i]=='1':
                result = self.add(result, a)
            a = a + '0'

        return result

    def mul(self, a, b):
        #take strings input and multiply them using mod self.p
        a=self.__remove_leading_zeros(a)
        b=self.__remove_leading_zeros(b)
        #first let a be the longer string
        if len(a) < len(b):
            a, b = b, a
        result='0'
        if self.m is None:
            for i in range(len(b)-1,-1,-1):
                if b[i]=='1':
                    result = self.add(result, a)
                a = a + '0'
        else:
            multiplication=self.mul2(a, b)
            result=self.div(multiplication, self.m)[1]
        
        return result

    # def mul3(self, a, b):
    #     #take strings input and multiply them using mod self.p
    #     a=self.__remove_leading_zeros(a)
    #     b=self.__remove_leading_zeros(b)
    #     #first let a be the longer string
    #     if len(a) < len(b):
    #         a, b = b, a

    #     result='0'
    #     if self.m is None:
    #         for i in range(len(b)-1,-1,-1):
    #             if b[i]=='1':
    #                 result = self.add(result, a)
    #             a = a + '0'
    #     else:
    #         results=dict()
    #         results[0]=a
    #         for i in range(1,len(b)):
    #             if results[i-1][0]=='0' or len(results[i-1])<self.n:
    #                 results[i]=results[i-1]+'0'
    #             else:
    #                 results[i]=self.__remove_leading_zeros(self.add(results[i-1]+'0', self.m))
    #         for i in range(len(b)):
    #             if b[-1-i]=='1':
    #                 result=self.add(result, results[i])

    #     return result

    def div(self, a, b):
        #take strings input and divide them using mod self.p
        a=self.__remove_leading_zeros(a)
        b=self.__remove_leading_zeros(b)
        difference = len(a) - len(b)
        result='0'
        while difference >= 0:
            x='1'+'0'*difference
            result=self.add(result, x)
            x=self.mul2(x, b)
            a=self.sub(a, x)
            a=self.__remove_leading_zeros(a)
            difference = len(a) - len(b)
        remainder=a
        return result, remainder

    def inv(self, a):
        if self.m is None:
            return 'm(x) is not defined'
        A2='0'
        A3=self.m
        B2='1'
        B3=a
        while B3!='0' and B3!='1':
            Q, R=self.div(A3, B3)
            A2, A3, B2, B3 = B2, B3, self.sub(A2, self.mul2(Q, B2)), R
        if B3=='0':
            return 'no inverse'
        else:
            return B2
        

if __name__=='__main__':
    gf = GF(2, 8, '100011011')
    a='01010111'
    b='10000011'
    print(gf.add(a, b))
    print(gf.mul(a, b))
    print(gf.inv(a))
    print(gf.mul(a,gf.inv(a)))
    gf2=GF(2, 3, '1011')
    a='110'
    b='100'
    print(gf2.mul(a, b))
    print(gf2.inv(b))