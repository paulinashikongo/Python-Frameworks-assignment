# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter

# -------------------------
# STREAMLIT APP HEADER
# -------------------------
st.title("CORD-19 Data Explorer")
st.write("Explore COVID-19 research papers from the CORD-19 dataset")

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv('metadata.csv', low_memory=False)

# -------------------------
# DATA CLEANING
# -------------------------
drop_cols = ['mag_id', 'who_covidence_id', 'arxiv_id', 's2_id']
df.drop(columns=drop_cols, inplace=True, errors='ignore')

df['abstract'] = df['abstract'].fillna("No abstract")
df['authors'] = df['authors'].fillna("Unknown")
df['pdf_json_files'] = df['pdf_json_files'].fillna("None")
df['pmc_json_files'] = df['pmc_json_files'].fillna("None")
df['sha'] = df['sha'].fillna("None")

df['title_word_count'] = df['title'].apply(lambda x: len(str(x).split()))
df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()))
df['year'] = pd.to_datetime(df['publish_time'], errors='coerce').dt.year

# -------------------------
# SIDEBAR FILTERS
# -------------------------
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.sidebar.slider("Select publication year range", min_year, max_year, (min_year, max_year))

top_n_journals = st.sidebar.slider("Top N journals", 5, 20, 10)
top_n_authors = st.sidebar.slider("Top N authors", 5, 20, 10)
top_n_words = st.sidebar.slider("Top N words in titles", 5, 20, 10)

filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# -------------------------
# BASIC VISUALIZATIONS
# -------------------------
sns.set(style="whitegrid")

# Histogram of abstract word count
st.subheader("Distribution of Abstract Word Count")
fig, ax = plt.subplots(figsize=(10,6))
sns.histplot(filtered_df['abstract_word_count'], bins=50, color='skyblue', ax=ax)
ax.set_xlabel("Number of words in abstract")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Histogram of title word count
st.subheader("Distribution of Title Word Count")
fig, ax = plt.subplots(figsize=(10,6))
sns.histplot(filtered_df['title_word_count'], bins=30, color='orange', ax=ax)
ax.set_xlabel("Number of words in title")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Top journals
st.subheader(f"Top {top_n_journals} Journals by Number of Papers")
top_journals = filtered_df['journal'].value_counts().head(top_n_journals)
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(x=top_journals.values, y=top_journals.index, palette='viridis', ax=ax)
ax.set_xlabel("Number of Papers")
ax.set_ylabel("Journal")
st.pyplot(fig)

# Top authors
st.subheader(f"Top {top_n_authors} Authors by Number of Papers")
top_authors = filtered_df['authors'].value_counts().head(top_n_authors)
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(x=top_authors.values, y=top_authors.index, palette='coolwarm', ax=ax)
ax.set_xlabel("Number of Papers")
ax.set_ylabel("Author")
st.pyplot(fig)

# Papers per year
st.subheader("Number of Papers Published Per Year")
year_counts = filtered_df['year'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(x=year_counts.index, y=year_counts.values, palette='magma', ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

# PDF JSON availability
st.subheader("PDF JSON Availability")
pdf_counts = filtered_df['pdf_json_files'].apply(lambda x: 'Available' if x != "None" else 'Missing').value_counts()
fig, ax = plt.subplots(figsize=(8,6))
sns.barplot(x=pdf_counts.index, y=pdf_counts.values, palette='Set2', ax=ax)
ax.set_xlabel("Status")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# PMC JSON availability
st.subheader("PMC JSON Availability")
pmc_counts = filtered_df['pmc_json_files'].apply(lambda x: 'Available' if x != "None" else 'Missing').value_counts()
fig, ax = plt.subplots(figsize=(8,6))
sns.barplot(x=pmc_counts.index, y=pmc_counts.values, palette='Set1', ax=ax)
ax.set_xlabel("Status")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# Average abstract length per year
st.subheader("Average Abstract Word Count Per Year")
avg_abstract_year = filtered_df.groupby('year')['abstract_word_count'].mean()
fig, ax = plt.subplots(figsize=(12,6))
sns.lineplot(x=avg_abstract_year.index, y=avg_abstract_year.values, marker='o', color='purple', ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Average Abstract Word Count")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

# -------------------------
# Word Cloud for Titles
# -------------------------
st.subheader("Word Cloud of Paper Titles")
all_titles = " ".join(filtered_df['title'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
fig, ax = plt.subplots(figsize=(15,7))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

# -------------------------
# Papers by Source
# -------------------------
st.subheader("Distribution of Papers by Source")
source_counts = filtered_df['source_x'].value_counts()
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x=source_counts.index, y=source_counts.values, palette='pastel', ax=ax)
ax.set_xlabel("Source")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# -------------------------
# Top Words in Titles (optional)
# -------------------------
st.subheader(f"Top {top_n_words} Most Frequent Words in Titles")
all_words = " ".join(filtered_df['title'].dropna().astype(str)).lower().split()
stop_words = set(['the','and','of','in','to','for','on','with','a','an','by','from'])
words_filtered = [w for w in all_words if w not in stop_words]
word_freq = Counter(words_filtered)
top_words = dict(word_freq.most_common(top_n_words))
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(x=list(top_words.values()), y=list(top_words.keys()), palette='Blues_d', ax=ax)
ax.set_xlabel("Frequency")
ax.set_ylabel("Word")
st.pyplot(fig)




