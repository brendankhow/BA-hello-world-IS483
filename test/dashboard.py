
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Load data
@st.cache_data
def load_data():
    # Load your cleaned Excel file
    sheets = pd.read_excel('sgsmu.studentcare_instagram_comments_cleaned.xlsx', sheet_name=None)
    combined_df = pd.concat([df.assign(Post=sheet) for sheet, df in sheets.items()], ignore_index=True)
    return combined_df

df = load_data()

st.title('Student Mental Wellness Dashboard')

# Sentiment Distribution
st.header('Sentiment Analysis')
sentiment_counts = df['Sentiment'].value_counts()
fig, ax = plt.subplots()
ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%')
st.pyplot(fig)

# Top Words
st.header('Top Words')
all_text = ' '.join(df.iloc[:, 3].dropna().astype(str))
stop_words = set(stopwords.words('english'))
words = [word.lower() for word in all_text.split() if word.lower() not in stop_words and len(word) > 2]
word_freq = Counter(words)
top_words = word_freq.most_common(20)
words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Frequency', y='Word', data=words_df, ax=ax)
st.pyplot(fig)

# Word Cloud
st.header('Word Cloud')
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

# Sentiment by Post
st.header('Sentiment by Post')
sentiment_by_post = df.groupby(['Post', 'Sentiment']).size().unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(12, 6))
sentiment_by_post.plot(kind='bar', stacked=True, ax=ax)
st.pyplot(fig)
