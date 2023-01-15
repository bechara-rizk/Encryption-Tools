from django.shortcuts import render
from .codes import texthex, extendedEuclid, exponentiation, gallois_fields
from .codes.ciphers import caesar_cipher, affine_cipher, hill_cipher, playfair_cipher, viginere_cipher, monoalphabetic_cipher, rail_fence_cipher, row_transposition_cipher
from .codes import aes, des, block_operations, digitial_signature
from .codes.ecc import ECCPrime, ECC_DH, ECC_decrypt, ECC_encrypt
from .codes import asymetric_encryption
from .codes import primes
from .codes import break_rsa
# from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def break_rsa_func(request):
    if request.method=="POST":
        if request.POST.get('break'):
            n=int(request.POST.get('n'))
            e=request.POST.get('e')
            if e=='':
                ei=None
                p,q,phi=break_rsa.break_rsa(n)
                return render(request, 'break_rsa.html', {'previousn':n,'previouse':e,'p':p,'q':q,'phi':phi})
            else:
                ei=int(e)
                p,q,phi,d=break_rsa.break_rsa(n,ei)
                return render(request, 'break_rsa.html', {'previousn':n,'previouse':e,'p':p,'q':q,'phi':phi,'d':d})
    return render(request, 'break_rsa.html')

def enc_text(request):
    if request.method=='POST':
        text=request.POST.get('text')
        key=request.POST.get('key')
        hex_key=texthex.text_to_hex(key)
        hex_key=hex_key.zfill(64)
        if len(hex_key)>64:
            hex_key=hex_key[:64]
        if request.POST.get('enc'):
            hex_text=texthex.text_to_hex(text)
            result=block_operations.operation('aes', 'ecb', hex_key, hex_text, 'encrypt')
        elif request.POST.get('dec'):
            result=block_operations.operation('aes', 'ecb', hex_key, text, 'decrypt')
            result=texthex.hex_to_text(result)
        return render(request, 'enc_text.html', {'previouskey':key,'previoustext':text,'result':result})
    return render(request, 'enc_text.html')

def dl(request):
    if request.method=='POST':
        if request.POST.get('compute'):
            base=int(request.POST.get('base'))
            mod=int(request.POST.get('mod'))
            table=primes.disc_log_table(base,mod)
            return render(request, 'dl.html', {'previousbase':base,'previousmod':mod,'result':table})
    return render(request, 'dl.html')

def pr(request):
    if request.method=='POST':
        if request.POST.get('compute'):
            n=int(request.POST.get('n'))
            result=primes.primitive_roots(n)
            return render(request, 'pr.html', {'previousn':n,'result':result})
    return render(request, 'pr.html', {'length':'auto auto auto'})

def crt(request):
    if request.method=='POST':
        if request.POST.get('compute'):
            m=request.POST.get('m')
            mi=m.split(',')
            for i in range(len(mi)):
                mi[i]=int(mi[i])
            print(mi)
            a=request.POST.get('a')
            if ',' in a:
                ai=a.split(',')
                for i in range(len(ai)):
                    ai[i]=int(ai[i])
            else:
                ai=int(a)
            result=primes.CRT(mi,ai)
            return render(request, 'crt.html', {'result':result,'previousm':m,'previousa':a})
    return render(request, 'crt.html')

def mr(request):
    if request.method=='POST':
        if request.POST.get('test'):
            n=int(request.POST.get('n'))
            rounds=request.POST.get('rounds')
            if rounds!='':
                rounds=int(rounds)
            else:
                rounds=1
            a=request.POST.get('base')
            if a!='':
                ai=int(a)
            else:
                ai=None
            result=primes.miller_rabbin(n, rounds, ai)
            if result:
                result=f'Maybe prime with probability {1-4**(-rounds)}'
            else:
                result='Not prime'
            return render(request, 'mr.html', {'previousn':n,'previousrounds':rounds,'previousbase':a,'result':result})
    return render(request, 'mr.html')

def etf(request):
    if request.method=='POST':
        if request.POST.get('compute'):
            n=int(request.POST.get('n'))
            result=primes.totient(n)
            return render(request, 'etf.html', {'previousn':n, 'result':result})
    return render(request, 'etf.html')

