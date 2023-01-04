file =open("mysite/Encryption_Tools/codes/primes.txt","r")
    prime=[]
    x=file.read()
    for i in x.split(","):
        try:
            prime.append(int(i))
        except:
            pass
    file.close()