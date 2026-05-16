import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

scenarios = pd.read_csv('_CortexQuest__table_scenario_results.csv')

scenarios = scenarios[scenarios['response_time'] > 0]
scenarios['correct_binary'] = (scenarios['is_correct'] == 'Yes').astype(int)
scenarios['fooled'] = 1 - scenarios['correct_binary']

sns.set_theme(style='darkgrid')
colors = sns.color_palette('Set2')

prior_alpha, prior_beta = 1, 1

cue_stats = scenarios.groupby('cue_type').agg(
    total=('fooled', 'count'),
    fooled=('fooled', 'sum')
).reset_index()

cue_stats['posterior_alpha'] = prior_alpha + cue_stats['fooled']
cue_stats['posterior_beta'] = prior_beta + (cue_stats['total'] - cue_stats['fooled'])
cue_stats['posterior_mean'] = cue_stats['posterior_alpha'] / (cue_stats['posterior_alpha'] + cue_stats['posterior_beta'])
cue_stats['ci_lower'] = stats.beta.ppf(0.025, cue_stats['posterior_alpha'], cue_stats['posterior_beta'])
cue_stats['ci_upper'] = stats.beta.ppf(0.975, cue_stats['posterior_alpha'], cue_stats['posterior_beta'])
cue_stats = cue_stats.sort_values('posterior_mean')

round_stats = scenarios.groupby('round_number').agg(
    total=('fooled', 'count'),
    fooled=('fooled', 'sum')
).reset_index()

round_stats['posterior_alpha'] = prior_alpha + round_stats['fooled']
round_stats['posterior_beta'] = prior_beta + (round_stats['total'] - round_stats['fooled'])
round_stats['posterior_mean'] = round_stats['posterior_alpha'] / (round_stats['posterior_alpha'] + round_stats['posterior_beta'])
round_stats['ci_lower'] = stats.beta.ppf(0.025, round_stats['posterior_alpha'], round_stats['posterior_beta'])
round_stats['ci_upper'] = stats.beta.ppf(0.975, round_stats['posterior_alpha'], round_stats['posterior_beta'])

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Bayesian Analysis', fontsize=14, fontweight='bold')

axes[0].barh(cue_stats['cue_type'], cue_stats['posterior_mean'], color=colors[2], alpha=0.8)
axes[0].errorbar(cue_stats['posterior_mean'], cue_stats['cue_type'],
                xerr=[cue_stats['posterior_mean'] - cue_stats['ci_lower'],
                      cue_stats['ci_upper'] - cue_stats['posterior_mean']],
                fmt='none', color='black', capsize=4)
axes[0].axvline(0.5, color='red', linestyle='--', label='50% threshold')
axes[0].set_title('Probability of Being Fooled by Cue Type')
axes[0].set_xlabel('Probability of Being Fooled')
axes[0].legend()

axes[1].bar(['Round 1', 'Round 2', 'Round 3'], round_stats['posterior_mean'], color=colors[3], alpha=0.8)
axes[1].errorbar(['Round 1', 'Round 2', 'Round 3'], round_stats['posterior_mean'],
                yerr=[round_stats['posterior_mean'] - round_stats['ci_lower'],
                      round_stats['ci_upper'] - round_stats['posterior_mean']],
                fmt='none', color='black', capsize=4)
axes[1].axhline(0.5, color='red', linestyle='--', label='50% threshold')
axes[1].set_title('Probability of Being Fooled by Round')
axes[1].set_ylabel('Probability of Being Fooled')
axes[1].legend()

plt.tight_layout()
plt.savefig('14Bayesian.png', dpi=150)
plt.close()
print("Saved: 14Bayesian.png")