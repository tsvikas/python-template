# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload

# %%
# %config ZMQ.??? = 'last_expr_or_assign'
# %autoreload 1
# %aimport titanic

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from IPython.core.display_functions import display
pd.options.core = ...
