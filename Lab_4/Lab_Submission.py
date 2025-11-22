import numpy as np
import matplotlib.pyplot as plt
import random
import math
import time
from PIL import Image


def read_octave_data(path='scrambled_lena.mat',grid_size=(4,4)):
    with open(path,'r') as fh:
        lines=fh.readlines()

    start_line=0
    for idx,ln in enumerate(lines):
        if not ln.startswith('#'):
            start_line=idx
            break

    dims=[int(x) for x in lines[start_line].split()]

    vals=[]
    for ln in lines[start_line+1:]:
        ln=ln.strip()
        if ln:
            try:
                vals.append(int(ln))
            except:
                continue

    mat=np.array(vals,dtype=np.uint8).reshape(dims[0],dims[1])

    if len(mat.shape)==2:
        mat=np.stack([mat]*3,axis=-1)

    print(f"Loaded data with shape: {mat.shape}")

    r,c=grid_size
    h,w=mat.shape[:2]
    ph=h//r
    pw=w//c

    parts=[]
    for i in range(r):
        for j in range(c):
            block=mat[i*ph:(i+1)*ph,j*pw:(j+1)*pw,:]
            parts.append(block)

    print(f"Generated {len(parts)} segments of {ph}x{pw}")
    return parts,grid_size


def border_error(b1,b2):
    sq=np.sum((b1.astype(np.float32)-b2.astype(np.float32))**2)
    g1=np.gradient(b1.astype(np.float32))
    g2=np.gradient(b2.astype(np.float32))
    gp=sum([np.sum((x-y)**2) for x,y in zip(g1,g2)])
    return sq+0.1*gp


def make_compatibility_map(chunks):
    n=len(chunks)
    maps={'right':np.zeros((n,n)),'down':np.zeros((n,n))}

    print("\nBuilding edge compatibility...")

    for a in range(n):
        for b in range(n):
            if a!=b:
                r1=chunks[a][:,-1,:]
                l2=chunks[b][:,0,:]
                maps['right'][a,b]=-border_error(r1,l2)

                b1=chunks[a][-1,:,:]
                t2=chunks[b][0,:,:]
                maps['down'][a,b]=-border_error(b1,t2)

    print("Compatibility table ready.")
    return maps


def config_energy(grid,shape,maps):
    r,c=shape
    score=0.0

    for i in range(r):
        for j in range(c-1):
            left=grid[i,j]
            right=grid[i,j+1]
            score-=maps['right'][left,right]

    for i in range(r-1):
        for j in range(c):
            up=grid[i,j]
            down=grid[i+1,j]
            score-=maps['down'][up,down]

    return score


def greedy_start(chunks,shape,maps):
    r,c=shape
    n=len(chunks)
    print("\nGreedy layout start...")

    grid=np.full(shape,-1,dtype=int)
    used=set()

    avg=[]
    for k in range(n):
        mean_val=(np.mean(maps['right'][k,:])+np.mean(maps['right'][:,k])+
                  np.mean(maps['down'][k,:])+np.mean(maps['down'][:,k]))/4
        avg.append(mean_val)

    cr,cc=r//2,c//2
    seed=np.argmax(avg)
    grid[cr,cc]=seed
    used.add(seed)

    order=[]
    for rad in range(1,max(r,c)):
        for i in range(max(0,cr-rad),min(r,cr+rad+1)):
            for j in range(max(0,cc-rad),min(c,cc+rad+1)):
                if grid[i,j]==-1:
                    order.append((i,j))

    for x,y in order:
        best=-1
        best_val=-float('inf')

        for cand in range(n):
            if cand in used: continue
            comp=0
            cnt=0

            if y>0 and grid[x,y-1]!=-1:
                comp+=maps['right'][grid[x,y-1],cand];cnt+=1
            if y<c-1 and grid[x,y+1]!=-1:
                comp+=maps['right'][cand,grid[x,y+1]];cnt+=1
            if x>0 and grid[x-1,y]!=-1:
                comp+=maps['down'][grid[x-1,y],cand];cnt+=1
            if x<r-1 and grid[x+1,y]!=-1:
                comp+=maps['down'][cand,grid[x+1,y]];cnt+=1

            if cnt>0: comp/=cnt
            if comp>best_val:
                best_val=comp;best=cand

        if best!=-1:
            grid[x,y]=best
            used.add(best)

    for i in range(r):
        for j in range(c):
            if grid[i,j]==-1:
                for cand in range(n):
                    if cand not in used:
                        grid[i,j]=cand
                        used.add(cand)
                        break

    e=config_energy(grid,shape,maps)
    print(f"Greedy start complete. Energy={e:.2f}")
    return grid


