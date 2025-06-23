#!/usr/bin/env python3
import re,math,sys,random,requests,signal,time,os,json
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
 T=re.compile(r'(?P<S>"[^"]*")|(?P<N>-?\d+\.?\d*)|(?P<I>[a-zA-Z_]\w*)|(?P<K>if|else|end|func|return|for|while|break|continue|in)|(?P<C>==|!=|<=|>=|<|>)|(?P<L>and|or|not)|(?P<A>=)|(?P<SC>;)|(?P<LP>\()|(?P<RP>\))|(?P<LB>\[)|(?P<RB>\])|(?P<LC>\{)|(?P<RC>\})|(?P<CO>:)|(?P<DD>\.\.)|(?P<CM>,)|(?P<D>\.)|(?P<O>[\+\-\*/%])|(?P<P>\*\*)|(?P<W>\s+)|(?P<U>.)')
 def __init__(self):
  self.v,self.f,self.s,self.i,self.d,self.t={},{},[],0,0,None
  signal.signal(signal.SIGINT,self.h)
  self.b={'print':lambda *a:self.pr(*a),'input':lambda p="":self.inp(p),'int':lambda x:self.it(x),'float':lambda x:float(str(x)),'str':str,'abs':abs,'sqrt':math.sqrt,'sin':math.sin,'cos':math.cos,'tan':math.tan,'asin':math.asin,'acos':math.acos,'atan':math.atan,'atan2':math.atan2,'sinh':math.sinh,'cosh':math.cosh,'tanh':math.tanh,'log':math.log,'log10':math.log10,'log2':math.log2,'exp':math.exp,'floor':math.floor,'ceil':math.ceil,'round':round,'max':max,'min':min,'pow':pow,'len':len,'type':lambda x:type(x).__name__,'sum':lambda l:sum(l)if isinstance(l,list)else l,'avg':lambda l:sum(l)/len(l)if isinstance(l,list)and l else 0,'factorial':lambda n:self.fa(n),'gcd':math.gcd,'lcm':lambda a,b:self.lc(a,b),'mod':lambda x,y:x%y,'div':lambda x,y:x//y,'random':random.random,'randint':random.randint,'range':lambda*a:list(range(*[int(x)for x in a])),'append':lambda l,i:self.ap(l,i),'pop':lambda l,i=-1:self.po(l,i),'size':len,'sort':sorted,'reverse':lambda l:l[::-1]if isinstance(l,list)else l,'pi':lambda:math.pi,'e':lambda:math.e,'deg':math.degrees,'rad':math.radians,'is_prime':lambda n:self.pm(n),'fib':lambda n:self.fi(n),'get':lambda u,h=None:self.ge(u,h),'post':lambda u,d=None,h=None:self.ps(u,d,h),'read_file':lambda f:self.rdf(f),'write_file':lambda f,d:self.wrf(f,d),'append_file':lambda f,d:self.apf(f,d),'file_exists':lambda f:self.fex(f),'list_dir':lambda d='.':self.lsd(d),'delete_file':lambda f:self.dlf(f),'file_size':lambda f:self.fsz(f),'json_parse':lambda s:self.jpa(s),'json_stringify':lambda d:self.jst(d),'read_json':lambda f:self.rjf(f),'write_json':lambda f,d:self.wjf(f,d)}
 def h(self,s,f):self.i=1;print("\nProgram interrupted");sys.exit(0)
 def c(self):
  if self.i:raise KeyboardInterrupt
 def pr(self,*a):print(' '.join(str(x)for x in a))
 def inp(self,p=""):
  try:return input(str(p))
  except KeyboardInterrupt:self.h(None,None)
 def it(self,x):s=str(x);return int(float(s))if'.'in s else int(s)
 def fa(self,n):n=int(n);return math.factorial(n)if n>=0 else ValueError("Negative factorial")
 def lc(self,a,b):a,b=int(a),int(b);return abs(a*b)//math.gcd(a,b)
 def ap(self,l,i):
  if not isinstance(l,list):raise TypeError("append() requires list")
  l.append(i);return l
 def po(self,l,i=-1):
  if not isinstance(l,list):raise TypeError("pop() requires list")
  return l.pop(int(i))
 def pm(self,n):n=int(n);return n>1 and all(n%i for i in range(2,int(n**0.5)+1))
 def fi(self,n):
  n=int(n)
  if n<=0:return 0
  if n==1:return 1
  a,b=0,1
  for _ in range(2,n+1):self.c();a,b=b,a+b
  return b
 def ge(self,u,h=None):
  try:
   r=requests.get(u,headers=h or{})
   return{'status':r.status_code,'content':r.text,'json':r.json()if'application/json'in r.headers.get('Content-Type','')else None}
  except KeyboardInterrupt:self.h(None,None)
  except Exception as e:return{'status':None,'error':str(e),'content':None,'json':None}
 def ps(self,u,d=None,h=None):
  try:
   r=requests.post(u,json=d,headers=h or{})
   return{'status':r.status_code,'content':r.text,'json':r.json()if'application/json'in r.headers.get('Content-Type','')else None}
  except KeyboardInterrupt:self.h(None,None)
  except Exception as e:return{'status':None,'error':str(e),'content':None,'json':None}
 def rdf(self,f):
  try:
   with open(str(f),'r')as file:return file.read()
  except Exception as e:return f"Error: {e}"
 def wrf(self,f,d):
  try:
   with open(str(f),'w')as file:file.write(str(d));return"Success"
  except Exception as e:return f"Error: {e}"
 def apf(self,f,d):
  try:
   with open(str(f),'a')as file:file.write(str(d));return"Success"
  except Exception as e:return f"Error: {e}"
 def fex(self,f):return os.path.exists(str(f))
 def lsd(self,d='.'):
  try:return os.listdir(str(d))
  except Exception as e:return f"Error: {e}"
 def dlf(self,f):
  try:os.remove(str(f));return"Success"
  except Exception as e:return f"Error: {e}"
 def fsz(self,f):
  try:return os.path.getsize(str(f))
  except Exception as e:return f"Error: {e}"
 def jpa(self,s):
  try:return json.loads(str(s))
  except Exception as e:return f"JSON Error: {e}"
 def jst(self,d):
  try:return json.dumps(d,ensure_ascii=False)
  except Exception as e:return f"JSON Error: {e}"
 def rjf(self,f):
  try:
   with open(str(f),'r')as file:return json.load(file)
  except Exception as e:return f"JSON Error: {e}"
 def wjf(self,f,d):
  try:
   with open(str(f),'w')as file:json.dump(d,file,ensure_ascii=False,indent=2);return"Success"
  except Exception as e:return f"JSON Error: {e}"
 def tk(self,c):return[(m.lastgroup,m.group())for m in self.T.finditer(c)if m.lastgroup!='W']
 def e(self,t,s=0):return self.o(t,s)
 def o(self,t,s):
  self.c();l,p=self.a(t,s)
  while p<len(t)and t[p]==('L','or'):self.c();p+=1;r,p=self.a(t,p);l=l or r
  return l,p
 def a(self,t,s):
  self.c();l,p=self.n(t,s)
  while p<len(t)and t[p]==('L','and'):self.c();p+=1;r,p=self.n(t,p);l=l and r
  return l,p
 def n(self,t,s):
  self.c()
  if s<len(t)and t[s]==('L','not'):x,p=self.co(t,s+1);return not x,p
  return self.co(t,s)
 def co(self,t,s):
  self.c();l,p=self.ad(t,s)
  if p<len(t)and t[p][0]=='C':
   o=t[p][1];p+=1;r,p=self.ad(t,p)
   ops={'==':lambda x,y:x==y,'!=':lambda x,y:x!=y,'<':lambda x,y:x<y,'>':lambda x,y:x>y,'<=':lambda x,y:x<=y,'>=':lambda x,y:x>=y}
   l=ops[o](l,r)
  return l,p
 def ad(self,t,s):
  self.c();l,p=self.m(t,s)
  while p<len(t)and(t[p][0]=='O'and t[p][1]in'+-'or t[p][0]=='DD'):
   self.c();o=t[p][1];p+=1;r,p=self.m(t,p)
   l=str(l)+str(r)if o=='..'else l+r if o=='+'else l-r
  return l,p
 def m(self,t,s):
  self.c();l,p=self.u(t,s)
  while p<len(t)and t[p][0]=='O'and t[p][1]in'*/%':
   self.c();o=t[p][1];p+=1;r,p=self.u(t,p)
   if o in'/%'and r==0:raise ZeroDivisionError("Division by zero")
   l=l/r if o=='/'else l%r if o=='%'else l*r
  return l,p
 def u(self,t,s):
  self.c()
  if s<len(t)and t[s][0]=='O'and t[s][1]in'+-':o=t[s][1];x,p=self.pw(t,s+1);return -x if o=='-'else x,p
  return self.pw(t,s)
 def pw(self,t,s):self.c();l,p=self.prim(t,s);return(l**self.pw(t,p+1)[0],self.pw(t,p+1)[1])if p<len(t)and t[p][0]=='P'else(l,p)
 def prim(self,t,s):
  self.c()
  if s>=len(t):raise SyntaxError("Unexpected end")
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
  if tp=='LP':x,p=self.e(t,s+1);return(x,p+1)if p<len(t)and t[p][0]=='RP'else SyntaxError("Expected )")
  raise SyntaxError(f"Unexpected token: {tv}")
 def di(self,t,s):
  self.c();p=s+1;r={}
  if p<len(t)and t[p][0]!='RC':
   while True:
    self.c()
    if p>=len(t):raise SyntaxError("Expected dict key")
    kt,kv=t[p]
    k=kv[1:-1]if kt=='S'else kv if kt=='I'else SyntaxError(f"Expected string/id as key")
    p+=1
    if p>=len(t)or t[p][0]!='CO':raise SyntaxError("Expected :")
    p+=1;v,p=self.e(t,p);r[k]=v
    if p>=len(t):raise SyntaxError("Expected }")
    if t[p][0]=='RC':break
    if t[p][0]=='CM':p+=1
    else:raise SyntaxError("Expected , or }")
  return r,p+1
 def pa(self,t,s):
  self.c();vn,pn=t[s][1],t[s+2][1]
  if s+2>=len(t)or t[s+1][0]!='D'or t[s+2][0]!='I':raise SyntaxError("Invalid property")
  if vn not in self.v:raise NameError(f"Variable '{vn}' not defined")
  vv=self.v[vn]
  if isinstance(vv,dict):return(vv[pn],s+3)if pn in vv else KeyError(f"Key '{pn}' not found")
  if pn=='length'and isinstance(vv,(list,str)):return len(vv),s+3
  raise AttributeError(f"No attribute '{pn}'")
 def ls(self,t,s):
  self.c();p=s+1;e=[]
  if p<len(t)and t[p][0]!='RB':
   while True:
    self.c();el,p=self.e(t,p);e.append(el)
    if p>=len(t):raise SyntaxError("Expected ]")
    if t[p][0]=='RB':break
    if t[p][0]in('CM','DD'):p+=1
    else:raise SyntaxError("Expected , or ]")
  return e,p+1
 def la(self,t,s):
  self.c();vn=t[s][1];p=s+2;i,p=self.e(t,p)
  if p>=len(t)or t[p][0]!='RB':raise SyntaxError("Expected ]")
  if vn not in self.v:raise NameError(f"Variable '{vn}' not defined")
  vv=self.v[vn]
  if not isinstance(vv,(list,str)):raise TypeError(f"'{vn}' not indexable")
  try:return vv[int(i)],p+1
  except IndexError:raise IndexError("Index out of range")
 def fc(self,t,s):
  self.c();fn=t[s][1];p=s+2;a=[]
  if p<len(t)and t[p][0]!='RP':
   while True:
    self.c();ar,p=self.e(t,p);a.append(ar)
    if p>=len(t):raise SyntaxError("Expected )")
    if t[p][0]=='RP':break
    if t[p][0]=='CM':p+=1
    else:raise SyntaxError("Expected , or )")
  p+=1
  if fn in self.b:return self.b[fn](*a),p
  if fn in self.f:return self.cu(fn,a),p
  raise NameError(f"Function '{fn}' not defined")
 def cu(self,fn,a):
  self.c();fu=self.f[fn]
  if len(a)!=len(fu.p):raise TypeError(f"Function '{fn}' expects {len(fu.p)} args")
  ov=self.v.copy();self.s.append(ov)
  for p,ar in zip(fu.p,a):self.v[p]=ar
  try:r=self.eb(fu.b)
  except R as ex:r=ex.v
  except(B,C):r=None
  finally:self.v=self.s.pop()
  return r if r is not None else 0
 def eb(self,bl):
  i=0
  while i<len(bl):
   self.c();l=bl[i].strip()
   if not l or l.startswith('#'):i+=1;continue
   if l.startswith('return '):
    re=l[7:].rstrip(';')
    if re:t=self.tk(re);v,_=self.e(t,0);raise R(v)
    raise R(None)
   elif l.startswith(('if ','for ','while ')):
    if l.startswith('if '):i=self.eif(bl,i)
    elif l.startswith('for '):i=self.efor(bl,i)
    elif l.startswith('while '):i=self.ewh(bl,i)
    i+=1
   else:self.el(l);i+=1
  return None
 def pst(self,t):
  self.c()
  if not t:return
  if t[0]==('K','break'):raise B()
  elif t[0]==('K','continue'):raise C()
  elif t[0]==('K','if'):self.pif(t)
  elif t[0]==('K','func'):self.pfd(t)
  elif t[0]==('K','for'):self.pfor(t)
  elif t[0]==('K','while'):self.pwh(t)
  elif len(t)>=3 and t[0][0]=='I'and t[1]==('A','='):vn=t[0][1];v,_=self.e(t,2);self.v[vn]=v
  elif len(t)>=5 and t[0][0]=='I'and t[1]==('LB','['):
   vn=t[0][1];ix,p=self.e(t,2)
   if p<len(t)and t[p]==('RB',']')and p+1<len(t)and t[p+1]==('A','='):
    v,_=self.e(t,p+2)
    if vn not in self.v or not isinstance(self.v[vn],list):raise TypeError(f"'{vn}' not list")
    ix=int(ix)
    if ix>=len(self.v[vn]):raise IndexError("Index out of range")
    self.v[vn][ix]=v
   else:raise SyntaxError("Invalid list assignment")
  else:self.e(t,0)
 def pfd(self,t):
  if len(t)<4:raise SyntaxError("Invalid function")
  fn=t[1][1]
  if t[2]!=('LP','('):raise SyntaxError("Expected (")
  p,pa=3,[]
  if p<len(t)and t[p]!=('RP',')'):
   while True:
    if t[p][0]!='I':raise SyntaxError("Expected param")
    pa.append(t[p][1]);p+=1
    if p>=len(t):raise SyntaxError("Expected )")
    if t[p]==('RP',')'):break
    if t[p]==('CM',','):p+=1
    else:raise SyntaxError("Expected , or )")
  return('func',fn,pa)
 def pif(self,t):co,_=self.e(t,1);return('if',co)
 def pfor(self,t):
  if len(t)<4:raise SyntaxError("Invalid for")
  vn=t[1][1]
  if len(t)<3 or t[2][1]!='in':raise SyntaxError("Expected in")
  it,_=self.e(t,3);return('for',vn,it)
 def pwh(self,t):co,_=self.e(t,1);return('while',co)
 def bs(self,l):l=l.strip();return l.startswith(('for ','while ','if ','func '))and not l.startswith(('for;','while;','if;','func;'))
 def be(self,ls,sl):
  d,cl=1,sl+1
  while cl<len(ls)and d>0:
   l=ls[cl].strip()
   if self.bs(l):d+=1
   elif l=='end;':d-=1
   cl+=1
  if d>0:raise SyntaxError(f"Missing end")
  return cl-1
 def efb(self,ls,sl):
  fl=ls[sl].strip()
  if fl.endswith(';'):fl=fl[:-1]
  t=self.tk(fl);_,fn,pa=self.pfd(t);el=self.be(ls,sl);bl=ls[sl+1:el];self.f[fn]=F(fn,pa,bl);return el
 def efor(self,ls,sl):
  self.c();fol=ls[sl].strip()
  if fol.endswith(';'):fol=fol[:-1]
  t=self.tk(fol);_,vn,it=self.pfor(t);el=self.be(ls,sl);hv=vn in self.v;ov=self.v.get(vn)if hv else None
  try:
   for i in it:
    self.c();self.v[vn]=i
    try:self.ebb(ls,sl+1,el)
    except B:break
    except C:continue
  finally:
   if hv:self.v[vn]=ov
   else:self.v.pop(vn,None)
  return el
 def ewh(self,ls,sl):
  self.c();wl=ls[sl].strip()
  if wl.endswith(';'):wl=wl[:-1]
  el=self.be(ls,sl)
  while True:
   self.c();t=self.tk(wl);_,co=self.pwh(t)
   if not co:break
   try:self.ebb(ls,sl+1,el)
   except B:break
   except C:continue
  return el
 def eif(self,ls,sl):
  self.c();cl=ls[sl].strip()
  if cl.endswith(';'):cl=cl[:-1]
  t=self.tk(cl);co,_=self.e(t,1);el=self.be(ls,sl);ell=None
  for i in range(sl+1,el):
   l=ls[i].strip()
   if l=='else'or l=='else;':ell=i;break
  if co:self.ebb(ls,sl+1,ell or el)
  elif ell:self.ebb(ls,ell+1,el)
  return el
 def ebb(self,ls,st,en):
  i=st
  while i<en:
   self.c();l=ls[i].strip()
   if not l or l.startswith('#')or l in('else','else;'):i+=1;continue
   if self.bs(l):
    if l.startswith('for '):i=self.efor(ls,i)
    elif l.startswith('while '):i=self.ewh(ls,i)
    elif l.startswith('if '):i=self.eif(ls,i)
    elif l.startswith('func '):i=self.efb(ls,i)
    i+=1
   else:self.el(l);i+=1
 def el(self,l):
  self.c();l=l.strip()
  if not l or l.startswith('#'):return
  if not l.endswith(';'):raise SyntaxError("Missing ;")
  t=self.tk(l[:-1]);self.pst(t)
 def ex(self,c):
  ls=c.split('\n')
  if ls and ls[0].strip()=='{debug}':self.d,self.t,ls=1,time.time(),ls[1:]
  ln=0
  while ln<len(ls):
   try:
    self.c();l=ls[ln].strip()
    if not l or l.startswith('#'):ln+=1;continue
    if self.bs(l):
     if l.startswith('func '):ln=self.efb(ls,ln)+1
     elif l.startswith('if '):ln=self.eif(ls,ln)+1
     elif l.startswith('for '):ln=self.efor(ls,ln)+1
     elif l.startswith('while '):ln=self.ewh(ls,ln)+1
    elif l in('else','else;','end;'):ln+=1
    else:self.el(l);ln+=1
   except KeyboardInterrupt:
    if self.d and self.t:print(f"\nInterrupted after {time.time()-self.t:.6f}s")
    return
   except Exception as e:print(f"Error line {ln+1}: {e}");break
  if self.d and self.t:print(f"\nCompleted in {time.time()-self.t:.6f}s")
 def rf(self,fn):
  if not fn.endswith('.blip'):print("Error: Must be .blip");return
  try:
   with open(fn,'r')as f:self.ex(f.read())
  except KeyboardInterrupt:
   if self.d and self.t:print(f"\nInterrupted after {time.time()-self.t:.6f}s")
  except FileNotFoundError:print(f"Error: File '{fn}' not found")
  except Exception as e:print(f"Error: {e}")
def main():
 try:
  i=I()
  if len(sys.argv)>1:i.rf(sys.argv[1])
 except KeyboardInterrupt:print("\nInterrupted")
if __name__=="__main__":main()
