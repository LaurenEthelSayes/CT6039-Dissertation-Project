import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

merged_conf = pre[['participant_id', 'conf_score']].merge(
    post[['participant_id', 'conf_score']],
    on='participant_id',
    suffixes=('_pre', '_post')
)

sns.set_theme(style='darkgrid')
colors = sns.color_palette('Set2')

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Correlation Analysis', fontsize=14, fontweight='bold')

axes[0].scatter(scenarios['response_time'], scenarios['correct_binary'], alpha=0.3, color=colors[0])
z = np.polyfit(scenarios['response_time'], scenarios['correct_binary'], 1)
p = np.poly1d(z)
axes[0].plot(sorted(scenarios['response_time']), p(sorted(scenarios['response_time'])), 'r--', label='Trend line')
axes[0].set_title('Response Time vs Accuracy')
axes[0].set_xlabel('Response Time (seconds)')
axes[0].set_ylabel('Correct (1) or Wrong (0)')
axes[0].legend()

axes[1].scatter(merged_conf['conf_score_pre'], merged_conf['conf_score_post'], alpha=0.6, color=colors[1])
axes[1].plot([1, 5], [1, 5], 'r--', label='No change line')
axes[1].set_title('Pre vs Post Confidence Correlation')
axes[1].set_xlabel('Pre Survey Confidence')
axes[1].set_ylabel('Post Survey Confidence')
axes[1].legend()

plt.tight_layout()
plt.savefig('09Correlation.png', dpi=150)
plt.close()
print("Saved: 09Correlation.png")