import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Video Game Sales Interactive Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("data/vgsales_clean.csv")

df = load_data()

st.write("Preview of cleaned data:")
st.dataframe(df.head())

year_range = st.slider(
    "Select year range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

filtered_df = df[df["Year"].between(year_range[0], year_range[1])]

genre_sales = (
    filtered_df.groupby("Genre", as_index=False)["Global_Sales"]
    .sum()
    .sort_values("Global_Sales", ascending=False)
)

fig = px.bar(
    genre_sales,
    x="Genre",
    y="Global_Sales",
    title="Global Sales by Genre"
)

st.plotly_chart(fig, use_container_width=True)
