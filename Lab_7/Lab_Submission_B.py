import numpy as np,random,json
n_runs=200
n_steps=10000
eps=0.1
alpha=0.1

def trial_one(n_steps,eps,alpha):
    qtrue=np.zeros(10)
    q_sa=np.zeros(10)
    q_c=np.zeros(10)
    n_sa=np.zeros(10)
    rew_sa=np.zeros(n_steps)
    rew_c=np.zeros(n_steps)
    opt_sa=np.zeros(n_steps)
    opt_c=np.zeros(n_steps)
    for t in range(n_steps):
        qtrue+= np.random.normal(0,0.01,10)
        opt_idx=int(np.argmax(qtrue))
        if random.random()<eps:
            a_sa=random.randrange(10)
        else:
            a_sa=int(np.argmax(q_sa))
        r_sa=np.random.normal(qtrue[a_sa],1.0)
        n_sa[a_sa]+=1
        q_sa[a_sa]+= (r_sa-q_sa[a_sa])/n_sa[a_sa]
        rew_sa[t]=r_sa
        opt_sa[t]=1 if a_sa==opt_idx else 0
        if random.random()<eps:
            a_c=random.randrange(10)
        else:
            a_c=int(np.argmax(q_c))
        r_c=np.random.normal(qtrue[a_c],1.0)
        q_c[a_c]+= alpha*(r_c-q_c[a_c])
        rew_c[t]=r_c
        opt_c[t]=1 if a_c==opt_idx else 0
    return rew_sa,opt_sa,rew_c,opt_c

def experiment(n_runs,n_steps,eps,alpha):
    ar_sa=np.zeros(n_steps); ao_sa=np.zeros(n_steps)
    ar_c=np.zeros(n_steps); ao_c=np.zeros(n_steps)
    for i in range(n_runs):
        r_sa,o_sa,r_c,o_c=trial_one(n_steps,eps,alpha)
        ar_sa+=r_sa; ao_sa+=o_sa
        ar_c+=r_c; ao_c+=o_c
    ar_sa/=n_runs; ao_sa/=n_runs
    ar_c/=n_runs; ao_c/=n_runs
    return ar_sa,ao_sa,ar_c,ao_c

if __name__=='__main__':
    ar_sa,ao_sa,ar_c,ao_c=experiment(n_runs,n_steps,eps,alpha)
    out={'ar_sa':ar_sa.tolist(),'ao_sa':ao_sa.tolist(),'ar_c':ar_c.tolist(),'ao_c':ao_c.tolist()}
    with open('bandit_nonstat_out.json','w') as f:
        json.dump(out,f)
    print('saved bandit_nonstat_out.json')
    print('avg reward last 100 steps sa=',np.mean(ar_sa[-100:]),' const-alpha=',np.mean(ar_c[-100:]))
    print('frac optimal last 100 steps sa=',np.mean(ao_sa[-100:]),' const-alpha=',np.mean(ao_c[-100:]))
