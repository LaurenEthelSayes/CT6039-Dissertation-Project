import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

scenarios = pd.read_csv('_CortexQuest__table_scenario_results.csv')

scenarios = scenarios[scenarios['response_time'] > 0]
scenarios['correct_binary'] = (scenarios['is_correct'] == 'Yes').astype(int)

sns.set_theme(style='darkgrid')
colors = sns.color_palette('Set2')

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('ANOVA Analysis', fontsize=14, fontweight='bold')

round_accuracy = scenarios.groupby('round_number')['correct_binary'].mean().mul(100)
round_accuracy.plot(kind='bar', ax=axes[0], color=colors)
axes[0].set_title('Accuracy by Round')
axes[0].set_xlabel('Round')
axes[0].set_ylabel('Accuracy (%)')
axes[0].set_xticklabels(['Round 1', 'Round 2', 'Round 3'], rotation=0)
axes[0].axhline(50, color='red', linestyle='--', label='50% threshold')
axes[0].legend()

cue_accuracy = scenarios.groupby('cue_type')['correct_binary'].mean().mul(100).sort_values()
cue_accuracy.plot(kind='barh', ax=axes[1], color=colors)
axes[1].set_title('Accuracy by Cue Type')
axes[1].set_xlabel('Accuracy (%)')
axes[1].axvline(50, color='red', linestyle='--', label='50% threshold')
axes[1].legend()

plt.tight_layout()
plt.savefig('11ANOVA.png', dpi=150)
plt.close()
print("Saved: 11ANOVA.png")