def rpt(request):
    if request.method=='POST':
        if request.POST.get('test'):
            a=int(request.POST.get('a'))
            b=int(request.POST.get('b'))
            result=primes.rel_prime(a,b)
            return render(request, 'rpt.html', {'previousa':a, 'previousb':b, 'result':str(result)})
    return render(request, 'rpt.html')

def ecc(request):
    if request.method=='POST':
        a=request.POST.get('a')
        a=int(a)
        b=request.POST.get('b')
        b=int(b)
        p=request.POST.get('p')
        p=int(p)
        curve=ECCPrime(a,b,p)
        if request.POST.get('enc'):
            gx=int(request.POST.get('gx'))
            gy=int(request.POST.get('gy'))
            G=(gx,gy)
            px=int(request.POST.get('px'))
            py=int(request.POST.get('py'))
            P=(px,py)
            pmx=int(request.POST.get('pmx'))
            pmy=int(request.POST.get('pmy'))
            Pm=(pmx,pmy)
            Cm=ECC_encrypt(curve, G, Pm, P)
            return render(request, 'ecc.html', {'previousa':a,'previousb':b,'previousp':p,'previousgx':gx,'previousgy':gy,'previouspx':px,'previouspy':py,'previouspmx':pmx,'previouspmy':pmy,'previouscm1x':Cm[0][0],'previouscm1y':Cm[0][1],'previouscm2x':Cm[1][0],'previouscm2y':Cm[1][1]})
        if request.POST.get('dec'):
            n=int(request.POST.get('n'))
            cm1x=int(request.POST.get('cm1x'))
            cm1y=int(request.POST.get('cm1y'))
            cm2x=int(request.POST.get('cm2x'))
            cm2y=int(request.POST.get('cm2y'))
            Cm=((cm1x,cm1y),(cm2x,cm2y))
            Pm=ECC_decrypt(curve, n, Cm)
            return render(request, 'ecc.html', {'previousa':a,'previousb':b,'previousp':p,'previouspmx':Pm[0],'previouspmy':Pm[1],'previouscm1x':Cm[0][0],'previouscm1y':Cm[0][1],'previouscm2x':Cm[1][0],'previouscm2y':Cm[1][1], 'previousn':n})
    return render(request, 'ecc.html')

def ecdh(request):
    if request.method=='POST':
        if request.POST.get('setup'):
            a=request.POST.get('a')
            a=int(a)
            b=request.POST.get('b')
            b=int(b)
            p=request.POST.get('p')
            p=int(p)
            curve=ECCPrime(a,b,p)
            gx=request.POST.get('gx')
            gx=int(gx)
            gy=request.POST.get('gy')
            gy=int(gy)
            na=request.POST.get('na')
            nb=request.POST.get('nb')
            if na!='':
                nai=int(na)
            else:
                nai=None
            if nb!='':
                nbi=int(nb)
            else:
                nbi=None
            na,nb,PA,PB,K=ECC_DH(curve,(gx,gy),nai,nbi)
            return render(request, 'ecdh.html', {'previousa':a,'previousb':b,'previousp':p,'previousgx':gx,'previousgy':gy,'previousna':na,'previousnb':nb,'previouspa':PA,'previouspb':PB,'previousk':K})
    return render(request, 'ecdh.html')

def eco(request):
    if request.method=='POST':
        a=request.POST.get('a')
        a=int(a)
        b=request.POST.get('b')
        b=int(b)
        p=request.POST.get('p')
        p=int(p)
        px=request.POST.get('px')
        py=request.POST.get('py')
        qx=request.POST.get('qx')
        qy=request.POST.get('qy')
        n=request.POST.get('n')
        curve=ECCPrime(a,b,p)
        resultpoints=''
        result=''
        if request.POST.get('show'):
            resultpoints=curve.all_points()
        elif request.POST.get('add'):
            P=(int(px),int(py))
            Q=(int(qx),int(qy))
            result=curve.add(P,Q)
            result=f'({px},{py}) + ({qx},{qy}) = {result}'
        elif request.POST.get('mul'):
            P=(int(px),int(py))
            result=curve.mul(int(n),P)
            result=f'{n} * ({px},{py}) = {result}'
        return render(request, "eco.html", {'result':result,'resultpoints':resultpoints,'previousa':a,'previousb':b,'previousp':p,'previouspx':px,'previouspy':py,'previousqx':qx,'previousqy':qy,'previousn':n})
    return render(request, 'eco.html')

