# full_assignment.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

# -------------------------
# ARGUMENT PARSING
# -------------------------
parser = argparse.ArgumentParser(description="Explore and visualize metadata.csv")
parser.add_argument('--file', '-f', type=str, required=True, help='Path to CSV file')
parser.add_argument('--nrows', type=int, default=None, help='Number of rows to load')
args = parser.parse_args()

# -------------------------
# LOAD DATA
# -------------------------
print(f"Loading data from: {args.file}")
df = pd.read_csv(args.file, nrows=args.nrows)

print("\n=== BASIC INFO ===")
print(df.info())
print("\n=== SHAPE ===")
print(df.shape)
print("\n=== FIRST 5 ROWS ===")
print(df.head())

print("\n=== MISSING VALUES ===")
print(df.isnull().mean() * 100)

# -------------------------
# CLEAN DATA
# -------------------------
drop_cols = ['mag_id', 'who_covidence_id', 'arxiv_id', 's2_id']
df.drop(columns=drop_cols, inplace=True)
df['abstract'] = df['abstract'].fillna("No abstract")
df['authors'] = df['authors'].fillna("Unknown")
df['pdf_json_files'] = df['pdf_json_files'].fillna("None")
df['pmc_json_files'] = df['pmc_json_files'].fillna("None")
df['sha'] = df['sha'].fillna("None")

# Feature engineering
df['title_word_count'] = df['title'].apply(lambda x: len(str(x).split()))
df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()))

print("\nData cleaned successfully!")
print("\n=== FIRST 5 ROWS AFTER CLEANING ===")
print(df.head())
print("\n=== MISSING VALUES AFTER CLEANING ===")
print(df.isnull().mean() * 100)

# -------------------------
# BASIC VISUALIZATIONS
# -------------------------
sns.set(style="whitegrid")

# 1. Histogram of abstract word count
plt.figure(figsize=(10,6))
sns.histplot(df['abstract_word_count'], bins=50, color='skyblue')
plt.title('Distribution of Abstract Word Count')
plt.xlabel('Number of words in abstract')
plt.ylabel('Frequency')
plt.savefig("abstract_word_count_hist.png")
plt.show()

# 2. Histogram of title word count
plt.figure(figsize=(10,6))
sns.histplot(df['title_word_count'], bins=30, color='orange')
plt.title('Distribution of Title Word Count')
plt.xlabel('Number of words in title')
plt.ylabel('Frequency')
plt.savefig("title_word_count_hist.png")
plt.show()

# 3. Top 10 Journals
plt.figure(figsize=(12,6))
top_journals = df['journal'].value_counts().head(10)
sns.barplot(x=top_journals.values, y=top_journals.index, palette='viridis')
plt.title('Top 10 Journals by Number of Papers')
plt.xlabel('Number of Papers')
plt.ylabel('Journal')
plt.savefig("top_journals.png")
plt.show()

# 4. Papers per publish year
df['year'] = pd.to_datetime(df['publish_time'], errors='coerce').dt.year
plt.figure(figsize=(12,6))
year_counts = df['year'].value_counts().sort_index()
sns.barplot(x=year_counts.index, y=year_counts.values, palette='magma')
plt.title('Number of Papers Published Per Year')
plt.xlabel('Year')
plt.ylabel('Number of Papers')
plt.xticks(rotation=45)
plt.savefig("papers_per_year.png")
plt.show()

# Top 10 Authors
plt.figure(figsize=(12,6))
top_authors = df['authors'].value_counts().head(10)
sns.barplot(x=top_authors.values, y=top_authors.index, palette='coolwarm')
plt.title('Top 10 Authors by Number of Papers')
plt.xlabel('Number of Papers')
plt.ylabel('Author')
plt.savefig("top_authors.png")
plt.show()
# Count of papers with/without PDF and PMC JSON
plt.figure(figsize=(8,6))
pdf_counts = df['pdf_json_files'].apply(lambda x: 'Available' if x != "None" else 'Missing').value_counts()
sns.barplot(x=pdf_counts.index, y=pdf_counts.values, palette='Set2')
plt.title('PDF JSON Availability')
plt.xlabel('Status')
plt.ylabel('Number of Papers')
plt.savefig("pdf_json_availability.png")
plt.show()

plt.figure(figsize=(8,6))
pmc_counts = df['pmc_json_files'].apply(lambda x: 'Available' if x != "None" else 'Missing').value_counts()
sns.barplot(x=pmc_counts.index, y=pmc_counts.values, palette='Set1')
plt.title('PMC JSON Availability')
plt.xlabel('Status')
plt.ylabel('Number of Papers')
plt.savefig("pmc_json_availability.png")
plt.show()
# Average abstract length by year
plt.figure(figsize=(12,6))
avg_abstract_year = df.groupby('year')['abstract_word_count'].mean()
sns.lineplot(x=avg_abstract_year.index, y=avg_abstract_year.values, marker='o', color='purple')
plt.title('Average Abstract Word Count Per Year')
plt.xlabel('Year')
plt.ylabel('Average Abstract Word Count')
plt.xticks(rotation=45)
plt.savefig("avg_abstract_per_year.png")
plt.show()

# -------------------------
# Word Cloud of Paper Titles
# -------------------------
from wordcloud import WordCloud

all_titles = " ".join(df['title'].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)

plt.figure(figsize=(15,7.5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Paper Titles', fontsize=20)
plt.savefig("title_wordcloud.png")
plt.show()

# -------------------------
# Papers by Source
# -------------------------
plt.figure(figsize=(12,6))
source_counts = df['source_x'].value_counts()
sns.barplot(x=source_counts.index, y=source_counts.values, palette='pastel')
plt.title('Number of Papers by Source')
plt.xlabel('Source')
plt.ylabel('Number of Papers')
plt.xticks(rotation=45)
plt.savefig("papers_by_source.png")
plt.show()
