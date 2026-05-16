import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

pre = pd.read_csv('_CortexQuest__table_presurvey.csv')
scenarios = pd.read_csv('_CortexQuest__table_scenario_results.csv')

scenarios = scenarios[scenarios['response_time'] > 0]
scenarios['correct_binary'] = (scenarios['is_correct'] == 'Yes').astype(int)

merged = scenarios.merge(pre[['participant_id', 'cyber_training', 'age_group', 'gender']], on='participant_id')

print("CHI-SQUARE TEST")

print("\n1. Cyber Training vs Accuracy")
ct1 = pd.crosstab(merged['cyber_training'], merged['correct_binary'])
chi2, p, dof, expected = chi2_contingency(ct1)
print(ct1)
print(f"Chi2 = {chi2:.3f}, p = {p:.3f}, dof = {dof}")

print("\n2. Gender vs Accuracy")
ct2 = pd.crosstab(merged['gender'], merged['correct_binary'])
chi2_2, p2, dof2, expected2 = chi2_contingency(ct2)
print(ct2)
print(f"Chi2 = {chi2_2:.3f}, p = {p2:.3f}, dof = {dof2}")

print("\n3. Age Group vs Accuracy")
ct3 = pd.crosstab(merged['age_group'], merged['correct_binary'])
chi2_3, p3, dof3, expected3 = chi2_contingency(ct3)
print(ct3)
print(f"Chi2 = {chi2_3:.3f}, p = {p3:.3f}, dof = {dof3}")