def elgamal(request):
    if request.method=='POST':
        q=request.POST.get('q')
        q=int(q)
        a=request.POST.get('a')
        xa=request.POST.get('xa')
        ya=request.POST.get('ya')
        m=request.POST.get('m')
        c1=request.POST.get('c1')
        c2=request.POST.get('c2')
        if request.POST.get('setup'):
            if a!='':
                ai=int(a)
            else:
                ai=None
            if xa!='':
                xai=int(xa)
            else:
                xai=None
            q,a,xa,ya=asymetric_encryption.el_gamal_setup(q, ai, xai)
            return render(request, 'elgamal.html', {'previousq':q,'previousa':a,'previousxa':xa,'previousya':ya, 'previousm':m, 'previousc1':c1, 'previousc2':c2})
        elif request.POST.get('enc'):
            a=int(a)
            ya=int(ya)
            m=int(m)
            c1,c2=asymetric_encryption.el_gamal_encrypt(m,q,a,ya)
            return render(request, 'elgamal.html', {'previousq':q,'previousa':a,'previousxa':xa,'previousya':ya, 'previousm':m, 'previousc1':c1, 'previousc2':c2})
        elif request.POST.get('dec'):
            xa=int(xa)
            c1=int(c1)
            c2=int(c2)
            m=asymetric_encryption.el_gamal_decrypt(c1,c2,q,xa)
            return render(request, 'elgamal.html', {'previousq':q,'previousa':a,'previousxa':xa,'previousya':ya, 'previousm':m, 'previousc1':c1, 'previousc2':c2})
    return render(request, 'elgamal.html')

def dh(request):
    if request.method=="POST" and request.POST.get('setup'):
        q=request.POST.get('q')
        q=int(q)
        a=request.POST.get('a')
        if a!='':
            ai=int(a)
        else:
            ai=None
        xa=request.POST.get('xa')
        if xa!='':
            xai=int(xa)
        else:
            xai=None
        xb=request.POST.get('xb')
        if xb!='':
            xbi=int(xb)
        else:
            xbi=None
        a,xa,xb,ya,yb,key=asymetric_encryption.DH_key_exchange(q,ai,xai,xbi)
        return render(request, 'dh.html', {'previousq': q,'previousa': a,'previousxa': xa,'previousxb': xb,'previousya': ya,'previousyb': yb,'previouskey': key})
    return render(request, 'dh.html')

def rsa(request):
    if request.method=="POST":
        p=request.POST.get("p")
        p=int(p)
        q=request.POST.get("q")
        q=int(q)
        e=request.POST.get("e")
        n=request.POST.get("n")
        phi=request.POST.get("phi")
        d=request.POST.get("d")
        m=request.POST.get("m")
        c=request.POST.get("c")
        if request.POST.get("setup"):
            if e !='':
                ei=int(e)
            else:
                ei=None
            n,phi,e,d=asymetric_encryption.RSA_setup(p, q, ei)
            return render(request, 'rsa.html', {"previousp":p, "previousq":q, "previouse":e, "previousm":m, "previousn":n, "previousphi":phi, "previousd":d, "previousc":c})
        elif request.POST.get("enc"):
            m=int(m)
            e=int(e)
            n=int(n)
            result=asymetric_encryption.RSA_encrypt(m, e, n)
            return render(request, 'rsa.html', {"previousp":p, "previousq":q, "previouse":e, "previousm":m, "previousn":n, "previousphi":phi, "previousd":d, "previousc":result})
        elif request.POST.get("dec"):
            c=int(c)
            d=int(d)
            n=int(n)
            result=asymetric_encryption.RSA_encrypt(c, d, n)
            return render(request, 'rsa.html', {"previousp":p, "previousq":q, "previouse":e, "previousm":result, "previousn":n, "previousphi":phi, "previousd":d, "previousc":c})
    return render(request, 'rsa.html')

