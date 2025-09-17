# Python-Frameworks-assignment
# CORD-19 Data Explorer

An interactive data exploration project analyzing the **CORD-19 (COVID-19 Open Research Dataset)**.
This project focuses on data cleaning, visualization, and dashboard development using **Python, Pandas, Seaborn, Matplotlib, and Streamlit**.


##  Features

* Cleaned and preprocessed the `metadata.csv` dataset
* Generated new features:

  * Title word count
  * Abstract word count
  * Publication year
* Visualized:

  * Distribution of abstract and title lengths
  * Top journals by publications
  * Top authors
  * Papers per year
  * Average abstract length per year
  * Availability of PDF and PMC JSON files
* Built an **interactive Streamlit app** with sidebar filters (year range, top N authors/journals)

## Project Structure

 CORD-19-Explorer
├── app.py                # Streamlit dashboard
├── part1_explore.py      # Command-line exploration script
├── full_assignment.py    # Combined script for all tasks
├── metadata.csv          # Dataset (not included here due to size)
├── REPORT.md             # Findings and reflection
├── README.md             # Project documentation (this file)

CORD-19 Data Exploration Report
1. Overview

This project explores the COVID-19 Open Research Dataset (CORD-19) using the metadata.csv file. The goal was to analyze research trends, publication patterns, and document insights through interactive visualizations using Python, pandas, matplotlib, seaborn, and Streamlit.

2. Data Loading and Exploration

Loaded metadata.csv into a pandas DataFrame.

Initial inspection included:

Number of rows and columns

Data types of each column

Missing value checks

First few rows preview

Observations:

Dataset contained 19 columns, including title, abstract, authors, journal, publication date, and file availability.

Some columns (e.g., mag_id, who_covidence_id, arxiv_id, s2_id) were mostly empty and were dropped.

3. Data Cleaning

Filled missing values in:

Abstract → "No abstract"

Authors → "Unknown"

PDF/PMC JSON columns → "None"

SHA → "None"

Extracted new features:

title_word_count → number of words in paper title

abstract_word_count → number of words in abstract

year → extracted from publish_time for time-based analysis

4. Key Findings and Visualizations
4.1 Abstract and Title Word Count

Abstracts mostly ranged 100–300 words.

Titles mostly had 5–15 words, showing concise naming.

Visualizations: Histogram of abstract and title word counts.


4.2 Top Journals

Most papers were published in top journals such as The Lancet, Nature, and BMJ.

Visualizations: Bar chart of top 10 journals.

4.3 Top Authors

A few authors contributed significantly to COVID-19 research publications.

Visualizations: Bar chart of top authors.

4.4 Publication Trends

Number of publications surged in 2020 and 2021.

Average abstract length slightly increased over time.

Visualizations: Papers per year, average abstract length per year.


4.5 PDF and PMC JSON Availability

Most papers had PDF and PMC JSON files available, though some were missing.

Visualizations: PDF and PMC JSON availability charts.


5. Streamlit Application

Interactive app built with Streamlit to explore the dataset.

Features:

Filter papers by publication year.

Select top N journals and authors.

Display histograms and bar charts.

Show PDF/PMC availability and abstract statistics.

Local URL example: http://localhost:8503

6. Challenges

Handling mixed data types in the CSV.

Converting publication dates correctly for analysis.

Cleaning and filling missing data without losing important records.

Making visualizations readable for large datasets.

Integrating all analyses into an interactive Streamlit dashboard.

7. Learning Outcomes

Gained practical experience with:

Data cleaning, preprocessing, and feature engineering

Visualization using matplotlib and seaborn

Building interactive dashboards with Streamlit

Developed skills to interpret research trends and patterns in large datasets.

Learned best practices for documenting and presenting findings in a GitHub repo.
