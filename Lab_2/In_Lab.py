import time
import psutil

class Board:
    def __init__(self,start,goal):
        self.start=start
        self.goal=goal

    def find_zero(self,state):
        for r in range(3):
            for c in range(3):
                if state[r][c]==0:
                    return r,c

    def get_next(self,state):
        next_states=[]
        r,c=self.find_zero(state)
        moves=[(0,1),(1,0),(0,-1),(-1,0)]
        for dr,dc in moves:
            nr,nc=r+dr,c+dc
            if 0<=nr<3 and 0<=nc<3:
                temp=[row.copy() for row in state]
                temp[r][c],temp[nr][nc]=temp[nr][nc],temp[r][c]
                next_states.append(temp)
        return next_states

    def is_goal(self,state):
        return state==self.goal

    def dls(self,state,limit):
        if self.is_goal(state):
            return "found",0
        if limit==0:
            return "stop",0
        count=0
        for nxt in self.get_next(state):
            res,n=self.dls(nxt,limit-1)
            count+=n
            if res=="found":
                return "found",count
        return "stop",count

    def ids(self):
        depth=0
        data=[]
        mem_total=0
        while True:
            t1=time.time()
            m1=psutil.virtual_memory().used/(1024**2)
            res,_=self.dls(self.start,depth)
            t2=time.time()
            m2=psutil.virtual_memory().used/(1024**2)
            dt=t2-t1
            dm=max(0,m2-m1)
            mem_total+=dm
            data.append([depth,dt,mem_total])
            if res=="found":
                return data
            elif res=="stop":
                depth+=1
            else:
                return data

def gen_states(grid,n):
    states=set()
    make_states(grid,n,[],states)
    return states

def make_states(grid,n,path,states):
    if n==0:
        states.add(tuple(map(tuple,grid)))
        return
    opts=get_moves(grid)
    for opt in opts:
        new=[row.copy() for row in grid]
        apply_move(new,opt)
        make_states(new,n-1,path+[opt],states)

def get_moves(grid):
    zero=[(r,row.index(0)) for r,row in enumerate(grid) if 0 in row][0]
    opts=[]
    if zero[1]>0:
        opts.append('l')
    if zero[1]<2:
        opts.append('r')
    if zero[0]>0:
        opts.append('u')
    if zero[0]<2:
        opts.append('d')
    return opts

def apply_move(grid,move):
    zero=[(r,row.index(0)) for r,row in enumerate(grid) if 0 in row][0]
    r,c=zero
    if move=='l':
        grid[r][c],grid[r][c-1]=grid[r][c-1],grid[r][c]
    elif move=='r':
        grid[r][c],grid[r][c+1]=grid[r][c+1],grid[r][c]
    elif move=='u':
        grid[r][c],grid[r-1][c]=grid[r-1][c],grid[r][c]
    elif move=='d':
        grid[r][c],grid[r+1][c]=grid[r+1][c],grid[r][c]

def show_all(start,states):
    print("Start:")
    for row in start:
        print(row)
    print()
    for i,s in enumerate(states,1):
        print(f"State {i}:")
        for row in s:
            print(row)
        print()

def show(grid):
    for row in grid:
        print(" ".join(map(str,row)))
    print()

class Solver:
    def __init__(self,start,goal):
        self.start=start
        self.goal=goal

    def show(self,state):
        for row in state:
            print(" ".join(map(str,row)))
        print()

    def find_zero(self,state):
        for r in range(3):
            for c in range(3):
                if state[r][c]==0:
                    return r,c

    def get_next(self,state):
        next_states=[]
        r,c=self.find_zero(state)
        moves=[(0,1),(1,0),(0,-1),(-1,0)]
        for dr,dc in moves:
            nr,nc=r+dr,c+dc
            if 0<=nr<3 and 0<=nc<3:
                temp=[row.copy() for row in state]
                temp[r][c],temp[nr][nc]=temp[nr][nc],temp[r][c]
                next_states.append(temp)
        return next_states

    def is_goal(self,state):
        return state==self.goal

    def run(self):
        depth=0
        while True:
            res=self.dls(self.start,depth)
            if res=="found":
                print("Done!")
                return
            elif res=="stop":
                print(f"Depth {depth} done, going deeper...")
                depth+=1
            else:
                print("No solution.")
                return

    def dls(self,state,limit):
        if self.is_goal(state):
            self.show(state)
            return "found"
        if limit==0:
            return "stop"
        hit_limit=False
        for nxt in self.get_next(state):
            res=self.dls(nxt,limit-1)
            if res=="found":
                self.show(state)
                return "found"
            elif res=="stop":
                hit_limit=True
        return "stop" if hit_limit else "fail"

if __name__=="__main__":
    goal1=[[1,0,3],[4,2,6],[7,5,8]]
    start1=[[1,2,3],[4,5,6],[7,8,0]]
    s1=Solver(start1,goal1)
    s1.run()

    print("\n"+"="*50+"\n")

    start2=[[4,2,3],[0,1,6],[5,7,8]]
    n=2
    states=gen_states(start2,n)
    show_all(start2,states)

    print("\n"+"="*50+"\n")

    start3=[[4,2,3],[0,1,6],[5,7,8]]
    goal3=[[1,2,3],[4,5,6],[7,8,0]]
    b=Board(start3,goal3)
    results=b.ids()
    print("\nDepth\tTime\tMemory")
    for row in results:
        print("\t".join(map(str,row)))
