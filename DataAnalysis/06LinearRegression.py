import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

pre = pd.read_csv('_CortexQuest__table_presurvey.csv')
scenarios = pd.read_csv('_CortexQuest__table_scenario_results.csv')

scenarios = scenarios[scenarios['response_time'] > 0]
scenarios['correct_binary'] = (scenarios['is_correct'] == 'Yes').astype(int)

conf_map = {
    'Not confident at all': 1,
    'Slightly confident': 2,
    'Moderately confident': 3,
    'Very confident': 4,
    'Extremely confident': 5
}

pre['conf_score'] = pre['suspicious_confidence'].map(conf_map)
pre['trained'] = (pre['cyber_training'] == 'Yes, formal training').astype(int)

merged = scenarios.merge(pre[['participant_id', 'conf_score', 'trained']], on='participant_id')

print("LINEAR REGRESSION")
print("Predicting accuracy from confidence, training and response time")

model = smf.ols('correct_binary ~ conf_score + trained + response_time', data=merged).fit()

print(f"\nR-squared: {model.rsquared:.3f}")
print(f"Adjusted R-squared: {model.rsquared_adj:.3f}")
print(f"F-statistic p-value: {model.f_pvalue:.3f}")

print("\nCoefficients:")
print(model.params.round(3))

print("\nP-values:")
print(model.pvalues.round(3))

