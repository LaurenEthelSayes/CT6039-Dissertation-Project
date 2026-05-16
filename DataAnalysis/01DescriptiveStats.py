import pandas as pd
import numpy as np

participants = pd.read_csv('_CortexQuest__table_participants.csv')
pre = pd.read_csv('_CortexQuest__table_presurvey.csv')
post = pd.read_csv('_CortexQuest__table_postsurvey.csv')
scenarios = pd.read_csv('_CortexQuest__table_scenario_results.csv')

scenarios = scenarios[scenarios['response_time'] > 0]

print("PARTICIPANT DEMOGRAPHICS")
print("\nAge Group:\n", pre['age_group'].value_counts())
print("\nGender:\n", pre['gender'].value_counts())
print("\nEducation Level:\n", pre['education_level'].value_counts())
print("\nCyber Training:\n", pre['cyber_training'].value_counts())

print("\nSCENARIO PERFORMANCE")
scenarios['correct_binary'] = (scenarios['is_correct'] == 'Yes').astype(int)
print("\nOverall Accuracy Rate:", round(scenarios['correct_binary'].mean() * 100, 2), "%")
print("\nAccuracy by Round:\n", scenarios.groupby('round_number')['correct_binary'].mean().mul(100).round(2))
print("\nAccuracy by Cue Type:\n", scenarios.groupby('cue_type')['correct_binary'].mean().mul(100).round(2))

print("\nRESPONSE TIMES")
print("\nAverage Response Time by Round:\n", scenarios.groupby('round_number')['response_time'].mean().round(2))
print("\nOverall Response Time Stats:\n", scenarios['response_time'].describe().round(2))

print("\nSCORES")
print("\nAverage Score by Round:\n", scenarios.groupby('round_number')['score_after_action'].mean().round(2))
print("\nOverall Score Stats:\n", scenarios['score_after_action'].describe().round(2))

print("\nPOST SURVEY RESPONSES")
print("\nPerceived Difficulty:\n", post['perceived_difficulty'].value_counts())
print("\nPerceived Pressure:\n", post['perceived_pressure'].value_counts())
print("\nConfidence After:\n", post['confidence_after'].value_counts())
print("\nUrgency Influence:\n", post['urgency_influence'].value_counts())