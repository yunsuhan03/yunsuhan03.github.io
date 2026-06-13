import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------
# Page Setting
# ------------------------

st.set_page_config(
    page_title="Cafe Review Dashboard",
    layout="wide"
)

st.title("☕ Cafe Review Analysis Dashboard")

st.markdown(
    """
    Analyze cafe ratings, review counts,
    themes and customer preferences.
    """
)

# ------------------------
# Sample Data
# ------------------------

data = {
    "Cafe": [
        "Cafe A",
        "Cafe B",
        "Cafe C",
        "Cafe D",
        "Cafe E"
    ],

    "District": [
        "Gangnam",
        "Hongdae",
        "Gangnam",
        "Seongsu",
        "Hongdae"
    ],

    "Theme": [
        "Study",
        "Dessert",
        "Instagram",
        "Study",
        "Dessert"
    ],

    "Rating": [
        4.8,
        4.5,
        4.7,
        4.3,
        4.6
    ],

    "ReviewCount": [
        520,
        430,
        380,
        250,
        410
    ]
}

df = pd.DataFrame(data)

# ------------------------
# Sidebar Filter
# ------------------------

st.sidebar.header("Filters")

district = st.sidebar.selectbox(
    "Select District",
    ["All"] + list(df["District"].unique())
)

theme = st.sidebar.selectbox(
    "Select Theme",
    ["All"] + list(df["Theme"].unique())
)

filtered_df = df.copy()

if district != "All":
    filtered_df = filtered_df[
        filtered_df["District"] == district
    ]

if theme != "All":
    filtered_df = filtered_df[
        filtered_df["Theme"] == theme
    ]

# ------------------------
# Metrics
# ------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Cafes",
    len(filtered_df)
)

col2.metric(
    "Average Rating",
    round(filtered_df["Rating"].mean(), 2)
)

col3.metric(
    "Total Reviews",
    int(filtered_df["ReviewCount"].sum())
)

# ------------------------
# Data Table
# ------------------------

st.subheader("Cafe Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ------------------------
# Scatter Plot
# ------------------------

st.subheader("Rating vs Review Count")

fig = px.scatter(
    filtered_df,
    x="Rating",
    y="ReviewCount",
    color="Theme",
    hover_name="Cafe",
    size="ReviewCount",
    title="Cafe Popularity Analysis"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------------
# Pie Chart
# ------------------------

st.subheader("Theme Distribution")

theme_count = (
    filtered_df["Theme"]
    .value_counts()
    .reset_index()
)

theme_count.columns = [
    "Theme",
    "Count"
]

fig2 = px.pie(
    theme_count,
    names="Theme",
    values="Count",
    title="Theme Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ------------------------
# Summary
# ------------------------

st.subheader("Dashboard Summary")

st.write(
    """
    This dashboard helps users compare cafes
    based on ratings, review counts, and themes.

    Users can quickly identify highly-rated cafes,
    popular districts, and customer-preferred themes.
    """
)