def ecdsa(request):
    if request.method=="POST":
        a=request.POST.get("a")
        a=int(a)
        b=request.POST.get("b")
        b=int(b)
        p=request.POST.get("p")
        p=int(p)
        gx=request.POST.get("gx")
        gx=int(gx)
        gy=request.POST.get("gy")
        gy=int(gy)
        e=request.POST.get("e")
        e=int(e)
        d=request.POST.get("d")
        k=request.POST.get('k')
        curve=ECCPrime(a, b, p)
        G=(gx, gy)
        if request.POST.get("setup"):
            if d!='':
                di=int(d)
            else:
                di=None
            if k!='':
                ki=int(k)
            else:
                ki=None
            result=digitial_signature.ECDSA_setup(curve, G, e, di, ki)
            return render(request, 'ecdsa.html', {"previousa":a, "previousb":b, "previousp":p, "previousgx":gx, "previousgy":gy, "previouse":e, "previousd":result[4], "previousk":result[5], 'previousqx':result[0][0], 'previousqy':result[0][1], 'previousr':result[1], 'previouss':result[2], 'previousorder':result[3]})
        elif request.POST.get("verify"):
            qx=request.POST.get("qx")
            qx=int(qx)
            qy=request.POST.get("qy")
            qy=int(qy)
            r=request.POST.get("r")
            r=int(r)
            s=request.POST.get("s")
            s=int(s)
            n=request.POST.get("order")
            n=int(n)
            result=digitial_signature.ECDSA_verify(curve, G, (qx, qy), e, r, s, n)
            return render(request, 'ecdsa.html', {"text":result, "previousa":a, "previousb":b, "previousp":p, "previousgx":gx, "previousgy":gy, "previouse":e, "previousd":d, "previousk":k, 'previousqx':qx, 'previousqy':qy, 'previousr':r, 'previouss':s, 'previousorder':n})
    return render(request, 'ecdsa.html')

def ds_eg(request):
    if request.method=="POST":
        q=request.POST.get("q")
        q=int(q)
        a=request.POST.get("a")
        a=int(a)
        m=request.POST.get("m")
        m=int(m)
        k=request.POST.get("k")
        xA=request.POST.get("xa")
        if request.POST.get("setup"):
            if k!='': 
                ki=int(k)
            else:
                ki=None
            if xA!='':
                xAi=int(xA)
            else:
                xAi=None
            result=digitial_signature.elgamal_ds_setup(q, a, m, xAi, ki)
            return render(request, 'ds_eg.html', {"previousq":q, "previousa":a, "previousm":m, "previousxa":result[0], "previousk":result[1], "previousya":result[2], "previouss1":result[3], "previouss2":result[4]})
        elif request.POST.get("verify"):
            yA=request.POST.get("ya")
            yA=int(yA)
            s1=request.POST.get("s1")
            s1=int(s1)
            s2=request.POST.get("s2")
            s2=int(s2)
            result=digitial_signature.elgamal_ds_verify(q, a, m, yA, (s1, s2))
            return render(request, 'ds_eg.html', {"text":result, "previousq":q, "previousa":a, "previousm":m, "previousxa":xA, "previousk":k, "previousya":yA, "previouss1":s1, "previouss2":s2})
        else:
            result=''
    return render(request, 'ds_eg.html')

def ofb_func(request):
    if request.method=="POST":
        text=request.POST.get("text")
        key=request.POST.get("key")
        nonce=request.POST.get("nonce")
        if request.POST.get("aenc"):
            if nonce:
                result=block_operations.operation('aes', 'ofb', key, text, 'encrypt', nonce)
            else:
                result=block_operations.operation('aes', 'ofb', key, text, 'encrypt')
        elif request.POST.get("adec"):
            if nonce:
                result=block_operations.operation('aes', 'ofb', key, text, 'decrypt', nonce)
            else:
                result='Please enter IV'
        elif request.POST.get("denc"):
            if nonce:
                result=block_operations.operation('des', 'ofb', key, text, 'encrypt',nonce)
            else:
                result=block_operations.operation('des', 'ofb', key, text, 'encrypt')
        elif request.POST.get("ddec"):
            if nonce:
                result=block_operations.operation('des', 'ofb', key, text, 'decrypt', nonce)
            else:
                result='Please enter IV'
        else:
            result='error'
        return render(request, 'ofb.html', {"text":result, "previouskey":request.POST.get("key"), "previoustext":request.POST.get("text"), "previousnonce":request.POST.get("nonce")})
    return render(request, 'ofb.html')

