# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 14:42:57 2025
Statistical analysis of single clogging scenarios: Field vs Simulation 
@author: USER - USING ABNT EVAPORATION CORRECTION
"""

#%% Statistical analysis of single clogging scenarios: Field vs Simulation WITH ABNT EVAPORATION CORRECTION!!!!
import pandas as pd
from scipy import stats

#%%
# Data (NOTE: SCENARIO ZERO IS NOT INCLUDED!!!!)
simulated = [91.93936, 90.84377, 89.78649, 91.26161, 89.20162, 90.85163, 
             89.89068, 88.51781, 91.28081, 88.00479, 91.60651, 85.71138]

field = [88.87393405, 90.28105898, 89.81108208, 89.0730903, 89.74608199, 90.9086958, 
         89.44829605, 88.48454997, 89.14347043, 88.26441074, 91.4081892, 85.75625578]

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
