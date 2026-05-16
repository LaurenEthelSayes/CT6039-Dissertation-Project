import pandas as pd
import numpy as np
import pingouin as pg

scenarios = pd.read_csv('_CortexQuest__table_scenario_results.csv')

scenarios = scenarios[scenarios['response_time'] > 0]
scenarios['correct_binary'] = (scenarios['is_correct'] == 'Yes').astype(int)

print("ANOVA")
print("Testing whether accuracy significantly differed across the 3 rounds")

print(f"\nMean accuracy per round:")
print(scenarios.groupby('round_number')['correct_binary'].mean().mul(100).round(2))

result = pg.anova(data=scenarios, dv='correct_binary', between='round_number')
print("\nResults:")
print(result.to_string())

print("\nANOVA BY CUE TYPE")
print("Testing whether accuracy significantly differed across cue types")

print(f"\nMean accuracy per cue type:")
print(scenarios.groupby('cue_type')['correct_binary'].mean().mul(100).round(2))

result2 = pg.anova(data=scenarios, dv='correct_binary', between='cue_type')
print("\nResults:")
print(result2.to_string())

