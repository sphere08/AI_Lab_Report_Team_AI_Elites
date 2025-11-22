import numpy as np
from math import exp
def sgm(v):return 1/(1+exp(-v))
def pb(b):return np.where(b==1,1,-1)
def hb(p):
    n=p.shape[1]
    w=np.zeros((n,n))
    for r in p:w+=np.outer(r,r)
    np.fill_diagonal(w,0)
    return w/p.shape[0]
def upd(w,s,it=1000):
    n=len(s)
    a=s.copy()
    for _ in range(it):
        i=np.random.randint(0,n)
        u=np.dot(w[i],a)
        a[i]=1 if u>=0 else -1
    return a
def make_p(m,n):
    return np.random.choice([0,1],(m,n))
def cap_test():
    n=100
    out=[]
    for m in range(1,26):
        p=make_p(m,n)
        pp=pb(p)
        w=hb(pp)
        ok=0
        for i in range(m):
            t=pp[i].copy()
            f=int(0.1*n)
            idx=np.random.choice(n,f,replace=False)
            t[idx]*=-1
            r=upd(w,t,500)
            if (r==pp[i]).all():ok+=1
        out.append((m,ok/m))
    return out
def store_demo():
    n=100
    p=13
    X=make_p(p,n)
    W=hb(pb(X))
    a=pb(X[0]).copy()
    idx=np.random.choice(n,8,replace=False)
    a[idx]*=-1
    r=upd(W,a,2000)
    return X,W,r
if __name__=='__main__':
    print("cap",cap_test())
    X,W,r=store_demo()
    print("recov ok", (r==pb(X[0])).all())
    N=100
    print("N",N,"theoretical~",int(0.138*N))
