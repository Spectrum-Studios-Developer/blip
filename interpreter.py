#!/usr/bin/env python3
import re,math,sys,random,requests,signal,time,threading,queue,concurrent.futures
from typing import List,Dict,Any,Tuple,Optional,Union
from functools import lru_cache
from collections import deque

class F:
 __slots__=('n','p','b')
 def __init__(self,n,p,b):self.n,self.p,self.b=n,p,b

class R(Exception):
 __slots__=('v',)
 def __init__(self,v):self.v=v

class B(Exception):pass
class C(Exception):pass

class T:
 __slots__=('v','s','i')
 def __init__(self):self.v,self.s,self.i={},deque(),0

class I:
 P=re.compile(r'(?P<S>"[^"]*")|(?P<N>-?\d+\.?\d*)|(?P<I>[a-zA-Z_]\w*)|(?P<K>if|else|end|func|return|for|while|break|continue|in|thread|join|async)|(?P<C>==|!=|<=|>=|<|>)|(?P<L>and|or|not)|(?P<A>=)|(?P<SC>;)|(?P<LP>\()|(?P<RP>\))|(?P<LB>\[)|(?P<RB>\])|(?P<LC>\{)|(?P<RC>\})|(?P<CO>:)|(?P<DD>\.\.)|(?P<CM>,)|(?P<D>\.)|(?P<O>[\+\-\*/%])|(?P<P>\*\*)|(?P<W>\s+)|(?P<U>.)')
 
 def __init__(self):
  self.v,self.f,self.s,self.i,self.d,self.t={},{},[],0,0,None
  self.x=threading.local()
  self.h={}
  self.p=concurrent.futures.ThreadPoolExecutor(max_workers=8)
  self.q=queue.Queue()
  self.l=threading.Lock()
  signal.signal(signal.SIGINT,self.z)
  self._init_builtins()
  self.c={}

 def _init_builtins(self):
  self.b={
   'print':self._pr,'input':self._in,'int':self._it,'float':lambda x:float(str(x)),
   'str':str,'abs':abs,'sqrt':math.sqrt,'sin':math.sin,'cos':math.cos,
   'tan':math.tan,'asin':math.asin,'acos':math.acos,'atan':math.atan,
   'atan2':math.atan2,'sinh':math.sinh,'cosh':math.cosh,'tanh':math.tanh,
   'log':math.log,'log10':math.log10,'log2':math.log2,'exp':math.exp,
   'floor':math.floor,'ceil':math.ceil,'round':round,'max':max,'min':min,
   'pow':pow,'len':len,'type':lambda x:type(x).__name__,
   'sum':lambda l:sum(l)if isinstance(l,list)else l,
   'avg':lambda l:sum(l)/len(l)if isinstance(l,list)and l else 0,
   'factorial':self._fa,'gcd':math.gcd,'lcm':self._lc,
   'mod':lambda x,y:x%y,'div':lambda x,y:x//y,
   'random':random.random,'randint':random.randint,
   'range':lambda*a:list(range(*[int(x)for x in a])),
   'append':self._ap,'pop':self._po,'size':len,'sort':sorted,
   'reverse':lambda l:l[::-1]if isinstance(l,list)else l,
   'pi':lambda:math.pi,'e':lambda:math.e,'deg':math.degrees,'rad':math.radians,
   'is_prime':self._pm,'fib':self._fi,'get':self._ge,'post':self._ps,
   'thread_create':self._tc,'thread_join':self._tj,'thread_id':self._tid,
   'thread_lock':self._tl,'thread_unlock':self._tu,
   'async_call':self._ac,'get_result':self._gr
  }

 def _gt(self):
  if not hasattr(self.x,'data'):self.x.data=T()
  return self.x.data

 def z(self,s,f):self.i=1;print("\nProgram interrupted");self.p.shutdown(wait=False);sys.exit(0)

 def k(self):
  if self.i:raise KeyboardInterrupt

 def _pr(self,*a):
  with self.l:print(' '.join(str(x)for x in a))

 def _in(self,p=""):
  try:return input(str(p))
  except KeyboardInterrupt:self.z(None,None)

 def _it(self,x):s=str(x);return int(float(s))if'.'in s else int(s)

 @lru_cache(maxsize=128)
 def _fa(self,n):
  n=int(n)
  if n<0:raise ValueError("Negative factorial")
  return math.factorial(n)

 def _lc(self,a,b):a,b=int(a),int(b);g=math.gcd(a,b);return abs(a*b)//g if g else 0

 def _ap(self,l,i):
  if not isinstance(l,list):raise TypeError("append() requires list")
  l.append(i);return l

 def _po(self,l,i=-1):
  if not isinstance(l,list):raise TypeError("pop() requires list")
  if not l:raise IndexError("pop from empty list")
  return l.pop(int(i))

 @lru_cache(maxsize=256)
 def _pm(self,n):n=int(n);return n>1 and all(n%i for i in range(2,int(n**0.5)+1))

 @lru_cache(maxsize=128)
 def _fi(self,n):
  n=int(n)
  if n<=0:return 0
  if n==1:return 1
  a,b=0,1
  for _ in range(2,n+1):
   self.k();a,b=b,a+b
  return b

 def _ge(self,u,h=None):
  try:
   r=requests.get(u,headers=h or{},timeout=10)
   ct=r.headers.get('Content-Type','')
   return{'status':r.status_code,'content':r.text,'json':r.json()if'application/json'in ct else None}
  except KeyboardInterrupt:self.z(None,None)
  except Exception as e:return{'status':None,'error':str(e),'content':None,'json':None}

 def _ps(self,u,d=None,h=None):
  try:
   r=requests.post(u,json=d,headers=h or{},timeout=10)
   ct=r.headers.get('Content-Type','')
   return{'status':r.status_code,'content':r.text,'json':r.json()if'application/json'in ct else None}
  except KeyboardInterrupt:self.z(None,None)
  except Exception as e:return{'status':None,'error':str(e),'content':None,'json':None}

 def _tc(self,fn,*args):
  tid=threading.get_ident()
  def w():
   try:
    if fn in self.f:return self.cu(fn,list(args))
    elif fn in self.b:return self.b[fn](*args)
    else:raise NameError(f"Function '{fn}' not defined")
   except Exception as e:return{'error':str(e)}
  
  u=self.p.submit(w)
  with self.l:self.h[tid]=u
  return tid

 def _tj(self,tid):
  with self.l:
   if tid in self.h:
    u=self.h.pop(tid)
    try:return u.result(timeout=30)
    except concurrent.futures.TimeoutError:return{'error':'Thread timeout'}
   return{'error':'Thread not found'}

 def _tid(self):return threading.get_ident()

 def _tl(self):self.l.acquire()
 def _tu(self):self.l.release()

 def _ac(self,fn,*args):return self._tc(fn,*args)
 def _gr(self,tid):return self._tj(tid)

 @lru_cache(maxsize=1024)
 def tk(self,c):
  if c in self.c:return self.c[c]
  t=[(m.lastgroup,m.group())for m in self.P.finditer(c)if m.lastgroup!='W']
  self.c[c]=t
  return t

 def e(self,t,s=0):return self.o(t,s)

 def o(self,t,s):
  self.k();l,p=self.a(t,s)
  while p<len(t)and t[p]==('L','or'):
   self.k();p+=1;r,p=self.a(t,p);l=l or r
  return l,p

 def a(self,t,s):
  self.k();l,p=self.n(t,s)
  while p<len(t)and t[p]==('L','and'):
   self.k();p+=1;r,p=self.n(t,p);l=l and r
  return l,p

 def n(self,t,s):
  self.k()
  if s<len(t)and t[s]==('L','not'):x,p=self.co(t,s+1);return not x,p
  return self.co(t,s)

 def co(self,t,s):
  self.k();l,p=self.ad(t,s)
  if p<len(t)and t[p][0]=='C':
   o=t[p][1];p+=1;r,p=self.ad(t,p)
   if o=='==':l=l==r
   elif o=='!=':l=l!=r
   elif o=='<':l=l<r
   elif o=='>':l=l>r
   elif o=='<=':l=l<=r
   elif o=='>=':l=l>=r
  return l,p

 def ad(self,t,s):
  self.k();l,p=self.m(t,s)
  while p<len(t):
   if t[p][0]=='O'and t[p][1]in'+-':
    self.k();o=t[p][1];p+=1;r,p=self.m(t,p)
    l=l+r if o=='+'else l-r
   elif t[p][0]=='DD':
    self.k();p+=1;r,p=self.m(t,p);l=str(l)+str(r)
   else:break
  return l,p

 def m(self,t,s):
  self.k();l,p=self.u(t,s)
  while p<len(t)and t[p][0]=='O'and t[p][1]in'*/%':
   self.k();o=t[p][1];p+=1;r,p=self.u(t,p)
   if o in'/%'and r==0:raise ZeroDivisionError("Division by zero")
   if o=='/':l=l/r
   elif o=='%':l=l%r
   else:l=l*r
  return l,p

 def u(self,t,s):
  self.k()
  if s<len(t)and t[s][0]=='O'and t[s][1]in'+-':
   o=t[s][1];x,p=self.pw(t,s+1)
   return -x if o=='-'else x,p
  return self.pw(t,s)

 def pw(self,t,s):
  self.k();l,p=self.pr(t,s)
  if p<len(t)and t[p][0]=='P':
   r,np=self.pw(t,p+1);return l**r,np
  return l,p

 def pr(self,t,s):
  self.k()
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
   if tv in self.b:return self.b[tv],s+1
   raise NameError(f"Variable '{tv}' not defined")
  if tp=='LP':
   x,p=self.e(t,s+1)
   if p<len(t)and t[p][0]=='RP':return x,p+1
   raise SyntaxError("Expected )")
  raise SyntaxError(f"Unexpected token: {tv}")

 def di(self,t,s):
  self.k();p=s+1;r={}
  if p<len(t)and t[p][0]!='RC':
   while True:
    self.k()
    if p>=len(t):raise SyntaxError("Expected dict key")
    kt,kv=t[p]
    if kt=='S':k=kv[1:-1]
    elif kt=='I':k=kv
    else:raise SyntaxError("Expected string/id as key")
    p+=1
    if p>=len(t)or t[p][0]!='CO':raise SyntaxError("Expected :")
    p+=1;v,p=self.e(t,p);r[k]=v
    if p>=len(t):raise SyntaxError("Expected }")
    if t[p][0]=='RC':break
    if t[p][0]=='CM':p+=1
    else:raise SyntaxError("Expected , or }")
  return r,p+1

 def pa(self,t,s):
  self.k();vn,pn=t[s][1],t[s+2][1]
  if s+2>=len(t)or t[s+1][0]!='D'or t[s+2][0]!='I':raise SyntaxError("Invalid property")
  if vn not in self.v:raise NameError(f"Variable '{vn}' not defined")
  vv=self.v[vn]
  if isinstance(vv,dict):
   if pn in vv:return vv[pn],s+3
   raise KeyError(f"Key '{pn}' not found")
  if pn=='length'and isinstance(vv,(list,str)):return len(vv),s+3
  raise AttributeError(f"No attribute '{pn}'")

 def ls(self,t,s):
  self.k();p=s+1;e=[]
  if p<len(t)and t[p][0]!='RB':
   while True:
    self.k();el,p=self.e(t,p);e.append(el)
    if p>=len(t):raise SyntaxError("Expected ]")
    if t[p][0]=='RB':break
    if t[p][0]in('CM','DD'):p+=1
    else:raise SyntaxError("Expected , or ]")
  return e,p+1

 def la(self,t,s):
  self.k();vn=t[s][1];p=s+2;i,p=self.e(t,p)
  if p>=len(t)or t[p][0]!='RB':raise SyntaxError("Expected ]")
  if vn not in self.v:raise NameError(f"Variable '{vn}' not defined")
  vv=self.v[vn]
  if not isinstance(vv,(list,str)):raise TypeError(f"'{vn}' not indexable")
  try:
   idx=int(i)
   if idx<0:idx+=len(vv)
   return vv[idx],p+1
  except (IndexError,ValueError):raise IndexError("Index out of range")

 def fc(self,t,s):
  self.k();fn=t[s][1];p=s+2;a=[]
  if p<len(t)and t[p][0]!='RP':
   while True:
    self.k();ar,p=self.e(t,p);a.append(ar)
    if p>=len(t):raise SyntaxError("Expected )")
    if t[p][0]=='RP':break
    if t[p][0]=='CM':p+=1
    else:raise SyntaxError("Expected , or )")
  p+=1
  if fn in self.b:return self.b[fn](*a),p
  if fn in self.f:return self.cu(fn,a),p
  raise NameError(f"Function '{fn}' not defined")

 def cu(self,fn,a):
  self.k();fu=self.f[fn]
  if len(a)!=len(fu.p):raise TypeError(f"Function '{fn}' expects {len(fu.p)} args, got {len(a)}")
  ov=self.v.copy();self.s.append(ov)
  for p,ar in zip(fu.p,a):self.v[p]=ar
  try:r=self.eb(fu.b)
  except R as ex:r=ex.v
  except(B,C):r=None
  finally:self.v=self.s.pop()if self.s else ov
  return r if r is not None else 0

 def eb(self,bl):
  i=0
  while i<len(bl):
   self.k();l=bl[i].strip()
   if not l or l.startswith('#'):i+=1;continue
   if l.startswith('return '):
    re=l[7:].rstrip(';')
    if re:t=self.tk(re);v,_=self.e(t,0);raise R(v)
    raise R(None)
   elif l.startswith(('if ','for ','while ','thread ','async ')):
    if l.startswith('if '):i=self.eif(bl,i)
    elif l.startswith('for '):i=self.efor(bl,i)
    elif l.startswith('while '):i=self.ewh(bl,i)
    elif l.startswith('thread '):i=self.eth(bl,i)
    elif l.startswith('async '):i=self.eas(bl,i)
    i+=1
   else:self.el(l);i+=1
  return None

 def eth(self,bl,i):
  self.k();tl=bl[i].strip().rstrip(';')
  parts=tl.split()
  if len(parts)<2:raise SyntaxError("Invalid thread syntax")
  fn=parts[1];args=[]
  if len(parts)>2:
   arg_str=' '.join(parts[2:])
   if arg_str:
    t=self.tk(arg_str)
    if t:
     try:args,_=self.e(t,0)
     except:args=[]
    if not isinstance(args,list):args=[args]
  
  self._tc(fn,*args)
  return i

 def eas(self,bl,i):return self.eth(bl,i)

 def pt(self,t):
  self.k()
  if not t:return
  tt=t[0]
  if tt==('K','break'):raise B()
  elif tt==('K','continue'):raise C()
  elif tt==('K','if'):self.pif(t)
  elif tt==('K','func'):self.pfd(t)
  elif tt==('K','for'):self.pfor(t)
  elif tt==('K','while'):self.pwh(t)
  elif len(t)>=3 and t[0][0]=='I'and t[1]==('A','='):
   vn=t[0][1];v,_=self.e(t,2);self.v[vn]=v
  elif len(t)>=5 and t[0][0]=='I'and t[1]==('LB','['):
   vn=t[0][1];ix,p=self.e(t,2)
   if p<len(t)and t[p]==('RB',']')and p+1<len(t)and t[p+1]==('A','='):
    v,_=self.e(t,p+2)
    if vn not in self.v:raise NameError(f"Variable '{vn}' not defined")
    if not isinstance(self.v[vn],list):raise TypeError(f"'{vn}' not list")
    idx=int(ix)
    if idx<0:idx+=len(self.v[vn])
    if 0<=idx<len(self.v[vn]):self.v[vn][idx]=v
    else:raise IndexError("Index out of range")
   else:raise SyntaxError("Invalid list assignment")
  else:self.e(t,0)

 def pfd(self,t):
  if len(t)<4:raise SyntaxError("Invalid function")
  fn=t[1][1]
  if t[2]!=('LP','('):raise SyntaxError("Expected (")
  p,pa=3,[]
  if p<len(t)and t[p]!=('RP',')'):
   while True:
    if p>=len(t)or t[p][0]!='I':raise SyntaxError("Expected param")
    pa.append(t[p][1]);p+=1
    if p>=len(t):raise SyntaxError("Expected )")
    if t[p]==('RP',')'):break
    if t[p]==('CM',','):p+=1
    else:raise SyntaxError("Expected , or )")
  return('func',fn,pa)

 def pif(self,t):
  if len(t)<2:raise SyntaxError("Invalid if")
  co,_=self.e(t,1);return('if',co)

 def pfor(self,t):
  if len(t)<4:raise SyntaxError("Invalid for")
  vn=t[1][1]
  if len(t)<3 or t[2][1]!='in':raise SyntaxError("Expected in")
  it,_=self.e(t,3);return('for',vn,it)

 def pwh(self,t):
  if len(t)<2:raise SyntaxError("Invalid while")
  co,_=self.e(t,1);return('while',co)

 def bs(self,l):
  l=l.strip()
  return l.startswith(('for ','while ','if ','func ','thread ','async '))and not any(l.startswith(x+';')for x in('for','while','if','func','thread','async'))

 def be(self,ls,sl):
  d,cl=1,sl+1
  while cl<len(ls)and d>0:
   l=ls[cl].strip()
   if self.bs(l):d+=1
   elif l=='end;':d-=1
   cl+=1
  if d>0:raise SyntaxError("Missing end")
  return cl-1

 def efb(self,ls,sl):
  fl=ls[sl].strip().rstrip(';')
  t=self.tk(fl);_,fn,pa=self.pfd(t)
  el=self.be(ls,sl);bl=ls[sl+1:el]
  self.f[fn]=F(fn,pa,bl);return el

 def efor(self,ls,sl):
  self.k();fol=ls[sl].strip().rstrip(';')
  t=self.tk(fol);_,vn,it=self.pfor(t)
  el=self.be(ls,sl);hv=vn in self.v;ov=self.v.get(vn)if hv else None
  try:
   if not hasattr(it,'__iter__'):raise TypeError(f"'{type(it).__name__}' object is not iterable")
   for item in it:
    self.k();self.v[vn]=item
    try:self.ebb(ls,sl+1,el)
    except B:break
    except C:continue
  finally:
   if hv:self.v[vn]=ov
   else:self.v.pop(vn,None)
  return el

 def ewh(self,ls,sl):
  self.k();wl=ls[sl].strip().rstrip(';')
  el=self.be(ls,sl)
  while True:
   self.k();t=self.tk(wl);_,co=self.pwh(t)
   if not co:break
   try:self.ebb(ls,sl+1,el)
   except B:break
   except C:continue
  return el

 def eif(self,ls,sl):
  self.k();cl=ls[sl].strip().rstrip(';')
  t=self.tk(cl);co,_=self.e(t,1)
  el=self.be(ls,sl);ell=None
  for i in range(sl+1,el):
   l=ls[i].strip()
   if l in('else','else;'):ell=i;break
  if co:self.ebb(ls,sl+1,ell or el)
  elif ell:self.ebb(ls,ell+1,el)
  return el

 def ebb(self,ls,st,en):
  i=st
  while i<en:
   self.k();l=ls[i].strip()
   if not l or l.startswith('#')or l in('else','else;'):i+=1;continue
   if self.bs(l):
    if l.startswith('for '):i=self.efor(ls,i)
    elif l.startswith('while '):i=self.ewh(ls,i)
    elif l.startswith('if '):i=self.eif(ls,i)
    elif l.startswith('func '):i=self.efb(ls,i)
    elif l.startswith(('thread ','async ')):i=self.eth(ls,i)
    i+=1
   else:self.el(l);i+=1

 def el(self,l):
  self.k();l=l.strip()
  if not l or l.startswith('#'):return
  if not l.endswith(';'):raise SyntaxError(f"Missing ; at end of statement: {l}")
  t=self.tk(l[:-1]);self.pt(t)

 def ex(self,c):
  ls=c.strip().split('\n')
  if ls and ls[0].strip()=='{debug}':
   self.d,self.t,ls=1,time.time(),ls[1:]
  
  ln=0
  while ln<len(ls):
   try:
    self.k();l=ls[ln].strip()
    if not l or l.startswith('#'):ln+=1;continue
    if self.bs(l):
     if l.startswith('func '):ln=self.efb(ls,ln)+1
     elif l.startswith('if '):ln=self.eif(ls,ln)+1
     elif l.startswith('for '):ln=self.efor(ls,ln)+1
     elif l.startswith('while '):ln=self.ewh(ls,ln)+1
     elif l.startswith(('thread ','async ')):ln=self.eth(ls,ln)+1
    elif l in('else','else;','end;'):ln+=1
    else:self.el(l);ln+=1
   except KeyboardInterrupt:
    if self.d and self.t:print(f"\nInterrupted after {time.time()-self.t:.6f}s")
    self.p.shutdown(wait=False);return
   except Exception as e:
    print(f"Error line {ln+1}: {type(e).__name__}: {e}")
    if self.d:import traceback;traceback.print_exc()
    break
  
  if self.d and self.t:print(f"\nCompleted in {time.time()-self.t:.6f}s")
  self.p.shutdown(wait=True)

 def rf(self,fn):
  if not fn.endswith('.blip'):print("Error: Must be .blip");return
  try:
   with open(fn,'r',encoding='utf-8')as f:self.ex(f.read())
  except KeyboardInterrupt:
   if self.d and self.t:print(f"\nInterrupted after {time.time()-self.t:.6f}s")
   self.p.shutdown(wait=False)
  except FileNotFoundError:print(f"Error: File '{fn}' not found")
  except UnicodeDecodeError:print(f"Error: File '{fn}' encoding issue")
  except Exception as e:print(f"Error: {type(e).__name__}: {e}")

def main():
 try:
  i=I()
  if len(sys.argv)>1:i.rf(sys.argv[1])
 except KeyboardInterrupt:print("\nInterrupted")
 except Exception as e:print(f"Fatal error: {type(e).__name__}: {e}")

if __name__=="__main__":main()
