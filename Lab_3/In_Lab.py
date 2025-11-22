import heapq
from copy import deepcopy
import time
import csv
import os

init_b=[[-1,-1,1,1,1,-1,-1],[-1,-1,1,1,1,-1,-1],[1,1,1,1,1,1,1],[1,1,1,0,1,1,1],[1,1,1,1,1,1,1],[-1,-1,1,1,1,-1,-1],[-1,-1,1,1,1,-1,-1]]
goal_b=[[-1,-1,0,0,0,-1,-1],[-1,-1,0,0,0,-1,-1],[0,0,0,0,0,0,0],[0,0,0,1,0,0,0],[0,0,0,0,0,0,0],[-1,-1,0,0,0,-1,-1],[-1,-1,0,0,0,-1,-1]]
dirs=[(-2,0),(2,0),(0,-2),(0,2)]

def b2t(b):return tuple(tuple(r) for r in b)
def goal(b):return sum(r.count(1) for r in b)==1 and b[3][3]==1

def moves(b):
    res=[]
    for i in range(7):
        for j in range(7):
            if b[i][j]==1:
                for dx,dy in dirs:
                    x,y=i+dx,j+dy
                    mx,my=i+dx//2,j+dy//2
                    if 0<=x<7 and 0<=y<7 and b[x][y]==0 and b[mx][my]==1:
                        nb=deepcopy(b)
                        nb[i][j]=0
                        nb[mx][my]=0
                        nb[x][y]=1
                        res.append(nb)
    return res

def h1(b):return sum(r.count(1) for r in b)-1
def h2(b):return sum(abs(i-3)+abs(j-3) for i in range(7) for j in range(7) if b[i][j]==1)

def bfs1(start,h,time_limit=5.0,node_limit=200000):
    st=time.perf_counter()
    seen=set()
    heap=[(h(start),start,[])]
    exp=0
    mx=1
    while heap:
        if time.perf_counter()-st>time_limit or exp>=node_limit:
            return None,{'runtime':time.perf_counter()-st,'nodes':exp,'mem':mx,'timeout':True}
        mx=max(mx,len(heap)+len(seen))
        _,b,path=heapq.heappop(heap)
        exp+=1
        tb=b2t(b)
        if tb in seen:continue
        seen.add(tb)
        if goal(b):return path+[b],{'runtime':time.perf_counter()-st,'nodes':exp,'mem':mx}
        for nb in moves(b):
            heapq.heappush(heap,(h(nb),nb,path+[b]))
    return None,{'runtime':time.perf_counter()-st,'nodes':exp,'mem':mx,'timeout':False}

def astar(start,h,time_limit=5.0,node_limit=200000):
    st=time.perf_counter()
    seen=set()
    heap=[(h(start),0,start,[])]
    exp=0
    mx=1
    while heap:
        if time.perf_counter()-st>time_limit or exp>=node_limit:
            return None,{'runtime':time.perf_counter()-st,'nodes':exp,'mem':mx,'timeout':True}
        mx=max(mx,len(heap)+len(seen))
        f,g,b,path=heapq.heappop(heap)
        exp+=1
        tb=b2t(b)
        if tb in seen:continue
        seen.add(tb)
        if goal(b):return path+[b],{'runtime':time.perf_counter()-st,'nodes':exp,'mem':mx}
        for nb in moves(b):
            ng=g+1
            nf=ng+h(nb)
            heapq.heappush(heap,(nf,ng,nb,path+[b]))
    return None,{'runtime':time.perf_counter()-st,'nodes':exp,'mem':mx,'timeout':False}

def runexp():
    res=[]
    tlim=2.0
    nlim=200000
    algs=[("Uniform Cost Search",lambda b:0,astar),("Best-First (Heuristic 1)",h1,bfs1),("Best-First (Heuristic 2)",h2,bfs1),("A* (Heuristic 1)",h1,astar),("A* (Heuristic 2)",h2,astar)]
    for name,h,sf in algs:
        print(f"Running {name}...")
        path,st=sf(init_b,h,time_limit=tlim,node_limit=nlim)
        steps=len(path)-1 if path else 0
        to=bool(st.get('timeout',False))
        res.append((name,steps,st['runtime'],st['mem'],to))
    fp=os.path.join(os.path.dirname(__file__),'experiments_results.csv')
    with open(fp,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['Algo','Steps','Runtime_s','MemNodes','Timeout'])
        for n,s,r,m,t in res:w.writerow([n,s,f"{r:.6f}",m,t])
    print(f"Experiments completed. Results saved to {fp}")
    return fp

if __name__=="__main__":runexp()
