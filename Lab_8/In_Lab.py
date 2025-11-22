import numpy as np
w,h=4,3
wl={(1,1)}
tm={(3,2):1.0,(3,1):-1.0}
ac={'U':(0,1),'D':(0,-1),'L':(-1,0),'R':(1,0)}
al=list(ac.keys())
pm,ps=0.8,0.1

def ins(st):
    x,y=st;return 0<=x<w and 0<=y<h and st not in wl

def sp(st,act):
    x,y=st;dx,dy=ac[act];nt=(x+dx,y+dy)
    return st if not ins(nt) else nt

def tr(st,act):
    if st in tm:return {st:1.0}
    if act in ('U','D'):p=('L','R')
    else:p=('U','D')
    d={}
    for a,pb in [(act,pm),(p[0],ps),(p[1],ps)]:
        nt=sp(st,a);d[nt]=d.get(nt,0)+pb
    return d

def rw(st,nt):
    return tm[nt] if nt in tm else r_step

def vi(gm,ep):
    v={(i,j):0 for i in range(w) for j in range(h) if (i,j) not in wl}
    for _ in range(10000):
        df=0;v2=v.copy()
        for st in v:
            if st in tm:
                v2[st]=tm[st];continue
            mx=-1e9
            for act in al:
                qv=0
                for nt,pb in tr(st,act).items():qv+=pb*(rw(st,nt)+gm*v[nt])
                mx=max(mx,qv)
            df=max(df,abs(v2[st]-mx))
            v2[st]=mx
        v=v2
        if df<ep:break
    return v

def pl(v,gm):
    p={}
    for st in v:
        if st in tm:continue
        mx=-1e9;bs=None
        for act in al:
            qv=0
            for nt,pb in tr(st,act).items():qv+=pb*(rw(st,nt)+gm*v[nt])
            if qv>mx:mx=qv;bs=act
        p[st]=bs
    return p

def sh(v,pb):
    for y in range(h-1,-1,-1):
        rw=[]
        for x in range(w):
            st=(x,y)
            if st in wl:rw.append("W")
            elif st in tm:rw.append(f"{tm[st]:.2f}")
            else:rw.append(f"{v[st]:.2f}")
        print(" ".join(rw))
    print()
    for y in range(h-1,-1,-1):
        rw=[]
        for x in range(w):
            st=(x,y)
            if st in wl:rw.append("W")
            elif st in tm:rw.append("T")
            else:rw.append(pb[st])
        print(" ".join(rw))

if __name__=="__main__":
    gm=0.99
    for r_step in [-2,0.1,0.02,1]:
        v=vi(gm,1e-6)
        pb=pl(v,gm)
        print("\n====== r =",r_step,"======")
        sh(v,pb)
