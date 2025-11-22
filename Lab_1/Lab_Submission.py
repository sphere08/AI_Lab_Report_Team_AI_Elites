from collections import deque
def make_start(n):
    return 'E'*n+'_'+'W'*n

def make_goal(n):
    return 'W'*n+'_'+'E'*n

def moves(s):
    r=[]
    L=len(s)
    for i,ch in enumerate(s):
        if ch=='E':
            j=i+1
            if j<L and s[j]=='_':
                t=list(s)
                t[i],t[j]=t[j],t[i]
                r.append((''.join(t),f"E {i}->{j}"))
            j=i+2
            if j<L and s[j]=='_' and s[i+1] in ('E','W'):
                t=list(s)
                t[i],t[j]=t[j],t[i]
                r.append((''.join(t),f"E {i}->{j}"))
        elif ch=='W':
            j=i-1
            if j>=0 and s[j]=='_':
                t=list(s)
                t[i],t[j]=t[j],t[i]
                r.append((''.join(t),f"W {i}->{j}"))
            j=i-2
            if j>=0 and s[j]=='_' and s[i-1] in ('E','W'):
                t=list(s)
                t[i],t[j]=t[j],t[i]
                r.append((''.join(t),f"W {i}->{j}"))
    return r

def bfs_path(a,b):
    q=deque([a])
    p={a:None}
    mv={a:""}
    while q:
        x=q.popleft()
        if x==b:
            res=[]
            while x is not None:
                res.append((x,mv[x]))
                x=p[x]
            res.reverse()
            return res
        for nx,m in moves(x):
            if nx not in p:
                p[nx]=x
                mv[nx]=m
                q.append(nx)
    return None

def dfs_path(a,b):
    st=[a]
    p={a:None}
    mv={a:""}
    vis={a}
    while st:
        x=st.pop()
        if x==b:
            res=[]
            while x is not None:
                res.append((x,mv[x]))
                x=p[x]
            res.reverse()
            return res
        for nx,m in moves(x):
            if nx not in vis:
                vis.add(nx)
                p[nx]=x
                mv[nx]=m
                st.append(nx)
    return None

def show_path(p):
    if not p:
        print("No solution")
        return
    print(f"{'Step':>4}  {'State':<30}  Move")
    print("-"*60)
    for i,(s,m) in enumerate(p):
        st=' '.join(s)
        if i==0:
            print(f"{i:>4}  {st:<30}  (start)")
        else:
            print(f"{i:>4}  {st:<30}  {m}")

def solve_game(n=3):
    a=make_start(n)
    b=make_goal(n)
    print(f"Start: {' '.join(a)}")
    print(f"Goal : {' '.join(b)}\n")
    bp=bfs_path(a,b)
    dp=dfs_path(a,b)
    print("\n--- BFS ---")
    show_path(bp)
    print(f"Total moves: {len(bp)-1}")
    print("Optimal: True")
    print("\n--- DFS ---")
    show_path(dp)
    print(f"Total moves: {len(dp)-1}")
    if bp and dp:
        print("Optimal:", len(dp)==len(bp))

if __name__=="__main__":
    solve_game(3)
