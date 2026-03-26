# SIADS 521 Assignment 3

## Project Title
Interactive Video Game Sales Dashboard

## Project Overview
This project explores video game sales patterns using an interactive dashboard built with Streamlit and Plotly. The dashboard allows users to filter the dataset by year, genre, and platform, and then compare multiple coordinated visualizations on a single screen.

## Why this topic
I chose video game sales because the dataset supports several complementary views at once:
- changes over time
- comparisons across genres and platforms
- publisher dominance
- regional sales differences
- distribution of sales across titles

This makes it a good fit for an interactive dashboard assignment.

## Visualization Techniques Used
This dashboard includes:
- line chart
- bar chart
- histogram
- pie chart
- scatter plot

These charts work together to tell a cohesive story about market trends, category performance, and top-selling games.

## Visualization Library
This dashboard uses:
- Streamlit for the dashboard interface
- Plotly for interactive visualizations
- Pandas for loading and filtering data

Plotly is a strong choice because it supports interactive charts with hover details and works well inside Streamlit. Streamlit makes it easy to build a multi-chart dashboard with sidebar filters that affect all plots simultaneously.

## Data
- Raw dataset: `data/vgsales_raw.csv`
- Cleaned dataset: `data/vgsales_clean.csv`

## Data Cleaning Summary
The cleaned dataset was prepared by:
- standardizing column names
- handling missing values
- converting year to numeric
- keeping relevant sales columns for analysis

## Files
- `app.py` – main Streamlit dashboard
- `requirements.txt` – required packages
- `data/vgsales_clean.csv` – cleaned dataset
- `data/vgsales_raw.csv` – original dataset

## LINKS

## Dashboard Link
https://siads521-assignment3-yva6skjxefwgnjkuv2n9we.streamlit.app/

## Video Demo Link
https://youtu.be/aAUtAb46HP0

## Notebooks
notebooks/assignment3_notebook.ipynb


## How to Run Locally
```bash
git clone https://github.com/gwc-creator/siads521-assignment3.git
cd siads521-assignment3
pip install -r requirements.txt
streamlit run app.py
