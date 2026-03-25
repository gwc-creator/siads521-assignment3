import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Video Game Sales Dashboard", layout="wide")

st.title("Video Game Sales Dashboard")
st.markdown(
    """
    This interactive dashboard explores global video game sales across time, genre,
    platform, publisher, and region. Use the sidebar filters to update all visualizations
    at once and compare how sales patterns change.
    """
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/vgsales_clean.csv")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)
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
    value=(year_min, year_max),
)

all_genres = sorted(df["Genre"].dropna().unique())
selected_genres = st.sidebar.multiselect(
    "Select Genre(s)",
    all_genres,
    default=all_genres,
)

all_platforms = sorted(df["Platform"].dropna().unique())
selected_platforms = st.sidebar.multiselect(
    "Select Platform(s)",
    all_platforms,
    default=all_platforms,
)

top_n = st.sidebar.slider("Top N Games / Publishers", 5, 20, 10)

# -----------------------------
# Filter data
# -----------------------------
filtered_df = df[
    (df["Year"].between(selected_years[0], selected_years[1]))
    & (df["Genre"].isin(selected_genres))
    & (df["Platform"].isin(selected_platforms))
].copy()

if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust the sidebar selections.")
    st.stop()

# -----------------------------
# KPI cards
# -----------------------------
st.subheader("Dashboard Overview")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Rows", f"{len(filtered_df):,}")
kpi2.metric("Unique Games", f"{filtered_df['Name'].nunique():,}")
kpi3.metric("Unique Publishers", f"{filtered_df['Publisher'].nunique():,}")
kpi4.metric("Total Global Sales", f"{filtered_df['Global_Sales'].sum():,.2f}M")

st.markdown("---")

# -----------------------------
# Chart 1: Sales over time
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
    title="Global Sales Over Time",
)
fig1.update_layout(xaxis_title="Year", yaxis_title="Global Sales (Millions)")

# -----------------------------
# Chart 2: Sales by genre
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
    title="Global Sales by Genre",
)
fig2.update_layout(xaxis_title="Genre", yaxis_title="Global Sales (Millions)")

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
    x="Global_Sales",
    y="Publisher",
    orientation="h",
    title=f"Top {top_n} Publishers by Global Sales",
)
fig3.update_layout(xaxis_title="Global Sales (Millions)", yaxis_title="Publisher")

# -----------------------------
# Chart 4: Sales distribution
# -----------------------------
fig4 = px.histogram(
    filtered_df,
    x="Global_Sales",
    nbins=30,
    title="Distribution of Global Sales",
)
fig4.update_layout(xaxis_title="Global Sales (Millions)", yaxis_title="Count")

# -----------------------------
# Chart 5: Regional sales share
# -----------------------------
regional_sales = filtered_df[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].sum().reset_index()
regional_sales.columns = ["Region", "Sales"]

fig5 = px.pie(
    regional_sales,
    names="Region",
    values="Sales",
    title="Regional Sales Share",
)

# -----------------------------
# Chart 6: Top games scatter
# -----------------------------
top_games = filtered_df.sort_values("Global_Sales", ascending=False).head(top_n)

fig6 = px.scatter(
    top_games,
    x="Year",
    y="Global_Sales",
    size="Global_Sales",
    color="Genre",
    hover_name="Name",
    title=f"Top {top_n} Best-Selling Games",
)
fig6.update_layout(xaxis_title="Year", yaxis_title="Global Sales (Millions)")

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
# Narrative summary
# -----------------------------
st.markdown("### Key Takeaways")
st.markdown(
    """
    - The line chart shows how overall game sales change across years.
    - The genre and publisher charts reveal which categories dominate under the current filters.
    - The histogram helps show whether sales are concentrated among a few high-selling titles.
    - The regional pie chart compares market share across North America, Europe, Japan, and Other regions.
    - The scatter plot highlights the best-selling games and allows quick comparison by year and genre.
    """
)

# -----------------------------
# Data table
# -----------------------------
with st.expander("Show Filtered Data Table"):
    st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_vgsales.csv",
    mime="text/csv",
)
