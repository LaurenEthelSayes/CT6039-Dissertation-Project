import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

pre = pd.read_csv('_CortexQuest__table_presurvey.csv')
post = pd.read_csv('_CortexQuest__table_postsurvey.csv')

stopwords = set([
    'i', 'me', 'my', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
    'to', 'for', 'of', 'with', 'it', 'is', 'are', 'was', 'be', 'been', 'have',
    'has', 'do', 'not', 'that', 'this', 'they', 'them', 'their', 'if', 'from',
    'as', 'by', 'so', 'what', 'when', 'which', 'who', 'will', 'would', 'could',
    'should', 'its', 'just', 'more', 'also', 'can', 'how', 'you', 'your', 'we',
    'our', 'there', 'about', 'up', 'out', 'than', 'then', 'into', 'through',
    'any', 'all', 'some', 'one', 'no', 'he', 'she', 'his', 'her', 'had', 'may',
    'most', 'other', 'such', 'even', 'only', 'very', 'much', 'think', 'feel',
    'get', 'got', 'make', 'made', 'often', 'well', 'now', 'still', 'dont',
    'doesnt', 'im', 'ive', 'id', 'its', 'things', 'something', 'anything',
    'everything', 'someone', 'anyone', 'way', 'time', 'times', 'thing', 'need',
    'know', 'use', 'used', 'using', 'take', 'taking', 'look', 'looking', 'see',
    'seen', 'say', 'said', 'click', 'clicking', 'send', 'sent', 'message',
    'messages', 'email', 'emails', 'people', 'person', 'being', 'whether',
    'though', 'because', 'before', 'after', 'always', 'never', 'every',
    'already', 'actually', 'really', 'quite', 'bit', 'lot', 'many', 'few',
    'own', 'back', 'first', 'second', 'third', 'new', 'old', 'different',
    'same', 'right', 'wrong', 'good', 'bad', 'big', 'small', 'long', 'short'
])

def get_top_words(text, n=15):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    words = [w for w in words if w not in stopwords and len(w) > 2]
    return Counter(words).most_common(n)

pre_text = ' '.join(pre[['qual1', 'qual2', 'qual3', 'qual4']].fillna('').values.flatten())
post_text = ' '.join(post[['qual_post1', 'qual_post2', 'qual_post3']].fillna('').values.flatten())

pre_top = get_top_words(pre_text)
post_top = get_top_words(post_text)

pre_words, pre_counts = zip(*pre_top)
post_words, post_counts = zip(*post_top)

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Pre vs Post Survey: Most Frequent Themes', fontsize=15, fontweight='bold')

axes[0].barh(pre_words, pre_counts, color='steelblue', alpha=0.85)
axes[0].set_title('Pre-Survey Top Themes\n(Before Simulation)', fontsize=12)
axes[0].set_xlabel('Frequency')
axes[0].invert_yaxis()

axes[1].barh(post_words, post_counts, color='tomato', alpha=0.85)
axes[1].set_title('Post-Survey Top Themes\n(After Simulation)', fontsize=12)
axes[1].set_xlabel('Frequency')
axes[1].invert_yaxis()

plt.tight_layout()
plt.savefig('18PrePostThematic.png', dpi=150)
plt.close()
print("Saved: 18PrePostThematic.png")