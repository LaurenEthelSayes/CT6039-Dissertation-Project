import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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

model = smf.ols('correct_binary ~ conf_score + trained + response_time', data=merged).fit()

sns.set_theme(style='darkgrid')
colors = sns.color_palette('Set2')

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Linear Regression Analysis', fontsize=14, fontweight='bold')

coefficients = model.params.drop('Intercept')
pvalues = model.pvalues.drop('Intercept')
bar_colors = ['green' if p < 0.05 else 'grey' for p in pvalues]
axes[0].bar(coefficients.index, coefficients.values, color=bar_colors)
axes[0].set_title('Regression Coefficients\n(green = significant, grey = not significant)')
axes[0].set_ylabel('Coefficient Value')
axes[0].axhline(0, color='black', linestyle='-', linewidth=0.8)
axes[0].tick_params(axis='x', rotation=15)

axes[1].scatter(merged['response_time'], merged['correct_binary'], alpha=0.3, color=colors[0])
z = np.polyfit(merged['response_time'], merged['correct_binary'], 1)
p = np.poly1d(z)
axes[1].plot(sorted(merged['response_time']), p(sorted(merged['response_time'])), 'r--', label='Trend line')
axes[1].set_title('Response Time vs Accuracy (Key Predictor)')
axes[1].set_xlabel('Response Time (seconds)')
axes[1].set_ylabel('Correct (1) or Wrong (0)')
axes[1].legend()

plt.tight_layout()
plt.savefig('13LinearRegression.png', dpi=150)
plt.close()
print("Saved: 13LinearRegression.png")