def anneal(chunks,shape,maps,max_iter=200000,trials=5):
    best_layout=None
    best_val=float('inf')

    for t in range(trials):
        print(f"\n{'='*70}\nTRIAL {t+1}/{trials}\n{'='*70}")

        n=len(chunks)
        r,c=shape
        T0=1e7
        Tend=1e-3
        cool=0.99995
        swaps=r*c*3

        if t==0:
            curr=greedy_start(chunks,shape,maps)
        else:
            curr=np.arange(n)
            np.random.shuffle(curr)
            curr=curr.reshape(shape)

        score=config_energy(curr,shape,maps)
        best=np.copy(curr)
        best_s=score

        T=T0
        it=0
        last_up=0
        patience=3000000
        start=time.time()
        print(f"Initial energy={score:.2f}")

        while T>Tend:
            if max_iter and it>=max_iter:
                break

            for _ in range(swaps):
                it+=1
                if T>T0*0.5:
                    pick=random.random()
                    if pick<0.3:
                        x1,y1=random.randint(0,r-1),random.randint(0,c-1)
                        adj=[]
                        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                            a,b=x1+dr,y1+dc
                            if 0<=a<r and 0<=b<c: adj.append((a,b))
                        if adj:
                            x2,y2=random.choice(adj)
                        else:
                            x2,y2=x1,y1
                    elif pick<0.5:
                        row=random.randint(0,r-1)
                        y1,y2=random.sample(range(c),2)
                        x1,x2=row,row
                    elif pick<0.7:
                        col=random.randint(0,c-1)
                        x1,x2=random.sample(range(r),2)
                        y1,y2=col,col
                    else:
                        x1,y1=random.randint(0,r-1),random.randint(0,c-1)
                        x2,y2=random.randint(0,r-1),random.randint(0,c-1)
                else:
                    x1,y1=random.randint(0,r-1),random.randint(0,c-1)
                    adj=[]
                    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
                        a,b=x1+dr,y1+dc
                        if 0<=a<r and 0<=b<c: adj.append((a,b))
                    if adj:
                        x2,y2=random.choice(adj)
                    else:
                        x2,y2=x1,y1

                new=np.copy(curr)
                new[x1,y1],new[x2,y2]=new[x2,y2],new[x1,y1]
                new_score=config_energy(new,shape,maps)
                diff=new_score-score

                if diff<0 or random.random()<math.exp(-diff/T):
                    curr=new
                    score=new_score
                    if score<best_s:
                        best=np.copy(curr)
                        best_s=score
                        last_up=it

            T*=cool
            if it%2000==0:
                print(f"Iter:{it:6d} | Temp:{T:10.2e} | Best:{best_s:12.2f} | "
                      f"Time:{time.time()-start:5.1f}s")
            if it-last_up>patience:
                print(f"No improvement for {patience} steps.")
                break

        print(f"\nTrial {t+1} done: Best={best_s:.2f}")
        if best_s<best_val:
            best_val=best_s
            best_layout=np.copy(best)
            print(f"*** GLOBAL BEST UPDATED: {best_val:.2f} ***")

    return best_layout,best_val


def build_image(layout,chunks,shape):
    r,c=shape
    h,w,ch=chunks[0].shape
    img=np.zeros((r*h,c*w,3),dtype=np.uint8)
    for i in range(r):
        for j in range(c):
            k=layout[i,j]
            img[i*h:(i+1)*h,j*w:(j+1)*w,:]=chunks[k]
    return img


def show_result(chunks,layout,shape):
    scrambled=np.arange(len(chunks)).reshape(shape)
    scrambled_img=build_image(scrambled,chunks,shape)
    solved_img=build_image(layout,chunks,shape)

    fig=plt.figure(figsize=(14,7))
    a1=plt.subplot(1,2,1)
    a1.imshow(scrambled_img)
    a1.set_title("Scrambled (4x4)",fontsize=16,fontweight='bold')
    a1.axis('off')

    a2=plt.subplot(1,2,2)
    a2.imshow(solved_img)
    a2.set_title("Solved Output",fontsize=16,fontweight='bold')
    a2.axis('off')

    plt.tight_layout()
    plt.savefig('result_puzzle.png',dpi=200,bbox_inches='tight')
    print("\nSaved final visualization to 'result_puzzle.png'")

    Image.fromarray(scrambled_img).save('scrambled_view.png')
    Image.fromarray(solved_img).save('solved_view.png')
    print("Images saved: 'scrambled_view.png', 'solved_view.png'")

    plt.show()


if __name__=="__main__":
    random.seed(42)
    np.random.seed(42)

    print("="*70)
    print("JIGSAW PUZZLE SOLVER ENGINE")
    print("="*70)

    pieces,grid=read_octave_data('scrambled_lena.mat',grid_size=(4,4))

    if pieces:
        compat=make_compatibility_map(pieces)
        best_layout,best_energy=anneal(pieces,grid,compat,max_iter=2000000,trials=10)
        show_result(pieces,best_layout,grid)

        print(f"\n{'='*70}\nFINAL OUTPUT\n{'='*70}")
        print(f"Energy={best_energy:.2f}")
        print("Layout:\n",best_layout)
        print("\nInitial order:\n",np.arange(16).reshape(4,4))
    else:
        print("Error reading input data.")
