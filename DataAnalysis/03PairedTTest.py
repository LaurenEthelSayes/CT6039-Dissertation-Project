import pandas as pd
import numpy as np
import pingouin as pg

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

merged = pre[['participant_id', 'conf_score']].merge(
    post[['participant_id', 'conf_score']],
    on='participant_id',
    suffixes=('_pre', '_post')
)

print("PAIRED SAMPLES T-TEST")
print("Testing whether confidence changed before vs after the simulation")

print(f"\nPre-survey confidence mean:  {merged['conf_score_pre'].mean():.2f}")
print(f"Post-survey confidence mean: {merged['conf_score_post'].mean():.2f}")

result = pg.ttest(merged['conf_score_pre'], merged['conf_score_post'], paired=True)
print("\nResults:")
print(result.to_string())