def cbc_func(request):
    if request.method=="POST":
        text=request.POST.get("text")
        key=request.POST.get("key")
        iv=request.POST.get("iv")
        if request.POST.get("aenc"):
            if iv:
                result=block_operations.operation('aes', 'cbc', key, text, 'encrypt', iv)
            else:
                result=block_operations.operation('aes', 'cbc', key, text, 'encrypt')
        elif request.POST.get("adec"):
            if iv:
                result=block_operations.operation('aes', 'cbc', key, text, 'decrypt', iv)
            else:
                result='Please enter IV'
        elif request.POST.get("denc"):
            if iv:
                result=block_operations.operation('des', 'cbc', key, text, 'encrypt',iv)
            else:
                result=block_operations.operation('des', 'cbc', key, text, 'encrypt')
        elif request.POST.get("ddec"):
            if iv:
                result=block_operations.operation('des', 'cbc', key, text, 'decrypt', iv)
            else:
                result='Please enter IV'
        else:
            result='error'
        return render(request, 'cbc.html', {"text":result, "previouskey":request.POST.get("key"), "previoustext":request.POST.get("text"), "previousiv":request.POST.get("iv")})
    return render(request, 'cbc.html')

def ecb_func(request):
    if request.method=="POST":
        text=request.POST.get("text")
        key=request.POST.get("key")
        if request.POST.get("aenc"):
            result=block_operations.operation('aes', 'ecb', key, text, 'encrypt')
        elif request.POST.get("adec"):
            result=block_operations.operation('aes', 'ecb', key, text, 'decrypt')
        elif request.POST.get("denc"):
            result=block_operations.operation('des', 'ecb', key, text, 'encrypt')
        elif request.POST.get("ddec"):
            result=block_operations.operation('des', 'ecb', key, text, 'decrypt')
        else:
            result='error'
        return render(request, 'ecb.html', {"text":result, "previouskey":request.POST.get("key"), "previoustext":request.POST.get("text")})
    return render(request, 'ecb.html')

def aes_func(request):
    clicked=''
    AES=aes.AES
    if request.method=="POST":
        if request.POST.get("show"):
            clicked='checked'
            a=AES(request.POST.get("key"), True, True)
            if request.POST.get("encrypt"):
                text,key=a.encrypt(request.POST.get("text"))
            else:
                # print(request.POST.get("decrypt"))
                text,key=a.decrypt(request.POST.get("text"))
        else: 
            clicked=''
            a=AES(request.POST.get("key"), True, False)
            if request.POST.get("encrypt"):
                text,key=a.encrypt(request.POST.get("text")),''
            else:
                # print(request.POST.get("decrypt"))
                text,key=a.decrypt(request.POST.get("text")),''
        return render(request, 'aes.html', {"text":text, 'key':key, "clicked":clicked, "previouskey":request.POST.get("key"), "previoustext":request.POST.get("text")})
    return render(request, 'aes.html', {"text":"", 'key':'', "clicked":clicked, "previouskey":'0f1571c947d9e8590cb7add6af7f6798', "previoustext":'ff0b844a0853bf7c6934ab4364148fb9'})

def des_func(request):
    clicked=''
    DES=des.DES
    if request.method=="POST":
        if request.POST.get("show"):
            clicked='checked'
            a=DES(request.POST.get("key"), True)
            if request.POST.get("encrypt"):
                text,key=a.encrypt(request.POST.get("text"))
            else:
                # print(request.POST.get("decrypt"))
                text,key=a.decrypt(request.POST.get("text"))
        else: 
            clicked=''
            a=DES(request.POST.get("key"), False)
            if request.POST.get("encrypt"):
                text,key=a.encrypt(request.POST.get("text")),''
                text="Encrypted Text: "+text
            else:
                # print(request.POST.get("decrypt"))
                text,key=a.decrypt(request.POST.get("text")),''
                text="Decrypted Text: "+text
        return render(request, 'des.html', {"text":text, 'key':key, "clicked":clicked, "previouskey":request.POST.get("key"), "previoustext":request.POST.get("text")})
    return render(request, 'des.html', {"text":"", 'key':'', "clicked":clicked, "previouskey":'0f1571c947d9e859', "previoustext":'02468aceeca86420'})

def text_hex(request):
    clicked=''
    if request.method=='POST':
        if request.POST.get('convert'):
            # print('hi', request.POST)
            text=request.POST.get('text')
            clicked=text
            text=texthex.text_to_hex(text)
            # print(text)
        elif request.POST.get('revert'):
            text=request.POST.get('text')
            clicked=text
            text=texthex.hex_to_text(text)
        else:
            text='error'
        return render(request, 'text_hex.html', {'result':text, 'previous':clicked})
    return render(request, 'text_hex.html',{'previous':clicked, 'result':''})

