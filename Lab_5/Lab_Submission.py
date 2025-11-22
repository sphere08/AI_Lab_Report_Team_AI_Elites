import yfinance as yf
import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
import matplotlib.pyplot as plt

def an(t='AAPL', s='2014-01-01', e='2024-01-01', n=2):
    d = yf.download(t, start=s, end=e, auto_adjust=False)
    p = d['Adj Close']
    r = p.pct_change().dropna().values.reshape(-1, 1)
    h = GaussianHMM(n_components=n, covariance_type='full', random_state=42)
    h.fit(r)
    st = h.predict(r)
    m = h.means_
    c = h.covars_
    tr = h.transmat_
    fig, ax = plt.subplots(3, 1, figsize=(14, 10))
    ax[0].plot(p.index, p)
    ax[0].set_title(t + '_Price')
    ax[1].plot(p.index[1:], r)
    ax[1].set_title('Returns')
    cl = ['green', 'red', 'blue', 'yellow']
    for i in range(n):
        ax[2].plot(p.index[1:][st == i], p[1:][st == i], '.', color=cl[i])
    ax[2].set_title('States')
    plt.tight_layout()
    plt.show()
    for i in range(n):
        print('S' + str(i) + '_mean', m[i][0], 'S' + str(i) + '_var', c[i][0][0])
    print('Trans_matrix\n', tr)
    print('Model_score', h.score(r))
    print('Next_state_prob', tr[st[-1]])

if __name__ == '__main__':
    an()
