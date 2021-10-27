#%% 
import sys
sys.path.append("..") 
import numpy as np
import scipy.io as spio
import scipy.sparse as sps
from scipy.sparse import diags
import matplotlib.pyplot as plt
import cuqi

%load_ext autoreload
%autoreload 2

# %% Set up Deconvolution test problem
# Parameters for Deconvolution problem
dim = 128
kernel = ["Gauss","Sinc","vonMises"]
phantom = ["Gauss","Sinc","vonMises","Square","Hat","Bumps","DerivGauss"]
noise_type = ["Gaussian","ScaledGaussian"]
noise_std = 0.05

# Test problem
tp = cuqi.testproblem.Deconvolution(
    dim = dim,
    kernel=kernel[0],
    phantom=phantom[3],
    noise_type=noise_type[0],
    noise_std = noise_std
)

#%% Plot exact solution
plt.plot(tp.exactSolution,'.-'); plt.title("Exact solution"); plt.show()

# Plot data
plt.plot(tp.data,'.-'); plt.title("Noisy data"); plt.show()

#%% Set likelihood to be on GaussianCov form
likelihood = cuqi.distribution.GaussianCov(mean = tp.data, cov = noise_std**2)

# %% Lets try with the Gaussian prior
prior_mean = np.zeros(dim)
prior_std = 0.2
prior_cov = sps.diags(prior_std**2 * np.ones(dim)) # TODO: need to convert to array for GaussianCov to work :.toarray() or update GaussianCov to work with sparse array
prior = cuqi.distribution.GaussianCov(mean = prior_mean, cov = prior_cov)

# %% sample prior
prior_samples = prior.sample(1) # issue, GaussianCov does not allow more than one prior sample
fig = plt.figure()
plt.plot(prior_samples)

# %% prior logpdf
prior.logpdf(np.zeros(dim))

#%% Sample posterior with linear_RTO
Ns = 5000
Nb = 1000
x0 = np.zeros(dim)
sampler = cuqi.sampler.Linear_RTO(likelihood, prior, tp.model, tp.data, x0) 
result = sampler.sample(N = Ns, Nb = Nb)

# plot mean + 95% of samples
result.plot_ci(95,exact=tp.exactSolution)

# %% Lets try with Gaussian sqrtprec prior, first identical to above
prior_sqrtprec = sps.diags(1/prior_std*np.ones(dim))
prior = cuqi.distribution.GaussianSqrtPrec(mean = prior_mean, sqrtprec = prior_sqrtprec)

# %% sample prior
prior_samples = prior.sample(5)
fig = plt.figure()
prior_samples.plot()

# %% prior logpdf
prior.logpdf(np.zeros(dim))

#%% sample posterior
sampler = cuqi.sampler.Linear_RTO(likelihood, prior, tp.model, tp.data, x0)
result = sampler.sample(N = Ns, Nb = Nb)

# plot mean + 95% of samples
result.plot_ci(95,exact=tp.exactSolution)

# %% Lets try with Gaussian sqrtprec prior, now with weights
# the true edge positions
dimh = int(np.round(dim/2))
w = int(np.round(dim/15))
# increase prior mean in the center
prior_mean[(dimh-w):(dimh+w)] = 0.6 
# have higher precsion on the outside compared to the center
sqrtprec = 20*np.ones(dim)
sqrtprec[(dimh-w):(dimh+w)] = 2
prior_sqrtprec = sps.diags(sqrtprec, 0)
# setup prior
prior = cuqi.distribution.GaussianSqrtPrec(mean = prior_mean, sqrtprec = prior_sqrtprec)

# %% sample prior
prior_samples = prior.sample(5)
fig = plt.figure()
prior_samples.plot()

#%% sample posterior
sampler = cuqi.sampler.Linear_RTO(likelihood, prior, tp.model, tp.data, x0)
result = sampler.sample(N = Ns, Nb = Nb)

# plot mean + 95% of samples
result.plot_ci(95,exact=tp.exactSolution)

# %% GMRF prior defined using GaussianSqrtPrec

# 1D finite difference matrix with Neumann boundary conditions
one_vec = np.ones(dim)
digs = np.vstack([-one_vec, one_vec])
locs = [0, 1]
D = sps.spdiags(digs, locs, dim, dim, format='csc').todense()
D[-1, -1] = 0

prior_sqrtprec = (1/prior_std)*D
# setup prior
prior = cuqi.distribution.GaussianSqrtPrec(mean = np.zeros(dim), sqrtprec = prior_sqrtprec)

# %% sample prior
prior_samples = prior.sample(5)
fig = plt.figure()
prior_samples.plot()

#%% sample posterior
sampler = cuqi.sampler.Linear_RTO(likelihood, prior, tp.model, tp.data, x0)
result = sampler.sample(N = Ns, Nb = Nb)

# plot mean + 95% of samples
result.plot_ci(95,exact=tp.exactSolution)
# %%
