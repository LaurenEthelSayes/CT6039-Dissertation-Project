import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pre = pd.read_csv('_CortexQuest__table_presurvey.csv')
post = pd.read_csv('_CortexQuest__table_postsurvey.csv')
scenarios = pd.read_csv('_CortexQuest__table_scenario_results.csv')

scenarios = scenarios[scenarios['response_time'] > 0]
scenarios['correct_binary'] = (scenarios['is_correct'] == 'Yes').astype(int)

sns.set_theme(style='darkgrid')
colors = sns.color_palette('Set2')

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Descriptive Statistics', fontsize=14, fontweight='bold')

cue_accuracy = scenarios.groupby('cue_type')['correct_binary'].mean().mul(100).sort_values()
cue_accuracy.plot(kind='barh', ax=axes[0], color=colors)
axes[0].set_title('Accuracy by Cue Type')
axes[0].set_xlabel('Accuracy (%)')
axes[0].axvline(50, color='red', linestyle='--', label='50% threshold')
axes[0].legend()

round_accuracy = scenarios.groupby('round_number')['correct_binary'].mean().mul(100)
round_accuracy.plot(kind='bar', ax=axes[1], color=colors)
axes[1].set_title('Accuracy by Round')
axes[1].set_xlabel('Round')
axes[1].set_ylabel('Accuracy (%)')
axes[1].set_xticklabels(['Round 1', 'Round 2', 'Round 3'], rotation=0)
axes[1].axhline(50, color='red', linestyle='--', label='50% threshold')
axes[1].legend()

post['perceived_pressure'].value_counts().plot(kind='bar', ax=axes[2], color=colors)
axes[2].set_title('Perceived Pressure')
axes[2].set_xlabel('Pressure Level')
axes[2].set_ylabel('Count')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('08DescriptiveStats.png', dpi=150)
plt.close()
print("Saved: 08DescriptiveStats.png")
