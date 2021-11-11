# %%
import sys
sys.path.append("..")
from cuqi.geometry import StepExpansion, MappedGeometry
import numpy as np
import matplotlib.pyplot as plt

%load_ext autoreload
%autoreload 2

# %% Values to plot
vals = np.array([3,5,2])
# %% Regular step geometry
geom = StepExpansion(np.linspace(0,1,10))
# %%
geom.plot(vals)
# %% mapped step geometry
mapped_geom = MappedGeometry(geom,lambda x: np.exp(x))
mapped_geom
#%%
mapped_geom.plot(vals)
