import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import random

cols=['EC100','EC160','IT101','IT161','MA101','PH100','PH160','HS101','QP']

def ld(fn):
    return pd.read_csv(fn,sep='\t')

def enc(df):
    mp={'AA':0,'AB':1,'BB':2,'BC':3,'CC':4,'CD':5,'DD':6,'F':7}
    for c in cols[:-1]:
        df[c]=df[c].map(mp)
    return df,mp

def cpt(df):
    t={}
    for i in range(len(cols)-2):
        p,c=cols[i],cols[i+1]
        g=df.groupby([p,c]).size()
        g=g.div(df.groupby(p).size(),level=0)
        t[c]=g.unstack(fill_value=0)
    return t

def q_ph(df,mp):
    ev={'EC100':'DD','IT101':'CC','MA101':'CD'}
    ev={k:mp[v] for k,v in ev.items()}
    m=(df['EC100']==ev['EC100'])&(df['IT101']==ev['IT101'])&(df['MA101']==ev['MA101'])
    v=df[m]['PH100'].value_counts(normalize=True)
    rmp={v:k for k,v in mp.items()}
    return rmp[v.idxmax()] if not v.empty else 'BB'

def nb_exp(df,n=20):
    X,y=df[cols[:-1]],df['QP']
    acc=[]
    for _ in range(n):
        rs=random.randint(0,99999)
        Xtr,Xts,ytr,yts=train_test_split(X,y,test_size=0.3,random_state=rs)
        m=MultinomialNB()
        m.fit(Xtr,ytr)
        acc.append(accuracy_score(yts,m.predict(Xts)))
    return float(np.mean(acc)),float(np.std(acc))

def dt_exp(df,n=20):
    X,y=df[cols[:-1]],df['QP']
    acc=[]
    for _ in range(n):
        rs=random.randint(0,99999)
        Xtr,Xts,ytr,yts=train_test_split(X,y,test_size=0.3,random_state=rs)
        m=DecisionTreeClassifier(max_depth=5,random_state=42)
        m.fit(Xtr,ytr)
        acc.append(accuracy_score(yts,m.predict(Xts)))
    return float(np.mean(acc)),float(np.std(acc))

if __name__=='__main__':
    df=ld('2020_bn_nb_data.txt')
    df,mp=enc(df)
    t=cpt(df)
    ph=q_ph(df,mp)
    print('PH100_pred',ph)

    m_nb,s_nb=nb_exp(df,20)
    print('NB_acc_mean',m_nb,'NB_acc_std',s_nb)

    m_dt,s_dt=dt_exp(df,20)
    print('DEP_acc_mean',m_dt,'DEP_acc_std',s_dt)
