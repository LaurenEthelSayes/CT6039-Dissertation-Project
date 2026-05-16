import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re

pre = pd.read_csv('_CortexQuest__table_presurvey.csv')
post = pd.read_csv('_CortexQuest__table_postsurvey.csv')

pre_qual_cols = ['qual1', 'qual2', 'qual3', 'qual4']
post_qual_cols = ['qual_post1', 'qual_post2', 'qual_post3']

pre_text = ' '.join(pre[pre_qual_cols].fillna('').values.flatten())
post_text = ' '.join(post[post_qual_cols].fillna('').values.flatten())
all_text = pre_text + ' ' + post_text

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
    'messages', 'email', 'emails'
])

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    words = [w for w in words if w not in stopwords and len(w) > 2]
    return ' '.join(words), words

cleaned_all, all_words = clean_text(all_text)
cleaned_pre, pre_words = clean_text(pre_text)
cleaned_post, post_words = clean_text(post_text)

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Qualitative Response Analysis', fontsize=16, fontweight='bold')

wc_pre = WordCloud(width=700, height=500, background_color='white',
                   colormap='Set2', max_words=50).generate(cleaned_pre)
axes[0].imshow(wc_pre, interpolation='bilinear')
axes[0].set_title('Pre-Survey: Most Common Themes', fontsize=13)
axes[0].axis('off')

wc_post = WordCloud(width=700, height=500, background_color='white',
                    colormap='Set1', max_words=50).generate(cleaned_post)
axes[1].imshow(wc_post, interpolation='bilinear')
axes[1].set_title('Post-Survey: Most Common Themes', fontsize=13)
axes[1].axis('off')

plt.tight_layout()
plt.savefig('16QualitativeWordClouds.png', dpi=150)
plt.close()
print("Saved: 16QualitativeWordClouds.png")

top_words = Counter(all_words).most_common(15)
words, counts = zip(*top_words)

fig, ax = plt.subplots(figsize=(12, 6))
ax.barh(words, counts, color=plt.cm.Set2.colors[:len(words)])
ax.set_title('Top 15 Most Frequent Words Across All Qualitative Responses', fontsize=13, fontweight='bold')
ax.set_xlabel('Frequency')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('17QualitativeTopWords.png', dpi=150)
plt.close()
print("Saved: 17QualitativeTopWords.png")

print("\nAll qualitative visualisations saved!")