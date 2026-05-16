import pandas as pd

pre = pd.read_csv('_CortexQuest__table_presurvey.csv')
post = pd.read_csv('_CortexQuest__table_postsurvey.csv')

print("PRE-SURVEY QUALITATIVE RESPONSES")
print("\nQ1: What makes something look suspicious?")
for i, response in enumerate(pre['qual1'].dropna(), 1):
    print(f"\n{i}. {response}")

print("\n" + "="*60)
print("\nQ2: Why do people fall for cyber attacks?")
for i, response in enumerate(pre['qual2'].dropna(), 1):
    print(f"\n{i}. {response}")

print("\n" + "="*60)
print("\nQ3: What makes something look trustworthy?")
for i, response in enumerate(pre['qual3'].dropna(), 1):
    print(f"\n{i}. {response}")

print("\n" + "="*60)
print("\nQ4: How do you decide whether to respond?")
for i, response in enumerate(pre['qual4'].dropna(), 1):
    print(f"\n{i}. {response}")

print("\n" + "="*60)
print("\nPOST-SURVEY QUALITATIVE RESPONSES")
print("\nQ5: What cues most influenced your decisions?")
for i, response in enumerate(post['qual_post1'].dropna(), 1):
    print(f"\n{i}. {response}")

print("\n" + "="*60)
print("\nQ6: Which scenario did you find most difficult?")
for i, response in enumerate(post['qual_post2'].dropna(), 1):
    print(f"\n{i}. {response}")

print("\n" + "="*60)
print("\nQ7: Has this changed how you will respond to digital messages?")
for i, response in enumerate(post['qual_post3'].dropna(), 1):
    print(f"\n{i}. {response}")
    