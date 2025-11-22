import random,json,math,sys
def ns(bd):
    return ''.join(str(x) for x in bd)

def rot90(bd):
    m=[6,3,0,7,4,1,8,5,2]
    return tuple(bd[i] for i in m)

def refv(bd):
    m=[2,1,0,5,4,3,8,7,6]
    return tuple(bd[i] for i in m)

def allsym(bd):
    s=[]
    a=tuple(bd)
    for i in range(4):
        s.append(a)
        a=rot90(a)
    a=refv(tuple(bd))
    for i in range(4):
        s.append(a)
        a=rot90(a)
    return s

def canon(bd):
    sy=allsym(bd)
    smin=min(sy)
    return tuple(smin)

def empty_idxs(bd):
    return [i for i,v in enumerate(bd) if v==0]

def init_box(bd,base=4):
    idxs=empty_idxs(bd)
    st=len(idxs)
    mult = max(1, base - (9-st))
    return {i:mult for i in idxs}

def save(bdict,fname):
    with open(fname,'w') as f:
        json.dump(bdict,f)

def load(fname):
    try:
        with open(fname) as f:
            obj=json.load(f)
            return {tuple(int(c) for c in k.split(',')): {int(kk):int(vv) for kk,vv in v.items()} for k,v in obj.items()}
    except Exception:
        return {}

def dump_for_save(bdict):
    return {','.join(map(str,k)):v for k,v in bdict.items()}

def cho(box):
    idxs=list(box.keys())
    weights=[box[i] for i in idxs]
    tot=sum(weights)
    if tot==0:
        return random.choice(idxs)
    pick=random.choices(idxs,weights=weights,k=1)[0]
    return pick

def rein(hist,outcome,bdict,winp=3,drawp=1,lossp=1):
    for st,idx in hist:
        box=bdict.get(st)
        if box is None:
            continue
        if outcome==1:
            box[idx]=box.get(idx,0)+winp
        elif outcome==0:
            box[idx]=box.get(idx,0)+drawp
        else:
            box[idx]=max(1, box.get(idx,1)-lossp)

def play(bdict,train=True,menace_is=1):
    bd=(0,)*9
    player=2
    hist=[]
    while True:
        idxs=empty_idxs(bd)
        if not idxs:
            outcome=0
            if train:
                rein(hist,outcome,bdict)
            return outcome
        if player==menace_is:
            st=canon(bd)
            if st not in bdict:
                bdict[st]=init_box(st)
            box=bdict[st]
            mv=cho(box)
            hist.append((st,mv))
            bd=list(bd)
            bd[mv]=player
            bd=tuple(bd)
        else:
            mv=random.choice(idxs)
            bd=list(bd)
            bd[mv]=player
            bd=tuple(bd)
        w=wincheck(bd)
        if w!=0:
            if w==menace_is:
                outcome=1
            else:
                outcome=-1
            if train:
                rein(hist,outcome,bdict)
            return outcome
        player=1 if player==2 else 2

def wincheck(bd):
    b=list(bd)
    lines=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,bx,c in lines:
        if b[a]!=0 and b[a]==b[bx]==b[c]:
            return b[a]
    return 0

def train(n,bdict,menace_is=1):
    stats={1:0,0:0,-1:0}
    for i in range(n):
        r=play(bdict,train=True,menace_is=menace_is)
        stats[r]+=1
    return stats

def evalt(n,bdict,menace_is=1):
    stats={1:0,0:0,-1:0}
    for i in range(n):
        r=play(bdict,train=False,menace_is=menace_is)
        stats[r]+=1
    return stats

if __name__=='__main__':
    fname='menace_boxes.json'
    bdict=load(fname)
    print('loaded boxes',len(bdict))
    st=train(5000,bdict)
    print('train',st)
    st=evalt(500,bdict)
    print('eval',st)
    save(dump_for_save(bdict),fname)
    print('saved')
