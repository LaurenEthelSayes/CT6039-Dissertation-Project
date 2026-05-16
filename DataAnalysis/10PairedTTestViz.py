import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pre = pd.read_csv('_CortexQuest__table_presurvey.csv')
post = pd.read_csv('_CortexQuest__table_postsurvey.csv')

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
fig.suptitle('Paired T-Test: Pre vs Post Confidence', fontsize=14, fontweight='bold')

means = [merged_conf['conf_score_pre'].mean(), merged_conf['conf_score_post'].mean()]
errors = [merged_conf['conf_score_pre'].std(), merged_conf['conf_score_post'].std()]
axes[0].bar(['Pre Survey', 'Post Survey'], means, yerr=errors, color=[colors[0], colors[1]], capsize=6, alpha=0.8)
axes[0].set_title('Mean Confidence Before and After Simulation')
axes[0].set_ylabel('Confidence Score (1-5)')
axes[0].set_ylim(0, 5)

for i, row in merged_conf.iterrows():
    axes[1].plot(['Pre Survey', 'Post Survey'], [row['conf_score_pre'], row['conf_score_post']], color='grey', alpha=0.4)
axes[1].plot(['Pre Survey', 'Post Survey'], means, color='red', linewidth=2, label='Mean')
axes[1].set_title('Individual Confidence Changes')
axes[1].set_ylabel('Confidence Score (1-5)')
axes[1].set_ylim(0, 5)
axes[1].legend()

plt.tight_layout()
plt.savefig('10PairedTTest.png', dpi=150)
plt.close()
print("Saved: 10PairedTTest.png")