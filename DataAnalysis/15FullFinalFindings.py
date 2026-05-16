import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.formula.api as smf

pre = pd.read_csv('_CortexQuest__table_presurvey.csv')
post = pd.read_csv('_CortexQuest__table_postsurvey.csv')
scenarios = pd.read_csv('_CortexQuest__table_scenario_results.csv')

scenarios = scenarios[scenarios['response_time'] > 0]
scenarios['correct_binary'] = (scenarios['is_correct'] == 'Yes').astype(int)
scenarios['fooled'] = 1 - scenarios['correct_binary']

conf_map = {
    'Not confident at all': 1,
    'Slightly confident': 2,
    'Moderately confident': 3,
    'Very confident': 4,
    'Extremely confident': 5
}

pre['conf_score'] = pre['suspicious_confidence'].map(conf_map)
post['conf_score'] = post['confidence_after'].map(conf_map)
pre['trained'] = (pre['cyber_training'] == 'Yes, formal training').astype(int)

merged_conf = pre[['participant_id', 'conf_score']].merge(
    post[['participant_id', 'conf_score']],
    on='participant_id',
    suffixes=('_pre', '_post')
)

merged_full = scenarios.merge(pre[['participant_id', 'conf_score', 'trained']], on='participant_id')
merged_demo = scenarios.merge(pre[['participant_id', 'cyber_training', 'age_group', 'gender']], on='participant_id')

model = smf.ols('correct_binary ~ conf_score + trained + response_time', data=merged_full).fit()

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

sns.set_theme(style='darkgrid')
colors = sns.color_palette('Set2')

fig = plt.figure(figsize=(24, 28))
fig.suptitle('Cortex Quest Full Final Findings\nThe Human Brain as an Attack Vector', 
             fontsize=20, fontweight='bold', y=0.98)

axes = []
axes.append(fig.add_subplot(4, 3, 1))
axes.append(fig.add_subplot(4, 3, 2))
axes.append(fig.add_subplot(4, 3, 3))
axes.append(fig.add_subplot(4, 3, 4))
axes.append(fig.add_subplot(4, 3, 5))
axes.append(fig.add_subplot(4, 3, 6))
axes.append(fig.add_subplot(4, 3, 7))
axes.append(fig.add_subplot(4, 3, 8))
axes.append(fig.add_subplot(4, 3, 9))
axes.append(fig.add_subplot(4, 3, 10))
axes.append(fig.add_subplot(4, 3, 11))
axes.append(fig.add_subplot(4, 3, 12))

cue_accuracy = scenarios.groupby('cue_type')['correct_binary'].mean().mul(100).sort_values()
cue_accuracy.plot(kind='barh', ax=axes[0], color=colors)
axes[0].set_title('Descriptive: Accuracy by Cue Type')
axes[0].set_xlabel('Accuracy (%)')
axes[0].axvline(50, color='red', linestyle='--', label='50%')
axes[0].legend(fontsize=8)

round_accuracy = scenarios.groupby('round_number')['correct_binary'].mean().mul(100)
round_accuracy.plot(kind='bar', ax=axes[1], color=colors)
axes[1].set_title('Descriptive: Accuracy by Round')
axes[1].set_xlabel('Round')
axes[1].set_ylabel('Accuracy (%)')
axes[1].set_xticklabels(['Round 1', 'Round 2', 'Round 3'], rotation=0)
axes[1].axhline(50, color='red', linestyle='--', label='50%')
axes[1].legend(fontsize=8)

post['perceived_pressure'].value_counts().plot(kind='bar', ax=axes[2], color=colors)
axes[2].set_title('Descriptive: Perceived Pressure')
axes[2].set_xlabel('Pressure Level')
axes[2].set_ylabel('Count')
axes[2].tick_params(axis='x', rotation=45)

axes[3].scatter(scenarios['response_time'], scenarios['correct_binary'], alpha=0.3, color=colors[0])
z = np.polyfit(scenarios['response_time'], scenarios['correct_binary'], 1)
p = np.poly1d(z)
axes[3].plot(sorted(scenarios['response_time']), p(sorted(scenarios['response_time'])), 'r--', label='Trend')
axes[3].set_title('Correlation: Response Time vs Accuracy')
axes[3].set_xlabel('Response Time (seconds)')
axes[3].set_ylabel('Correct (1) or Wrong (0)')
axes[3].legend(fontsize=8)

