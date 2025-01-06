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
# %config ZMQInteractiveShell.ast_node_interactivity = 'last_expr_or_assign'
# %autoreload 1
# %aimport {{package_name}}

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from IPython.core.display_functions import display

pd.options.display.show_dimensions = True
pd.options.display.width = 120
pd.options.mode.copy_on_write = True
