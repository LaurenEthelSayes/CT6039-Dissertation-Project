import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr

pre = pd.read_csv('_CortexQuest__table_presurvey.csv')
post = pd.read_csv('_CortexQuest__table_postsurvey.csv')
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
post['conf_score'] = post['confidence_after'].map(conf_map)

print("CORRELATION ANALYSIS")

print("\n1. Response Time vs Accuracy")
corr, p = pearsonr(scenarios['response_time'], scenarios['correct_binary'])
print(f"   r = {corr:.3f}, p = {p:.3f}")

print("\n2. Response Time vs Score")
corr2, p2 = pearsonr(scenarios['response_time'], scenarios['score_after_action'])
print(f"   r = {corr2:.3f}, p = {p2:.3f}")

print("\n3. Round Number vs Accuracy (does accuracy change as pressure increases)")
corr3, p3 = spearmanr(scenarios['round_number'], scenarios['correct_binary'])
print(f"   r = {corr3:.3f}, p = {p3:.3f}")

print("\n4. Pre Survey Confidence vs Accuracy")
merged = scenarios.merge(pre[['participant_id', 'conf_score']], on='participant_id')
corr4, p4 = pearsonr(merged['conf_score'], merged['correct_binary'])
print(f"   r = {corr4:.3f}, p = {p4:.3f}")

print("\n5. Pre vs Post Confidence")
merged_conf = pre[['participant_id', 'conf_score']].merge(post[['participant_id', 'conf_score']], on='participant_id', suffixes=('_pre', '_post'))
corr5, p5 = pearsonr(merged_conf['conf_score_pre'], merged_conf['conf_score_post'])
print(f"   r = {corr5:.3f}, p = {p5:.3f}")
