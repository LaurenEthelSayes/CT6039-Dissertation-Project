import pandas as pd
import numpy as np

participants = pd.read_csv('_CortexQuest__table_participants.csv')
pre = pd.read_csv('_CortexQuest__table_presurvey.csv')
post = pd.read_csv('_CortexQuest__table_postsurvey.csv')
scenarios = pd.read_csv('_CortexQuest__table_scenario_results.csv')

print("Data loaded")

print("\nMISSING VALUES")
print("Pre-survey:\n", pre.isnull().sum())
print("\nPost-survey:\n", post.isnull().sum())
print("\nScenarios:\n", scenarios.isnull().sum())

print("\nDUPLICATES")
print("Pre duplicates:", pre.duplicated(subset='participant_id').sum())
print("Post duplicates:", post.duplicated(subset='participant_id').sum())

print("\nRESPONSE TIME")
print(scenarios['response_time'].describe())

scenarios = scenarios[scenarios['response_time'] > 0]

for col in pre.select_dtypes(include='object').columns:
    pre[col] = pre[col].str.strip()

for col in post.select_dtypes(include='object').columns:
    post[col] = post[col].str.strip()

post['qual_post2'] = post['qual_post2'].fillna('No response')

print("\nPARTICIPATION FUNNEL")
print(f"Registered:        {len(participants)}")
print(f"Completed pre:     {len(pre)}")
print(f"Completed post:    {len(post)}")
print(f"Scenario entries:  {len(scenarios)}")

print("\nData cleaned and ready")