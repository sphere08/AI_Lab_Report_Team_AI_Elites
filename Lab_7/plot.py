import json, numpy as np, matplotlib.pyplot as plt
d=json.load(open('bandit_nonstat_out.json'))
ar_sa=np.array(d['ar_sa']); ao_sa=np.array(d['ao_sa'])
ar_c=np.array(d['ar_c']); ao_c=np.array(d['ao_c'])
x=np.arange(len(ar_sa))
w=50
def smooth(x,w=50): return np.convolve(x,np.ones(w)/w,mode='same')
plt.figure();
plt.plot(x,smooth(np.cumsum(ar_sa)/(np.arange(1,len(x)+1)),w));
plt.plot(x,smooth(np.cumsum(ar_c)/(np.arange(1,len(x)+1)),w));
plt.legend(['sa','const-alpha']); plt.title('avg reward');
plt.show();
plt.figure();
plt.plot(x,smooth(ao_sa,w));
plt.plot(x,smooth(ao_c,w));
plt.legend(['sa opt','const opt']);
plt.title('% optimal');
plt.show();
