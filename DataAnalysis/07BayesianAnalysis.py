import pandas as pd
import numpy as np
from scipy import stats

scenarios = pd.read_csv('_CortexQuest__table_scenario_results.csv')
pre = pd.read_csv('_CortexQuest__table_presurvey.csv')

scenarios = scenarios[scenarios['response_time'] > 0]
scenarios['correct_binary'] = (scenarios['is_correct'] == 'Yes').astype(int)
scenarios['fooled'] = 1 - scenarios['correct_binary']

print("BAYESIAN ANALYSIS")
print("Estimating the probability of being fooled by each cue type")
print("Using Beta distribution with uninformed prior (alpha=1, beta=1)")

prior_alpha = 1
prior_beta = 1

cue_stats = scenarios.groupby('cue_type').agg(
    total=('fooled', 'count'),
    fooled=('fooled', 'sum')
).reset_index()

cue_stats['posterior_alpha'] = prior_alpha + cue_stats['fooled']
cue_stats['posterior_beta'] = prior_beta + (cue_stats['total'] - cue_stats['fooled'])
cue_stats['posterior_mean'] = cue_stats['posterior_alpha'] / (cue_stats['posterior_alpha'] + cue_stats['posterior_beta'])
cue_stats['ci_lower'] = stats.beta.ppf(0.025, cue_stats['posterior_alpha'], cue_stats['posterior_beta'])
cue_stats['ci_upper'] = stats.beta.ppf(0.975, cue_stats['posterior_alpha'], cue_stats['posterior_beta'])

print("\nProbability of being fooled by cue type:")
print(f"{'Cue Type':<35} {'P(Fooled)':<12} {'95% CI'}")
print("-" * 65)
for _, row in cue_stats.iterrows():
    print(f"{row['cue_type']:<35} {row['posterior_mean']:.3f}        [{row['ci_lower']:.3f} - {row['ci_upper']:.3f}]")

print("\nBYESIAN ANALYSIS BY ROUND")
print("Estimating the probability of being fooled per round")

round_stats = scenarios.groupby('round_number').agg(
    total=('fooled', 'count'),
    fooled=('fooled', 'sum')
).reset_index()

round_stats['posterior_alpha'] = prior_alpha + round_stats['fooled']
round_stats['posterior_beta'] = prior_beta + (round_stats['total'] - round_stats['fooled'])
round_stats['posterior_mean'] = round_stats['posterior_alpha'] / (round_stats['posterior_alpha'] + round_stats['posterior_beta'])
round_stats['ci_lower'] = stats.beta.ppf(0.025, round_stats['posterior_alpha'], round_stats['posterior_beta'])
round_stats['ci_upper'] = stats.beta.ppf(0.975, round_stats['posterior_alpha'], round_stats['posterior_beta'])

print(f"\n{'Round':<10} {'P(Fooled)':<12} {'95% CI'}")
print("-" * 40)
for _, row in round_stats.iterrows():
    print(f"{int(row['round_number']):<10} {row['posterior_mean']:.3f}        [{row['ci_lower']:.3f} - {row['ci_upper']:.3f}]")

