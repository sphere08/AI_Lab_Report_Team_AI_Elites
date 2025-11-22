import numpy as np
from math import tanh
def pm(b):return np.where(b==1,1,-1)
def he(p):
    n=p.shape[1]
    w=np.zeros((n,n))
    for x in p:w+=np.outer(x,x)
    np.fill_diagonal(w,0)
    return w
def run_hop(w,s,it=2000):
    a=s.copy()
    for _ in range(it):
        i=np.random.randint(0,len(a))
        a[i]=1 if np.dot(w[i],a)>=0 else -1
    return a
def err_corr():
    n=100
    m=12
    P=np.random.choice([0,1],(m,n))
    Pp=pm(P)
    W=he(Pp)
    res=[]
    for f in range(0,31,2):
        T=100;ok=0
        for _ in range(T):
            i=np.random.randint(0,m)
            t=Pp[i].copy()
            if f>0:
                j=np.random.choice(n,f,replace=False);t[j]*=-1
            r=run_hop(W,t,3000)
            if (r==Pp[i]).all():ok+=1
        res.append((f,ok/T))
    return res
def rook(A=12,B=18,it=15000):
    N=8;n=N*N
    v=np.random.randint(0,2,n).astype(float)
    w=np.zeros((n,n));b=np.zeros(n)
    for i in range(n):
        r=i//N;c=i%N
        for j in range(n):
            if i==j:continue
            rr=j//N;cc=j%N
            if rr==r or cc==c:w[i,j]=-A
    b+=B
    for _ in range(it):
        i=np.random.randint(0,n)
        u=np.dot(w[i],v)+b[i]
        v[i]=1 if u>0.5 else 0
    s=v.reshape(N,N).astype(int)
    return s,s.sum(1),s.sum(0)
def tsp(D,A=500,B=500,C=200,it=4000,dt=0.01):
    N=len(D);n=N*N
    u=np.random.randn(n)
    for _ in range(it):
        U=np.tanh(u)
        for i in range(n):
            c=i//N;p=i%N
            t1=-A*(U[c*N:(c+1)*N].sum()-1)
            t2=-B*(U[p::N].sum()-1)
            t3=0
            for j in range(N):
                if j==c:continue
                nxt=(p+1)%N
                t3-=C*D[c,j]*U[j*N+nxt]
            du=t1+t2+t3-U[i]
            u[i]+=dt*du
    M=np.tanh(u).reshape(N,N)
    sol=np.zeros_like(M)
    for p in range(N):sol[np.argmax(M[:,p]),p]=1
    tour=[int(np.argmax(sol[:,p])) for p in range(N)]
    cost=0
    for p in range(N):
        a=tour[p];b=tour[(p+1)%N];cost+=D[a,b]
    neurons=N*N
    weights=neurons*(neurons-1)//2
    return tour,cost,neurons,weights
def rnd(N):
    x=np.random.rand(N,2)
    return np.sqrt(((x[:,None,:]-x[None,:,:])**2).sum(2))
if __name__=='__main__':
    print("err",err_corr())
    s,r,c=rook()
    print("8rook\n",s)
    print("rows",r,"cols",c)
    D=rnd(10)
    t,cost,nw,wg=tsp(D)
    print("tour",t,"cost",round(cost,3))
    print("neurons",nw,"weights",wg)
