import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pre = pd.read_csv('_CortexQuest__table_presurvey.csv')
scenarios = pd.read_csv('_CortexQuest__table_scenario_results.csv')

scenarios = scenarios[scenarios['response_time'] > 0]
scenarios['correct_binary'] = (scenarios['is_correct'] == 'Yes').astype(int)

merged = scenarios.merge(pre[['participant_id', 'cyber_training', 'age_group', 'gender']], on='participant_id')

sns.set_theme(style='darkgrid')
colors = sns.color_palette('Set2')

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Chi-Square Analysis', fontsize=14, fontweight='bold')

pd.crosstab(merged['cyber_training'], merged['correct_binary']).plot(kind='bar', ax=axes[0], color=[colors[0], colors[1]])
axes[0].set_title('Cyber Training vs Accuracy')
axes[0].set_xlabel('Cyber Training')
axes[0].set_ylabel('Count')
axes[0].tick_params(axis='x', rotation=45)
axes[0].legend(['Wrong', 'Correct'])

pd.crosstab(merged['gender'], merged['correct_binary']).plot(kind='bar', ax=axes[1], color=[colors[0], colors[1]])
axes[1].set_title('Gender vs Accuracy')
axes[1].set_xlabel('Gender')
axes[1].set_ylabel('Count')
axes[1].tick_params(axis='x', rotation=45)
axes[1].legend(['Wrong', 'Correct'])

pd.crosstab(merged['age_group'], merged['correct_binary']).plot(kind='bar', ax=axes[2], color=[colors[0], colors[1]])
axes[2].set_title('Age Group vs Accuracy')
axes[2].set_xlabel('Age Group')
axes[2].set_ylabel('Count')
axes[2].tick_params(axis='x', rotation=45)
axes[2].legend(['Wrong', 'Correct'])

plt.tight_layout()
plt.savefig('12ChiSquare.png', dpi=150)
plt.close()
print("Saved: 12ChiSquare.png")