def mod_inv(request):
    clicked=''
    if request.method=='POST':
        if request.POST.get('invert'):
            # print('hi', request.POST)
            nb=request.POST.get('nb')
            mod=request.POST.get('mod')
            try:
                result=extendedEuclid.extendedEuclid(int(nb), int(mod))
            except:
                result='error'
            # print(text)
        else:
            result='error'
        return render(request, 'mod_inv.html', {'result':result, 'previous':clicked, 'previousmod':mod, 'previousnb':nb})
    return render(request, 'mod_inv.html',{'previousnb':'', 'previousmod':'', 'result':''})

def exponentiation_func(request):
    if request.method=='POST':
        if request.POST.get('exponentiate'):
            # print('hi', request.POST)
            base=request.POST.get('base')
            exponent=request.POST.get('exponent')
            mod=request.POST.get('mod')

            try:
                result=exponentiation.exponentiation(int(base), int(exponent), int(mod))
            except:
                result='error'
            # print(text)
        else:
            result='error'
        if result==0:
            result='0'
        return render(request, 'exponentiation.html', {'result':result, 'previousmod':mod, 'previousexponent':exponent, 'previousbase':base})
    return render(request, 'exponentiation.html',{'previousbase':'', 'previousexponent':'', 'previousmod':'', 'result':''})

def gfo(request):
    if request.method=='POST':
        p=request.POST.get('p')
        if p:
            p=int(p)
        else:
            result='error'
        n=request.POST.get('n')
        a=request.POST.get('a')
        if not a:
            result='error'
        b=request.POST.get('b')
        if not b:
            b=None
        m=request.POST.get('mod')
        if n:
            gf=gallois_fields.GF(p, int(n), m)
        else:
            gf=gallois_fields.GF(p)
        if request.POST.get('add'):
            # print('add')
            result=gf.add(a, b)
            result=a+' + '+b+' = '+result
        elif request.POST.get('sub'):
            # print('subtract')
            result=gf.sub(a, b)
            result=a+' - '+b+' = '+result
        elif request.POST.get('mul'):
            # print('multiply')
            result=gf.mul(a, b)
            result=a+' * '+b+' = '+result
        elif request.POST.get('div'):
            # print('divide')
            result=gf.div(a, b)
            result=a+' / '+b+' = '+result[0]+' with remainder '+result[1]
        elif request.POST.get('inv'):
            # print('inverse')
            result=gf.inv(a)
            result=a+"^-1 mod "+m+" = "+result
        else:
            # print('error')
            result='error'
        return render(request, 'gfo.html', {'result':result, 'previousp':p, 'previousn':n, 'previousa':a, 'previousb':b, 'previousmod':m})
    return render(request, 'gfo.html')

def cipher_caesar(request):
    if request.method=='POST':
        text=request.POST.get('text')
        key=request.POST.get('key')
        if request.POST.get('enc'):
            result=caesar_cipher.caesar_cipher_enc(text, int(key))
        elif request.POST.get('dec'):
            result=caesar_cipher.caesar_cipher_dec(text, int(key))
        else:
            result='error'
        return render(request, 'cipher_caesar.html', {'result':result, 'previoustext':text, 'previouskey':key})
    return render(request, 'cipher_caesar.html', {'previoustext':'', 'previouskey':'', 'result':''})

def cipher_affine(request):
    if request.method=='POST':
        text=request.POST.get('text')
        a=request.POST.get('a')
        b=request.POST.get('b')
        if request.POST.get('enc'):
            result=affine_cipher.affine_cipher_enc(text, int(a), int(b))
        elif request.POST.get('dec'):
            result=affine_cipher.affine_cipher_dec(text, int(a), int(b))
        else:
            result='error'
        return render(request, 'cipher_affine.html', {'result':result, 'previoustext':text, 'previousa':a, 'previousb':b})
    return render(request, 'cipher_affine.html', {'previoustext':'', 'previousa':'', 'previousb':'', 'result':''})

