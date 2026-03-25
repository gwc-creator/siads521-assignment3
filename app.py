import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Video Game Sales Dashboard", layout="wide")
st.title("Video Game Sales Interactive Dashboard")
st.markdown("Explore video game sales by year, platform, genre, publisher, and region.")

@st.cache_data
def load_data():
    df = pd.read_csv("data/vgsales_clean.csv")
    return df

df = load_data()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

year_min = int(df["Year"].min())
year_max = int(df["Year"].max())

selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

all_genres = sorted(df["Genre"].dropna().unique())
selected_genres = st.sidebar.multiselect(
    "Select Genre(s)",
    all_genres,
    default=all_genres
)

all_platforms = sorted(df["Platform"].dropna().unique())
selected_platforms = st.sidebar.multiselect(
    "Select Platform(s)",
    all_platforms,
    default=all_platforms
)

top_n = st.sidebar.slider("Top N Publishers / Games", 5, 20, 10)

# -----------------------------
# Filtered data
# -----------------------------
filtered_df = df[
    (df["Year"].between(selected_years[0], selected_years[1])) &
    (df["Genre"].isin(selected_genres)) &
    (df["Platform"].isin(selected_platforms))
].copy()

st.subheader("Filtered Dataset Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Rows", len(filtered_df))
col2.metric("Total Global Sales", f"{filtered_df['Global_Sales'].sum():,.2f}M")
col3.metric("Unique Games", filtered_df["Name"].nunique())

if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust your filters.")
    st.stop()

# -----------------------------
# Chart 1: Global sales over time
# -----------------------------
sales_by_year = (
    filtered_df.groupby("Year", as_index=False)["Global_Sales"]
    .sum()
    .sort_values("Year")
)

fig1 = px.line(
    sales_by_year,
    x="Year",
    y="Global_Sales",
    markers=True,
    title="Global Sales Over Time"
)

# -----------------------------
# Chart 2: Global sales by genre
# -----------------------------
sales_by_genre = (
    filtered_df.groupby("Genre", as_index=False)["Global_Sales"]
    .sum()
    .sort_values("Global_Sales", ascending=False)
)

fig2 = px.bar(
    sales_by_genre,
    x="Genre",
    y="Global_Sales",
    title="Global Sales by Genre"
)

# -----------------------------
# Chart 3: Top publishers
# -----------------------------
sales_by_publisher = (
    filtered_df.groupby("Publisher", as_index=False)["Global_Sales"]
    .sum()
    .sort_values("Global_Sales", ascending=False)
    .head(top_n)
)

fig3 = px.bar(
    sales_by_publisher,
    x="Publisher",
    y="Global_Sales",
    title=f"Top {top_n} Publishers by Global Sales"
)

# -----------------------------
# Chart 4: Regional sales comparison
# -----------------------------
regional_sales = filtered_df[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].sum().reset_index()
regional_sales.columns = ["Region", "Sales"]

fig4 = px.pie(
    regional_sales,
    names="Region",
    values="Sales",
    title="Regional Sales Share"
)

# -----------------------------
# Chart 5: Platform vs sales
# -----------------------------
sales_by_platform = (
    filtered_df.groupby("Platform", as_index=False)["Global_Sales"]
    .sum()
    .sort_values("Global_Sales", ascending=False)
)

fig5 = px.bar(
    sales_by_platform,
    x="Platform",
    y="Global_Sales",
    title="Global Sales by Platform"
)

# -----------------------------
# Chart 6: Top games scatter
# -----------------------------
top_games = (
    filtered_df.sort_values("Global_Sales", ascending=False)
    .head(top_n)
)

fig6 = px.scatter(
    top_games,
    x="Year",
    y="Global_Sales",
    size="Global_Sales",
    color="Genre",
    hover_name="Name",
    title=f"Top {top_n} Best-Selling Games"
)

# -----------------------------
# Layout
# -----------------------------
row1_col1, row1_col2 = st.columns(2)
row1_col1.plotly_chart(fig1, use_container_width=True)
row1_col2.plotly_chart(fig2, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)
row2_col1.plotly_chart(fig3, use_container_width=True)
row2_col2.plotly_chart(fig4, use_container_width=True)

row3_col1, row3_col2 = st.columns(2)
row3_col1.plotly_chart(fig5, use_container_width=True)
row3_col2.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# Raw data preview
# -----------------------------
with st.expander("Show Filtered Data Table"):
    st.dataframe(filtered_df)