axes[4].scatter(merged_conf['conf_score_pre'], merged_conf['conf_score_post'], alpha=0.6, color=colors[1])
axes[4].plot([1, 5], [1, 5], 'r--', label='No change')
axes[4].set_title('Correlation: Pre vs Post Confidence')
axes[4].set_xlabel('Pre Confidence')
axes[4].set_ylabel('Post Confidence')
axes[4].legend(fontsize=8)

means = [merged_conf['conf_score_pre'].mean(), merged_conf['conf_score_post'].mean()]
errors = [merged_conf['conf_score_pre'].std(), merged_conf['conf_score_post'].std()]
axes[5].bar(['Pre Survey', 'Post Survey'], means, yerr=errors, color=[colors[0], colors[1]], capsize=6, alpha=0.8)
axes[5].set_title('Paired T-Test: Confidence Change\n(p = 0.009)')
axes[5].set_ylabel('Confidence Score (1-5)')
axes[5].set_ylim(0, 5)

round_accuracy.plot(kind='bar', ax=axes[6], color=colors)
axes[6].set_title('ANOVA: Accuracy by Round\n(p = 0.067)')
axes[6].set_xlabel('Round')
axes[6].set_ylabel('Accuracy (%)')
axes[6].set_xticklabels(['Round 1', 'Round 2', 'Round 3'], rotation=0)
axes[6].axhline(50, color='red', linestyle='--')

cue_accuracy.plot(kind='barh', ax=axes[7], color=colors)
axes[7].set_title('ANOVA: Accuracy by Cue Type\n(p = 0.000047)')
axes[7].set_xlabel('Accuracy (%)')
axes[7].axvline(50, color='red', linestyle='--')

pd.crosstab(merged_demo['cyber_training'], merged_demo['correct_binary']).plot(kind='bar', ax=axes[8], color=[colors[0], colors[1]])
axes[8].set_title('Chi-Square: Cyber Training vs Accuracy\n(p = 0.332)')
axes[8].set_xlabel('Cyber Training')
axes[8].set_ylabel('Count')
axes[8].tick_params(axis='x', rotation=45)
axes[8].legend(['Wrong', 'Correct'], fontsize=8)

coefficients = model.params.drop('Intercept')
pvalues = model.pvalues.drop('Intercept')
bar_colors = ['green' if p < 0.05 else 'grey' for p in pvalues]
axes[9].bar(coefficients.index, coefficients.values, color=bar_colors)
axes[9].set_title('Linear Regression: Coefficients\n(green = significant)')
axes[9].set_ylabel('Coefficient Value')
axes[9].axhline(0, color='black', linewidth=0.8)
axes[9].tick_params(axis='x', rotation=15)

axes[10].barh(cue_stats['cue_type'], cue_stats['posterior_mean'], color=colors[2], alpha=0.8)
axes[10].errorbar(cue_stats['posterior_mean'], cue_stats['cue_type'],
                xerr=[cue_stats['posterior_mean'] - cue_stats['ci_lower'],
                      cue_stats['ci_upper'] - cue_stats['posterior_mean']],
                fmt='none', color='black', capsize=4)
axes[10].axvline(0.5, color='red', linestyle='--', label='50%')
axes[10].set_title('Bayesian: Probability of Being Fooled')
axes[10].set_xlabel('Probability of Being Fooled')
axes[10].legend(fontsize=8)

summary_text = (
    "KEY FINDINGS SUMMARY\n\n"
    "Overall accuracy: 47.39%\n"
    "Reward cue fooled participants: 77.8%\n"
    "Confidence dropped significantly: p = 0.009\n"
    "Cue type effect: p = 0.000047\n"
    "Training made no difference: p = 0.332\n"
    "Time pressure predicted mistakes: p = 0.000\n\n"
    "CONCLUSION: The human brain is hackable.\n"
    "Cognitive triggers bypass critical thinking\n"
    "regardless of training, age or gender."
)

axes[11].axis('off')
axes[11].text(0.5, 0.5, summary_text, transform=axes[11].transAxes,
              fontsize=11, verticalalignment='center', horizontalalignment='center',
              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('15FullFinalFindings.png', dpi=150)
plt.close()
print("Saved: 15FullFinalFindings.png")