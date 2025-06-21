#!/usr/bin/env python3
import re,math,sys,random,requests
from typing import List,Dict,Any,Tuple,Optional

class F:
 __slots__=('n','p','b')
 def __init__(self,n,p,b):self.n,self.p,self.b=n,p,b

class R(Exception):
 __slots__=('v',)
 def __init__(self,v):self.v=v

class B(Exception):pass
class C(Exception):pass

class I:
 T=re.compile(r'(?P<S>"[^"]*")|(?P<N>-?\d+\.?\d*)|(?P<I>[a-zA-Z_]\w*)|(?P<K>if|else|end|func|return|for|while|break|continue|in)|(?P<C>==|!=|<=|>=|<|>)|(?P<L>and|or|not)|(?P<A>=)|(?P<SC>;)|(?P<LP>\()|(?P<RP>\))|(?P<LB>\[)|(?P<RB>\])|(?P<LC>\{)|(?P<RC>\})|(?P<CO>:)|(?P<CM>,)|(?P<D>\.)|(?P<O>[\+\-\*/%])|(?P<P>\*\*)|(?P<W>\s+)|(?P<U>.)')
 
 def __init__(self):
  self.v={}
  self.f={}
  self.s=[]
  self.b={'print':lambda*a:print(' '.join(str(x)for x in a)),'input':lambda p="":input(str(p)),'int':self._i,'float':lambda x:float(str(x)),'str':str,'abs':abs,'sqrt':math.sqrt,'sin':math.sin,'cos':math.cos,'tan':math.tan,'asin':math.asin,'acos':math.acos,'atan':math.atan,'atan2':math.atan2,'sinh':math.sinh,'cosh':math.cosh,'tanh':math.tanh,'log':math.log,'log10':math.log10,'log2':math.log2,'exp':math.exp,'floor':math.floor,'ceil':math.ceil,'round':round,'max':max,'min':min,'pow':pow,'len':len,'type':lambda x:type(x).__name__,'sum':lambda l:sum(l)if isinstance(l,list)else l,'avg':lambda l:sum(l)/len(l)if isinstance(l,list)and l else 0,'factorial':self._fact,'gcd':math.gcd,'lcm':self._lcm,'mod':lambda x,y:x%y,'div':lambda x,y:x//y,'random':random.random,'randint':random.randint,'range':lambda*a:list(range(*[int(x)for x in a])),'append':self._app,'pop':self._pop,'size':len,'sort':sorted,'reverse':lambda l:l[::-1]if isinstance(l,list)else l,'pi':lambda:math.pi,'e':lambda:math.e,'deg':math.degrees,'rad':math.radians,'is_prime':self._prime,'fib':self._fib,'get':self._get,'post':self._post}
 
 def _i(self,x):
  s=str(x)
  return int(float(s))if'.'in s else int(s)
 
 def _fact(self,n):
  n=int(n)
  if n<0:raise ValueError("Factorial not defined for negative numbers")
  return math.factorial(n)
 
 def _lcm(self,a,b):
  a,b=int(a),int(b)
  return abs(a*b)//math.gcd(a,b)
 
 def _app(self,l,i):
  if not isinstance(l,list):raise TypeError("append() requires a list")
  l.append(i)
  return l
 
 def _pop(self,l,i=-1):
  if not isinstance(l,list):raise TypeError("pop() requires a list")
  return l.pop(int(i))
 
 def _prime(self,n):
  n=int(n)
  return n>1 and all(n%i for i in range(2,int(n**0.5)+1))
 
 def _fib(self,n):
  n=int(n)
  if n<=0:return 0
  if n==1:return 1
  a,b=0,1
  for _ in range(2,n+1):a,b=b,a+b
  return b
 
 def _get(self,u,h=None):
  try:
   r=requests.get(u,headers=h or{})
   return{'status':r.status_code,'content':r.text,'json':r.json()if'application/json'in r.headers.get('Content-Type','').lower()else None}
  except Exception as e:return{'status':None,'error':str(e),'content':None,'json':None}
 
 def _post(self,u,d=None,h=None):
  try:
   r=requests.post(u,json=d,headers=h or{})
   return{'status':r.status_code,'content':r.text,'json':r.json()if'application/json'in r.headers.get('Content-Type','').lower()else None}
  except Exception as e:return{'status':None,'error':str(e),'content':None,'json':None}
 
 def t(self,c):return[(m.lastgroup,m.group())for m in self.T.finditer(c)if m.lastgroup!='W']
 
 def e(self,t,s=0):return self.o(t,s)
 
 def o(self,t,s):
  l,p=self.a(t,s)
  while p<len(t)and t[p]==('L','or'):
   p+=1
   r,p=self.a(t,p)
   l=l or r
  return l,p
 
 def a(self,t,s):
  l,p=self.n(t,s)
  while p<len(t)and t[p]==('L','and'):
   p+=1
   r,p=self.n(t,p)
   l=l and r
  return l,p
 
 def n(self,t,s):
  if s<len(t)and t[s]==('L','not'):
   x,p=self.c(t,s+1)
   return not x,p
  return self.c(t,s)
 
 def c(self,t,s):
  l,p=self.ad(t,s)
  if p<len(t)and t[p][0]=='C':
   o=t[p][1]
   p+=1
   r,p=self.ad(t,p)
   ops={'==':lambda x,y:x==y,'!=':lambda x,y:x!=y,'<':lambda x,y:x<y,'>':lambda x,y:x>y,'<=':lambda x,y:x<=y,'>=':lambda x,y:x>=y}
   l=ops[o](l,r)
  return l,p
 
 def ad(self,t,s):
  l,p=self.m(t,s)
  while p<len(t)and t[p][0]=='O'and t[p][1]in'+-':
   o=t[p][1]
   p+=1
   r,p=self.m(t,p)
   l=l+r if o=='+'else l-r
  return l,p
 
 def m(self,t,s):
  l,p=self.u(t,s)
  while p<len(t)and t[p][0]=='O'and t[p][1]in'*/%':
   o=t[p][1]
   p+=1
   r,p=self.u(t,p)
   if o=='/'and r==0:raise ZeroDivisionError("Division by zero")
   elif o=='%'and r==0:raise ZeroDivisionError("Modulo by zero")
   l=l/r if o=='/'else l%r if o=='%'else l*r
  return l,p
 
 def u(self,t,s):
  if s<len(t)and t[s][0]=='O'and t[s][1]in'+-':
   o=t[s][1]
   x,p=self.pw(t,s+1)
   return -x if o=='-'else x,p
  return self.pw(t,s)
 
 def pw(self,t,s):
  l,p=self.pr(t,s)
  if p<len(t)and t[p][0]=='P':
   p+=1
   r,p=self.pw(t,p)
   l=l**r
  return l,p
 
 def pr(self,t,s):
  if s>=len(t):raise SyntaxError("Unexpected end of expression")
  tp,tv=t[s]
  if tp=='N':return(float(tv)if'.'in tv else int(tv)),s+1
  if tp=='S':return tv[1:-1],s+1
  if tp=='LB':return self.ls(t,s)
  if tp=='LC':return self.di(t,s)
  if tp=='I':
   if s+1<len(t):
    if t[s+1][0]=='LP':return self.fc(t,s)
    if t[s+1][0]=='LB':return self.la(t,s)
    if t[s+1][0]=='D':return self.pa(t,s)
   if tv in self.v:return self.v[tv],s+1
   raise NameError(f"Variable '{tv}' not defined")
  if tp=='LP':
   x,p=self.e(t,s+1)
   if p>=len(t)or t[p][0]!='RP':raise SyntaxError("Expected closing parenthesis")
   return x,p+1
  raise SyntaxError(f"Unexpected token: {tv}")
 
 def di(self,t,s):
  p=s+1
  r={}
  if p<len(t)and t[p][0]!='RC':
   while True:
    if p>=len(t):raise SyntaxError("Expected dictionary key")
    kt,kv=t[p]
    if kt=='S':k=kv[1:-1];p+=1
    elif kt=='I':k=kv;p+=1
    else:raise SyntaxError(f"Expected string or identifier as dictionary key, got {kv}")
    if p>=len(t)or t[p][0]!='CO':raise SyntaxError("Expected ':' after dictionary key")
    p+=1
    v,p=self.e(t,p)
    r[k]=v
    if p>=len(t):raise SyntaxError("Expected closing brace")
    if t[p][0]=='RC':break
    if t[p][0]=='CM':p+=1
    else:raise SyntaxError("Expected comma or closing brace")
  elif p>=len(t):raise SyntaxError("Expected closing brace")
  return r,p+1
 
 def pa(self,t,s):
  vn=t[s][1]
  if s+2>=len(t)or t[s+1][0]!='D'or t[s+2][0]!='I':raise SyntaxError("Invalid property access")
  pn=t[s+2][1]
  if vn not in self.v:raise NameError(f"Variable '{vn}' not defined")
  vv=self.v[vn]
  if isinstance(vv,dict):
   if pn in vv:return vv[pn],s+3
   raise KeyError(f"Key '{pn}' not found in dictionary")
  if pn=='length':
   if isinstance(vv,(list,str)):return len(vv),s+3
   raise TypeError(f"'{vn}' does not have a length property")
  raise AttributeError(f"'{type(vv).__name__}' object has no attribute '{pn}'")
 
 def ls(self,t,s):
  p=s+1
  e=[]
  if p<len(t)and t[p][0]!='RB':
   while True:
    el,p=self.e(t,p)
    e.append(el)
    if p>=len(t):raise SyntaxError("Expected closing bracket")
    if t[p][0]=='RB':break
    if t[p][0]=='CM':p+=1
    else:raise SyntaxError("Expected comma or closing bracket")
  elif p>=len(t):raise SyntaxError("Expected closing bracket")
  return e,p+1
 
 def la(self,t,s):
  vn=t[s][1]
  p=s+2
  i,p=self.e(t,p)
  if p>=len(t)or t[p][0]!='RB':raise SyntaxError("Expected closing bracket")
  if vn not in self.v:raise NameError(f"Variable '{vn}' not defined")
  vv=self.v[vn]
  if not isinstance(vv,(list,str)):raise TypeError(f"'{vn}' is not indexable")
  try:return vv[int(i)],p+1
  except IndexError:raise IndexError("Index out of range")
 
 def fc(self,t,s):
  fn=t[s][1]
  p=s+2
  a=[]
  if p<len(t)and t[p][0]!='RP':
   while True:
    ar,p=self.e(t,p)
    a.append(ar)
    if p>=len(t):raise SyntaxError("Expected closing parenthesis")
    if t[p][0]=='RP':break
    if t[p][0]=='CM':p+=1
    else:raise SyntaxError("Expected comma or closing parenthesis")
  elif p>=len(t):raise SyntaxError("Expected closing parenthesis")
  p+=1
  if fn in self.b:return self.b[fn](*a),p
  if fn in self.f:return self.cu(fn,a),p
  raise NameError(f"Function '{fn}' not defined")
 
 def cu(self,fn,a):
  fu=self.f[fn]
  if len(a)!=len(fu.p):raise TypeError(f"Function '{fn}' expects {len(fu.p)} arguments, got {len(a)}")
  ov=self.v.copy()
  self.s.append(ov)
  for p,ar in zip(fu.p,a):self.v[p]=ar
  try:r=self.eb(fu.b)
  except R as ex:r=ex.v
  except(B,C):r=None
  finally:self.v=self.s.pop()
  return r if r is not None else 0
 
 def eb(self,bl):
  i=0
  while i<len(bl):
   l=bl[i].strip()
   if not l or l.startswith('#'):i+=1;continue
   if l.startswith('return '):
    re=l[7:].rstrip(';')
    if re:
     t=self.t(re)
     v,_=self.e(t,0)
     raise R(v)
    raise R(None)
   elif l.startswith(('if ','for ','while ')):
    if l.startswith('if '):i=self.eif(bl,i)
    elif l.startswith('for '):i=self.efor(bl,i)
    elif l.startswith('while '):i=self.ewh(bl,i)
    i+=1
   else:self.el(l);i+=1
  return None
 
 def ps(self,t):
  if not t:return
  if t[0]==('K','break'):raise B()
  elif t[0]==('K','continue'):raise C()
  elif t[0]==('K','if'):self.pif(t)
  elif t[0]==('K','func'):self.pfd(t)
  elif t[0]==('K','for'):self.pfor(t)
  elif t[0]==('K','while'):self.pwh(t)
  elif len(t)>=3 and t[0][0]=='I'and t[1]==('A','='):
   vn=t[0][1]
   v,_=self.e(t,2)
   self.v[vn]=v
  elif len(t)>=5 and t[0][0]=='I'and t[1]==('LB','['):
   vn=t[0][1]
   ix,p=self.e(t,2)
   if p<len(t)and t[p]==('RB',']')and p+1<len(t)and t[p+1]==('A','='):
    v,_=self.e(t,p+2)
    if vn not in self.v or not isinstance(self.v[vn],list):raise TypeError(f"'{vn}' is not a list")
    ix=int(ix)
    if ix>=len(self.v[vn]):raise IndexError("List assignment index out of range")
    self.v[vn][ix]=v
   else:raise SyntaxError("Invalid list assignment")
  else:self.e(t,0)
 
 def pfd(self,t):
  if len(t)<4:raise SyntaxError("Invalid function definition")
  fn=t[1][1]
  if t[2]!=('LP','('):raise SyntaxError("Expected '(' after function name")
  p=3
  pa=[]
  if p<len(t)and t[p]!=('RP',')'):
   while True:
    if t[p][0]!='I':raise SyntaxError("Expected parameter name")
    pa.append(t[p][1])
    p+=1
    if p>=len(t):raise SyntaxError("Expected closing parenthesis")
    if t[p]==('RP',')'):break
    if t[p]==('CM',','):p+=1
    else:raise SyntaxError("Expected comma or closing parenthesis")
  return('func',fn,pa)
 
 def pif(self,t):
  co,_=self.e(t,1)
  return('if',co)
 
 def pfor(self,t):
  if len(t)<4:raise SyntaxError("Invalid for statement")
  vn=t[1][1]
  if len(t)<3 or t[2][1]!='in':raise SyntaxError("Expected 'in' in for statement")
  it,_=self.e(t,3)
  return('for',vn,it)
 
 def pwh(self,t):
  co,_=self.e(t,1)
  return('while',co)
 
 def bs(self,l):
  l=l.strip()
  return l.startswith(('for ','while ','if ','func '))and not l.startswith(('for;','while;','if;','func;'))
 
 def be(self,ls,sl):
  d=1
  cl=sl+1
  while cl<len(ls)and d>0:
   l=ls[cl].strip()
   if self.bs(l):d+=1
   elif l=='end;':d-=1
   cl+=1
  if d>0:raise SyntaxError(f"Missing 'end;' for block starting at line {sl+1}")
  return cl-1
 
 def efb(self,ls,sl):
  fl=ls[sl].strip()
  if fl.endswith(';'):fl=fl[:-1]
  t=self.t(fl)
  _,fn,pa=self.pfd(t)
  el=self.be(ls,sl)
  bl=ls[sl+1:el]
  self.f[fn]=F(fn,pa,bl)
  return el
 
 def efor(self,ls,sl):
  fol=ls[sl].strip()
  if fol.endswith(';'):fol=fol[:-1]
  t=self.t(fol)
  _,vn,it=self.pfor(t)
  el=self.be(ls,sl)
  hv=vn in self.v
  ov=self.v.get(vn)if hv else None
  try:
   for i in it:
    self.v[vn]=i
    try:self.ebb(ls,sl+1,el)
    except B:break
    except C:continue
  finally:
   if hv:self.v[vn]=ov
   else:self.v.pop(vn,None)
  return el
 
 def ewh(self,ls,sl):
  wl=ls[sl].strip()
  if wl.endswith(';'):wl=wl[:-1]
  el=self.be(ls,sl)
  while True:
   t=self.t(wl)
   _,co=self.pwh(t)
   if not co:break
   try:self.ebb(ls,sl+1,el)
   except B:break
   except C:continue
  return el
 
 def eif(self,ls,sl):
  cl=ls[sl].strip()
  if cl.endswith(';'):cl=cl[:-1]
  t=self.t(cl)
  co,_=self.e(t,1)
  el=self.be(ls,sl)
  ell=None
  for i in range(sl+1,el):
   l=ls[i].strip()
   if l=='else'or l=='else;':ell=i;break
  if co:self.ebb(ls,sl+1,ell or el)
  elif ell:self.ebb(ls,ell+1,el)
  return el
 
 def ebb(self,ls,st,en):
  i=st
  while i<en:
   l=ls[i].strip()
   if not l or l.startswith('#')or l in('else','else;'):i+=1;continue
   if self.bs(l):
    if l.startswith('for '):i=self.efor(ls,i)
    elif l.startswith('while '):i=self.ewh(ls,i)
    elif l.startswith('if '):i=self.eif(ls,i)
    elif l.startswith('func '):i=self.efb(ls,i)
    i+=1
   else:self.el(l);i+=1
 
 def el(self,l):
  l=l.strip()
  if not l or l.startswith('#'):return
  if not l.endswith(';'):raise SyntaxError("Statement must end with semicolon")
  t=self.t(l[:-1])
  self.ps(t)
 
 def ex(self,c):
  ls=c.split('\n')
  ln=0
  while ln<len(ls):
   try:
    l=ls[ln].strip()
    if not l or l.startswith('#'):ln+=1;continue
    if self.bs(l):
     if l.startswith('func '):ln=self.efb(ls,ln)+1
     elif l.startswith('if '):ln=self.eif(ls,ln)+1
     elif l.startswith('for '):ln=self.efor(ls,ln)+1
     elif l.startswith('while '):ln=self.ewh(ls,ln)+1
    elif l in('else','else;','end;'):ln+=1
    else:self.el(l);ln+=1
   except Exception as e:print(f"Error on line {ln+1}: {e}");break
 
 def rf(self,fn):
  if not fn.endswith('.blip'):print("Error: File must have .blip extension");return
  try:
   with open(fn,'r')as f:self.ex(f.read())
  except FileNotFoundError:print(f"Error: File '{fn}' not found")
  except Exception as e:print(f"Error reading file: {e}")

def main():
 i=I()
 if len(sys.argv)>1:i.rf(sys.argv[1])

if __name__=="__main__":main()
