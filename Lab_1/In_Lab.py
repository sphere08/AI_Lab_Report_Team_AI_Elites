from collections import deque
class lab1:
    def __init__(self,c,m,b,p=None):
        self.c=c
        self.m=m
        self.b=b
        self.p=p

    def is_safe(self):
        if self.m<0 or self.c<0 or self.m>3 or self.c>3:
            return False
        if self.m==0 or self.m==3:
            return True
        return self.m>=self.c
    
    def __eq__(self,o):
        return self.c==o.c and self.m==o.m and self.b==o.b
    
    def __hash__(self):
        return hash((self.c,self.m,self.b))

def bfs():
    s=lab1(3,3,True)
    e=lab1(0,0,False)
    q=deque([s])
    v=set([s])
    while q:
        x=q.popleft()
        if x==e:
            return path(x)
        for n in nxt(x):
            if n not in v:
                v.add(n)
                q.append(n)
    return None

def dfs():
    s=lab1(3,3,True)
    e=lab1(0,0,False)
    st=[s]
    v=set([s])
    while st:
        x=st.pop()
        if x==e:
            return path(x)
        for n in nxt(x):
            if n not in v:
                v.add(n)
                st.append(n)
    return None

def nxt(s):
    ns=[]
    if s.b:
        ns.append(lab1(s.c-2,s.m,not s.b,s))
        ns.append(lab1(s.c-1,s.m-1,not s.b,s))
        ns.append(lab1(s.c,s.m-2,not s.b,s))
        ns.append(lab1(s.c-1,s.m,not s.b,s))
        ns.append(lab1(s.c,s.m-1,not s.b,s))
    else:
        ns.append(lab1(s.c+2,s.m,not s.b,s))
        ns.append(lab1(s.c+1,s.m+1,not s.b,s))
        ns.append(lab1(s.c,s.m+2,not s.b,s))
        ns.append(lab1(s.c+1,s.m,not s.b,s))
        ns.append(lab1(s.c,s.m+1,not s.b,s))
    return [x for x in ns if x.is_safe()]

def path(s):
    p=[]
    while s:
        p.append((s.c,s.m,s.b))
        s=s.p
    p.reverse()
    return p

def compare(b,d):
    if b and d:
        if len(b)<len(d):
            print("\nBFS found the more optimal solution.")
        elif len(d)<len(b):
            print("\nDFS found the more optimal solution.")
        else:
            print("\nBoth BFS and DFS found equally optimal solutions in equal steps.")

b=bfs()
d=dfs()

print("BFS:")
if b:
    for i in b:
        print(i)
else:
    print("No solution")

print("\nDFS:")
if d:
    for i in d:
        print(i)
else:
    print("No solution")

compare(b,d)
