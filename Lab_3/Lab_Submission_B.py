import random

def gen_k_sat(vars_count, clauses_count, clause_len, seed_val=None):
    if seed_val is not None:
        random.seed(seed_val)
    cl_list=[]
    for _ in range(clauses_count):
        c_vars=random.sample(range(1,vars_count+1),clause_len)
        clause=[v if random.choice([True,False]) else -v for v in c_vars]
        cl_list.append(clause)
    return cl_list

def show_ins(clause_len,n_list,ins_each,clauses_per=10):
    ins_num=1
    print(f"Clause length k={clause_len}")
    print(f"Variables n: {', '.join(map(str,n_list))}")
    print(f"Number of clauses m for each ins: {clauses_per}")
    print(f"Ins per n: {ins_each}")
    print("Machine specs: Intel i7-10700K @ 3.8 GHz, 32 GB RAM, Python 3.10")
    print("VI-H Experimental Results\n")
    for n in n_list:
        for _ in range(ins_each):
            seed_val=random.randint(1,100000)
            clauses=gen_k_sat(n,clauses_per,clause_len,seed_val)
            print(f"Ins {ins_num}: k={clause_len}, m={clauses_per}, n={n}, seed={seed_val}")
            for i,cl in enumerate(clauses,start=1):
                print(f"Clause {i}: {cl}")
            print("-"*40)
            ins_num+=1

if __name__=="__main__":
    k=3
    n_vals=[20,50,100]
    ins_per_n=30
    clauses_per_ins=10
    show_ins(k,n_vals,ins_per_n,clauses_per_ins)
