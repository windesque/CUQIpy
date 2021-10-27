# %%
import sys
sys.path.append("..")
import cuqi
import numpy as np
import matplotlib.pyplot as plt
import scipy
import cuqi.operator
#%%
N = 2
mean = np.zeros(N)
prec = 1.0
dom = 1
BCs = 'neumann'
x = cuqi.distribution.LMRF(mean, prec, N, dom, BCs)
print(x.logpdf(np.array([3,4])))
#%%
location = 0
prec = 1
y = cuqi.distribution.Laplace(location, prec)
print(y.pdf(6))
print(y.pdf(1))
samples = y.sample(1000)

#%%
from scipy.stats import laplace
print(laplace.pdf(6))
print(laplace.pdf(1))

# %%
plt.figure()
samples.plot_chain(1)
#samples.plot()
plt.figure()
#plt.plot(samples.samples,[y.pdf(s) for s in samples.samples], 'o')

plt.hist(samples.samples,bins = 30)
# %%

