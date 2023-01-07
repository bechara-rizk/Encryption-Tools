from django.shortcuts import render
from .codes import texthex, extendedEuclid, exponentiation, gallois_fields
# from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

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
            print('hi', request.POST)
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