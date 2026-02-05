# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 21:35:17 2025

@author: USER
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 14:42:57 2025
Statistical analysis of single clogging scenarios: Field vs Simulation
@author: WITHOUT ABNT EVAPORATION CORRECTION
"""

#%% Statistical analysis of single clogging scenarios: Field vs Simulation WITHOUT ABNT EVAPORATION CORRECTION!!!!
import pandas as pd
from scipy import stats

#%%
# Data (NOTE: SCENARIO ZERO IS NOT INCLUDED!!!!)
simulated = [91.03003, 89.7116, 88.73289, 89.21847, 86.5776, 87.41009, 
             87.39313, 84.19931, 87.47308, 83.00757, 85.87817, 80.82867]

field = [84.41144864, 88.51368668, 88.70680875, 85.54094196, 87.34959904, 88.46052484, 
         87.85087683, 85.93634023, 86.82239121, 84.74328852, 87.82635507, 82.05307216]

# Normality test (Shapiro-Wilk)
norm_sim = stats.shapiro(simulated).pvalue
norm_field = stats.shapiro(field).pvalue

print("Normality Simulated (p):", norm_sim)
print("Normality Field (p):", norm_field)

# Choose test based on normality
if norm_sim > 0.05 and norm_field > 0.05:
    print("\nData appear normal → using Paired t-test")
    t_test = stats.ttest_rel(simulated, field)
    pval = t_test.pvalue
    print("p-value of paired t-test:", pval)
    if pval < 0.05:
        print("➡ There is a significant difference between Simulated and Field.")
    else:
        print("➡ There is NO significant difference between Simulated and Field.")
else:
    print("\nData do not follow normal distribution → using Wilcoxon test")
    wilcoxon_test = stats.wilcoxon(simulated, field)
    pval = wilcoxon_test.pvalue
    print("p-value of Wilcoxon test:", pval)
    if pval < 0.05:
        print("➡ There is a significant difference between Simulated and Field.")
    else:
        print("➡ There is NO significant difference between Simulated and Field.")