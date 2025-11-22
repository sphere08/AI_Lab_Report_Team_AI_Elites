import random,math,sys
def run(p1,p2,eps,steps):
    q=[0.0,0.0]
    n=[0,0]
    rew=0.0
    for t in range(steps):
        if random.random()<eps:
            a=random.choice([0,1])
        else:
            a=0 if q[0]>=q[1] else 1
        r=1 if random.random()<(p1 if a==0 else p2) else 0
        n[a]+=1
        q[a]+= (r-q[a])/n[a]
        rew+=r
    return {'avg_reward':rew/steps,'q':q,'n':n}

if __name__=='__main__':
    p1=0.7; p2=0.5; eps=0.1; steps=10000
    out=run(p1,p2,eps,steps)
    print('p1,p2,eps,steps=',p1,p2,eps,steps)
    print('avg_reward=',round(out['avg_reward'],4))
    print('final_q=',[round(x,3) for x in out['q']],'n_sel=',out['n'])
