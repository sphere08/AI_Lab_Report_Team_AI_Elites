import random, math, numpy as np, time, os
from pathlib import Path

class SA:
    def __init__(self, pts, labs, T=1000.0, cool=0.995, lim=10000):
        self.pts=[tuple(p) for p in pts]
        self.labs=list(labs)
        self.n=len(self.pts)
        self.T=T
        self.cool=cool
        self.lim=lim
        self.cur=list(range(self.n))
        random.shuffle(self.cur)
        self.curcost=self._f(self.cur)
        self.best=list(self.cur)
        self.bestc=self.curcost
        self.k=0
        self.hist=[]
        self.time=0.0

    def _f(self,perm):
        s=0.0
        for i in range(self.n):
            a=self.pts[perm[i]]
            b=self.pts[perm[(i+1)%self.n]]
            s+=math.hypot(a[0]-b[0],a[1]-b[1])
        return s

    def _swap(self,p):
        i=random.randrange(self.n)
        j=random.randrange(self.n)
        if i>j:i,j=j,i
        q=p[:]
        q[i:j+1]=reversed(q[i:j+1])
        return q

    def run(self):
        T=self.T
        k=0
        st=time.time()
        while k<self.lim and T>1e-9:
            nxt=self._swap(self.cur)
            cost=self._f(nxt)
            d=cost-self.curcost
            if d<0 or random.random()<math.exp(-d/T):
                self.cur=nxt
                self.curcost=cost
                if cost<self.bestc:
                    self.bestc=cost
                    self.best=list(nxt)
            self.hist.append(self.curcost)
            T*=self.cool
            k+=1
        self.k=k
        self.time=time.time()-st
        return self.best,self.bestc

    def showpath(self):
        print("Best cost:",self.bestc)
        for i in self.best:
            print(self.labs[i],end=' -> ')
        print(self.labs[self.best[0]])

    def plotcurve(self):
        try:
            import matplotlib.pyplot as plt
        except:
            print('matplotlib missing')
            return
        plt.plot(self.hist)
        plt.xlabel('Iter')
        plt.ylabel('Cost')
        plt.title('SA Curve')
        plt.show()


def readfile(f):
    p=Path(f)
    if not p.is_absolute() and not p.exists():
        r=Path(__file__).resolve().parent
        q=r/p
        if q.exists():p=q
    if not p.exists():raise FileNotFoundError(f"Missing file: {f}")
    f=open(p,'r')
    line=f.readline().strip().split()
    print("File Name:",line[2])
    while line[0]!='NODE_COORD_SECTION':
        if line[0]=='DIMENSION':dim=line[2]
        line=f.readline().strip().split()
    pts=[]
    names=[]
    print('Dimension',dim)
    N=int(dim)
    for _ in range(N):
        x,y,z=f.readline().strip().split()[:]
        pts.append([float(y),float(z)])
        names.append(x)
    f.close()
    return pts,names


def compare():
    root=Path(__file__).resolve().parent/'Data'
    files=['rajasthan.tsp','bcl380.tsp','pbk411.tsp','pbl395.tsp','pka379.tsp']
    out=[]
    for f in files:
        path=root/f
        try:
            nodes,names=readfile(path)
        except Exception as e:
            print(f"Fail {f}: {e}")
            continue
        if 'rajasthan' in f.lower():
            print('\nRajasthan locations:')
            for i,n in enumerate(names,1):print(f"{i:2d}. {n}")
        pts=np.array(nodes)
        n=len(pts)
        it=min(50000,max(5000,n*200))
        sa=SA(pts,names,lim=it)
        sa.run()
        if 'rajasthan' in f.lower():
            print('\nBest route:')
            for i in sa.best:print('-',names[i])
            print(f"Cost: {sa.bestc:.6f}\n")
        out.append((f,sa.k,sa.time,sa.k,sa.bestc))
    c1,c2,c3,c4,c5=28,10,12,16,14
    hdr=(f"{'Dataset':{c1}}  {'Steps':{c2}}  {'Runtime(s)':{c3}}  {'Memory(est)':{c4}}  {'BestCost':{c5}}")
    print('\nResults:')
    print(hdr)
    print('-'*(c1+c2+c3+c4+c5+8))
    for f,a,b,c,d in out:
        print(f"{f:{c1}}  {a:{c2}}  {b:{c3}.2f}  {c:{c4}}  {d:{c5}.6f}")
    if out:
        best=min(out,key=lambda x:x[4])
        print('\nLowest cost:')
        print(f" Dataset: {best[0]}\n Steps: {best[1]}\n Runtime(s): {best[2]:.2f}\n EstMem: {best[3]}\n BestCost: {best[4]:.6f}")


def main():
    compare()

if __name__=='__main__':
    main()
