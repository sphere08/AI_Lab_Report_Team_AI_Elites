import math,csv,time,sys,zipfile,os
zp="gbike.zip";m,n,r,c,p,t,g,k=20,5,10,2,4,10,0.9,20
q=(3.0,4.0);s=(3.0,2.0);f=True;pk=True;d=False

def po(l,x):return math.exp(-l)*(l**x)/math.factorial(x)
def bd(l):
    p=[po(l,i)for i in range(k)]
    p[-1]+=1-sum(p)
    return p
q0=bd(q[0]);q1=bd(q[1]);s0=bd(s[0]);s1=bd(s[1])
st=[(i,j)for i in range(m+1)for j in range(m+1)]
ac=list(range(-n,n+1))

def cl(x):return 0 if x<0 else m if x>m else x

def mc(a):
    if f and a>0:
        e=a-1
        return e*c if e>0 else 0
    return abs(a)*c

def pc(x):return p if pk and x>t else 0

def btr():
    tr={};rw={}
    tot=len(st)
    t0=time.time()
    for idx,(n1,n2) in enumerate(st):
        if d and idx%5==0:
            print(f"bld:{idx}/{tot},t{time.time()-t0:.2f}s")
        fs=[a for a in ac if 0<=n1-a<=m and 0<=n2+a<=m]
        for a in fs:
            a1=n1-a;a2=n2+a
            ic=mc(a)+pc(a1)+pc(a2)
            nsp={}
            er=0.0
            for r0 in range(k):
                pr0=q0[r0]
                for r1 in range(k):
                    pr1=q1[r1];pr=pr0*pr1
                    rent0=min(a1,r0);rent1=min(a2,r1)
                    inc=r*(rent0+rent1)
                    rm0=a1-rent0;rm1=a2-rent1
                    for t0i in range(k):
                        pt0=s0[t0i]
                        for t1i in range(k):
                            pt1=s1[t1i];prob=pr*pt0*pt1
                            nx=(cl(rm0+t0i),cl(rm1+t1i))
                            nsp[nx]=nsp.get(nx,0.0)+prob
                            er+=prob*inc
            ss=sum(nsp.values())
            if ss>0:
                for key in nsp:nsp[key]/=ss
            tr[(n1,n2,a)]=nsp
            rw[(n1,n2,a)]=er-ic
    if d:print("bld done",time.time()-t0)
    return tr,rw

def pi(tr,rw,th=1e-5):
    v={s:0.0 for s in st}
    po={}
    for s in st:
        n1,n2=s
        fs=[a for a in ac if 0<=n1-a<=m and 0<=n2+a<=m]
        po[s]=fs[0]
    def ep():
        while True:
            dlt=0.0
            for s in st:
                a=po[s]
                r=rw[(s[0],s[1],a)]
                q=0.0
                for ns,pr in tr[(s[0],s[1],a)].items():
                    q+=pr*v[ns]
                nv=r+g*q
                dlt=max(dlt,abs(nv-v[s]))
                v[s]=nv
            if dlt<th:break
    def imp():
        ch=False
        for s in st:
            b=None;bv=-1e99
            for a in [x for x in ac if(s[0],s[1],x)in tr]:
                r=rw[(s[0],s[1],a)]
                q=0.0
                for ns,pr in tr[(s[0],s[1],a)].items():
                    q+=pr*v[ns]
                val=r+g*q
                if val>bv:bv=val;b=a
            if b!=po[s]:po[s]=b;ch=True
        return ch
    it=0
    while True:
        ep();it+=1
        if d:print(f"pi iter {it}")
        if not imp():break
    return v,po

def sc(v,po,mn):
    vf=f"gbike_{mn}_value.csv"
    pf=f"gbike_{mn}_policy.csv"
    with open(vf,"w",newline="")as f:
        w=csv.writer(f);w.writerow(["b1\\b2"]+[str(j)for j in range(m+1)])
        for i in range(m+1):
            w.writerow([i]+[f"{v[(i,j)]:.6f}"for j in range(m+1)])
    with open(pf,"w",newline="")as f:
        w=csv.writer(f);w.writerow(["b1\\b2"]+[str(j)for j in range(m+1)])
        for i in range(m+1):
            w.writerow([i]+[str(po[(i,j)])for j in range(m+1)])
    return vf,pf

def rn():
    md=[]
    if f:md.append("free_shuttle")
    if pk:md.append("parking")
    mn="_".join(md)if md else"standard"
    print("mode:",mn,"m:",m,"n:",n,"c:",k)
    if os.path.exists(zp):
        with zipfile.ZipFile(zp,'r')as zf:
            namelist=zf.namelist()
            if f"gbike_{mn}_value.csv" in namelist and f"gbike_{mn}_policy.csv" in namelist:
                print("found in zip,loading...")
                zf.extract(f"gbike_{mn}_value.csv")
                zf.extract(f"gbike_{mn}_policy.csv")
                print("done")
                return
    print("building T/R...")
    tr,rw=btr()
    print("running PI...")
    v,po=pi(tr,rw)
    vf,pf=sc(v,po,mn)
    print("done.value:",vf,"policy:",pf,"zip:",zp)
    print("sample 0..4")
    for i in range(5):
        vals=[f"{v[(i,j)]:6.2f}"for j in range(5)]
        acts=[str(po[(i,j)]).rjust(3)for j in range(5)]
        print("V:"," ".join(vals)," A:"," ".join(acts))
    if os.path.exists(zp):
        with zipfile.ZipFile(zp,'a')as zf:
            zf.write(vf);zf.write(pf)
            print("added to zip")

if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=="debug":
        d=True;m,n,k=4,2,6
        q0=bd(q[0]);q1=bd(q[1]);s0=bd(s[0]);s1=bd(s[1])
        st[:]=[(i,j)for i in range(m+1)for j in range(m+1)]
        tr,rw=btr()
        v,po=pi(tr,rw)
        print("debug done")
        for i in range(m+1):
            vals=[f"{v[(i,j)]:6.2f}"for j in range(m+1)]
            acts=[str(po[(i,j)]).rjust(3)for j in range(m+1)]
            print("V:"," ".join(vals)," A:"," ".join(acts))
    else:rn()