def cipher_hill(request):
    if request.method=='POST':
        text=request.POST.get('text')
        key=[]
        # print(request.POST)
        a=request.POST.get('a')
        b=request.POST.get('b')
        c=request.POST.get('c')
        d=request.POST.get('d')
        e=request.POST.get('e')
        f=request.POST.get('f')
        g=request.POST.get('g')
        h=request.POST.get('h')
        i=request.POST.get('i')
        if c:
            key.append([int(a), int(b), int(c)])
            key.append([int(d), int(e), int(f)])
            key.append([int(g), int(h), int(i)])
        else:
            key.append([int(a), int(b)])
            key.append([int(d), int(e)])

        if request.POST.get('enc'):
            if len(key)==2:
                result=hill_cipher.hill_cipher_2_enc(text, key)
            elif len(key)==3:
                result=hill_cipher.hill_cipher_3_enc(text, key)
            else:
                result='error'
        elif request.POST.get('dec'):
            if len(key)==2:
                result=hill_cipher.hill_cipher_2_dec(text, key)
            elif len(key)==3:
                result=hill_cipher.hill_cipher_3_dec(text, key)
            else:
                result='error'
        else:
            result='error'
        return render(request, 'cipher_hill.html', {'result':result, 'previoustext':text, 'previousa':a, 'previousb':b, 'previousc':c, 'previousd':d, 'previouse':e, 'previousf':f, 'previousg':g, 'previoush':h, 'previousi':i})
    return render(request, 'cipher_hill.html', {'previoustext':'', 'previousa':'', 'previousb':'', 'previousc':'', 'previousd':'', 'previouse':'', 'previousf':'', 'previousg':'', 'previoush':'', 'previousi':'', 'result':''})

def cipher_playfair(request):
    if request.method=='POST':
        text=request.POST.get('text')
        key=request.POST.get('key')
        if request.POST.get('enc'):
            result=playfair_cipher.playfair_cipher_enc(text, key)
        elif request.POST.get('dec'):
            result=playfair_cipher.playfair_cipher_dec(text, key)
        else:
            result='error'
        return render(request, 'cipher_playfair.html', {'result':result, 'previoustext':text, 'previouskey':key})
    return render(request, 'cipher_playfair.html')

def cipher_viginere(request):
    if request.method=='POST':
        text=request.POST.get('text')
        key=request.POST.get('key')
        if request.POST.get('enc'):
            result=viginere_cipher.viginere_cipher_enc(text, key)
        elif request.POST.get('dec'):
            result=viginere_cipher.viginere_cipher_dec(text, key)
        else:
            result='error'
        return render(request, 'cipher_viginere.html', {'result':result, 'previoustext':text, 'previouskey':key})
    return render(request, 'cipher_viginere.html')


def cipher_monoalphabetic(request):
    if request.method=='POST':
        text=request.POST.get('text')
        key=request.POST.get('key')
        if request.POST.get('enc'):
            result=monoalphabetic_cipher.monoalphabetic_cipher_enc(text, key)
        elif request.POST.get('dec'):
            result=monoalphabetic_cipher.monoalphabetic_cipher_dec(text, key)
        else:
            result='error'
        return render(request, 'cipher_monoalphabetic.html', {'result':result, 'previoustext':text, 'previouskey':key})
    return render(request, 'cipher_monoalphabetic.html')

def cipher_railfence(request):
    if request.method=='POST':
        text=request.POST.get('text')
        key=request.POST.get('key')
        if request.POST.get('enc'):
            result=rail_fence_cipher.rail_fence_cipher_enc(text, int(key))
        elif request.POST.get('dec'):
            result=rail_fence_cipher.rail_fence_cipher_dec(text, int(key))
        else:
            result='error'
        return render(request, 'cipher_railfence.html', {'result':result, 'previoustext':text, 'previouskey':key})
    return render(request, 'cipher_railfence.html')

def cipher_rowtrans(request):
    if request.method=='POST':
        text=request.POST.get('text')
        key=request.POST.get('key')
        if request.POST.get('enc'):
            result=row_transposition_cipher.row_transposition_cipher_enc(text, key)
        elif request.POST.get('dec'):
            result=row_transposition_cipher.row_transposition_cipher_dec(text, key)
        else:
            result='error'
        return render(request, 'cipher_rowtrans.html', {'result':result, 'previoustext':text, 'previouskey':key})
    return render(request, 'cipher_rowtrans.html')