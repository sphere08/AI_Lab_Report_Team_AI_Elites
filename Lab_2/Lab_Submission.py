import heapq
import re
import nltk
from nltk.tokenize import sent_tokenize
from zipfile import ZipFile
import os


try:nltk.data.find('tokenizers/punkt')
except LookupError:nltk.download('punkt')


def proc_text(txt):
    raw=sent_tokenize(txt)
    res=[]
    for s in raw:
        s=s.strip()
        if not s:continue
        s=s.lower()
        s=re.sub(r'[^\w\s]','',s).strip()
        if s:res.append(s)
    return res


def calc_dist(a,b):
    m,n=len(a),len(b)
    d=[[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1):d[i][0]=i
    for j in range(n+1):d[0][j]=j
    for i in range(1,m+1):
        for j in range(1,n+1):
            if a[i-1]==b[j-1]:d[i][j]=d[i-1][j-1]
            else:d[i][j]=1+min(d[i-1][j],d[i][j-1],d[i-1][j-1])
    return d[m][n]


def h_func(d1,d2,i,j):
    r1=len(d1)-i
    r2=len(d2)-j
    return abs(r1-r2)


def find_align(d1,d2):
    st=(0,0)
    en=(len(d1),len(d2))
    gv={st:0}
    pm={}
    def f_val(x,y):return gv.get((x,y),float('inf'))+h_func(d1,d2,x,y)
    q=[]
    heapq.heappush(q,(f_val(0,0),0,0))
    vis=set()
    while q:
        _,i,j=heapq.heappop(q)
        if (i,j) in vis:continue
        vis.add((i,j))
        if (i,j)==en:
            tot=gv[(i,j)]
            aln=0
            skp=0
            cur=(i,j)
            while cur in pm:
                pi,pj,op=pm[cur]
                if op=='m':aln+=1
                elif op in('s1','s2'):skp+=1
                cur=(pi,pj)
            return tot,aln,skp
        if i<len(d1) and j<len(d2):
            c=calc_dist(d1[i],d2[j])
            ni,nj=i+1,j+1
            nc=gv[(i,j)]+c
            if nc<gv.get((ni,nj),float('inf')):
                gv[(ni,nj)]=nc
                pm[(ni,nj)]=(i,j,'m')
                heapq.heappush(q,(nc+h_func(d1,d2,ni,nj),ni,nj))
        if i<len(d1):
            ni,nj=i+1,j
            nc=gv[(i,j)]+1
            if nc<gv.get((ni,nj),float('inf')):
                gv[(ni,nj)]=nc
                pm[(ni,nj)]=(i,j,'s1')
                heapq.heappush(q,(nc+h_func(d1,d2,ni,nj),ni,nj))
        if j<len(d2):
            ni,nj=i,j+1
            nc=gv[(i,j)]+1
            if nc<gv.get((ni,nj),float('inf')):
                gv[(ni,nj)]=nc
                pm[(ni,nj)]=(i,j,'s2')
                heapq.heappush(q,(nc+h_func(d1,d2,ni,nj),ni,nj))
    return float('inf'),0,0


def chk_plag(t1,t2):
    s1=proc_text(t1)
    s2=proc_text(t2)
    if not s1 or not s2:
        return {'cost':0.0,'aligned':0,'skipped':0,'result':'No plagiarism','doc1_count':len(s1),'doc2_count':len(s2)}
    tot,aln,skp=find_align(s1,s2)
    mx=max(len(s1),len(s2))
    rt=aln/mx if mx>0 else 0
    avg=tot/aln if aln>0 else float('inf')
    sc=rt*(1/(1+avg))
    if sc>0.5 and rt>0.7:res='Plagiarism detected'
    elif sc>0.3 and rt>0.5:res='Possible plagiarism'
    else:res='No plagiarism'
    return {'cost':float(tot),'aligned':int(aln),'skipped':int(skp),'result':res,'doc1_count':len(s1),'doc2_count':len(s2)}


folder=""
pairs=[("doc1_1.txt","doc2_1.txt"),
       ("doc1_2.txt","doc2_2.txt"),
       ("doc1_3.txt","doc2_3.txt"),
       ("doc1_4.txt","doc2_4.txt")]


COL1=22;COL2=12;COL3=14;COL4=18;COL5=28
def print_header():
    hdr=(f"{'Doc Pair':{COL1}}  {'Cost':{COL2}}  {'Aligned':{COL3}}  {'Skipped':{COL4}}  {'Detection':{COL5}}")
    print('\n'+hdr)
    print('-'*(COL1+COL2+COL3+COL4+COL5+8))
def print_row(name,r):
    print(f"{name:{COL1}}  {r['cost']:{COL2}.1f}  {r['aligned']:{COL3}}  {r['skipped']:{COL4}}  {r['result']:{COL5}}")


print_header()
for doc1,doc2 in pairs:
    path1=os.path.join(folder,doc1)
    path2=os.path.join(folder,doc2)
    with open(path1,'r') as f1, open(path2,'r') as f2:
        text1=f1.read()
        text2=f2.read()
    result=chk_plag(text1,text2)
    pair_name=f"{doc1} vs {doc2}"
    print_row(pair_name,result)
