import random
from itertools import combinations

def gen_k_sat(var_count, clause_count, k_val=3, seed_val=None):
    if seed_val is not None:
        random.seed(seed_val)
    cl_list=[]
    for _ in range(clause_count):
        c_vars=random.sample(range(1,var_count+1),k_val)
        clause=[v if random.choice([True,False]) else -v for v in c_vars]
        cl_list.append(clause)
    return cl_list

def eval_solution(sol, cl_list):
    sat=0
    for cl in cl_list:
        if any((lit>0 and sol[lit-1]) or (lit<0 and not sol[-lit-1]) for lit in cl):
            sat+=1
    return sat

def h1(sol, cl_list):
    return eval_solution(sol, cl_list)

def h2(sol, cl_list):
    cnt=0
    for cl in cl_list:
        if any((lit>0 and sol[lit-1]) or (lit<0 and not sol[-lit-1]) for lit in cl):
            cnt+=1+sum(1 for lit in cl if (lit>0 and sol[lit-1]) or (lit<0 and not sol[-lit-1]))
    return cnt

def hill_climb(var_count, cl_list, heuristic):
    curr=[random.choice([True,False]) for _ in range(var_count)]
    curr_score=heuristic(curr, cl_list)
    improved=True
    while improved:
        improved=False
        for i in range(var_count):
            neigh=curr.copy()
            neigh[i]=not neigh[i]
            score=heuristic(neigh, cl_list)
            if score>curr_score:
                curr=neigh
                curr_score=score
                improved=True
                break
    return curr,curr_score

def beam_search(var_count, cl_list, heuristic, width):
    beam=[[random.choice([True,False]) for _ in range(var_count)] for _ in range(width)]
    for _ in range(var_count):
        candidates=[]
        for sol in beam:
            for i in range(var_count):
                neigh=sol.copy()
                neigh[i]=not neigh[i]
                candidates.append(neigh)
        candidates.sort(key=lambda x: heuristic(x, cl_list), reverse=True)
        beam=candidates[:width]
    best=max(beam, key=lambda x: heuristic(x, cl_list))
    return best, heuristic(best, cl_list)

def vnd_search(var_count, cl_list, heuristic):
    curr=[random.choice([True,False]) for _ in range(var_count)]
    neighborhoods=[
        lambda sol: [flip1(sol,i) for i in range(var_count)],
        lambda sol: [flip2(sol,i,j) for i in range(var_count) for j in range(i+1,var_count)],
        lambda sol: [flip3(sol,i,j,k) for i in range(var_count) for j in range(i+1,var_count) for k in range(j+1,var_count)]
    ]
    curr_score=heuristic(curr, cl_list)
    improved=True
    while improved:
        improved=False
        for neigh_func in neighborhoods:
            for neigh in neigh_func(curr):
                score=heuristic(neigh, cl_list)
                if score>curr_score:
                    curr=neigh
                    curr_score=score
                    improved=True
                    break
            if improved:
                break
    return curr,curr_score

def flip1(sol,i):
    neigh=sol.copy()
    neigh[i]=not neigh[i]
    return neigh

def flip2(sol,i,j):
    neigh=sol.copy()
    neigh[i]=not neigh[i]
    neigh[j]=not neigh[j]
    return neigh

def flip3(sol,i,j,k):
    neigh=sol.copy()
    neigh[i]=not neigh[i]
    neigh[j]=not neigh[j]
    neigh[k]=not neigh[k]
    return neigh

if __name__=="__main__":
    n_vals=[20,50]
    m_vals=[60,80]
    ins_per_comb=5
    k_val=3
    for n in n_vals:
        for m in m_vals:
            print(f"\n=== n={n}, m={m} ===")
            res={"HC_h1":[],"HC_h2":[],"BS3_h1":[],"BS4_h1":[],"VND_h1":[]}
            for ins in range(1,ins_per_comb+1):
                clauses=gen_k_sat(n,m,k_val)
                _,score=hill_climb(n,clauses,h1)
                res["HC_h1"].append(score)
                _,score=hill_climb(n,clauses,h2)
                res["HC_h2"].append(score)
                _,score=beam_search(n,clauses,h1,3)
                res["BS3_h1"].append(score)
                _,score=beam_search(n,clauses,h1,4)
                res["BS4_h1"].append(score)
                _,score=vnd_search(n,clauses,h1)
                res["VND_h1"].append(score)
            print("\nAverage Clauses Satisfied:")
            for method,scores in res.items():
                avg=sum(scores)/len(scores)
                print(f"{method}: {avg:.2f}/{m}")
