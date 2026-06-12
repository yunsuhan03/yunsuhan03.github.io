import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Cafe Review Analysis Dashboard",
    layout="wide"
)

st.title("☕ Cafe Review Analysis Dashboard")

# Sample Data
df = pd.DataFrame({
    "Cafe": [
        "Cafe A",
        "Cafe B",
        "Cafe C",
        "Cafe D",
        "Cafe E"
    ],
    "District": [
        "Gangnam",
        "Jongno",
        "Mapo",
        "Gangnam",
        "Seodaemun"
    ],
    "Theme": [
        "GoodToStudy",
        "DessertCafe",
        "Instagrammable",
        "GoodToStudy",
        "DessertCafe"
    ],
    "Rating": [
        4.8,
        4.5,
        4.7,
        4.3,
        4.6
    ],
    "ReviewCount": [
        530,
        320,
        480,
        210,
        410
    ],
    "Address": [
        "Gangnam-gu",
        "Jongno-gu",
        "Mapo-gu",
        "Gangnam-gu",
        "Seodaemun-gu"
    ],
    "Menu": [
        "Latte",
        "Cheesecake",
        "Coffee",
        "Americano",
        "Tiramisu"
    ],
    "Summary": [
        "Great for studying",
        "Best desserts",
        "Nice atmosphere",
        "Quiet space",
        "Popular cafe"
    ]
})

# Sidebar
st.sidebar.header("Filter Options")

district = st.sidebar.selectbox(
    "Select District",
    ["All"] + list(df["District"].unique())
)

theme = st.sidebar.multiselect(
    "Select Theme",
    df["Theme"].unique(),
    default=df["Theme"].unique()
)

filtered_df = df.copy()

if district != "All":
    filtered_df = filtered_df[
        filtered_df["District"] == district
    ]

filtered_df = filtered_df[
    filtered_df["Theme"].isin(theme)
]

# Dataset
st.subheader("Cafe Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# Scatter Plot
st.subheader("Rating vs Review Count")

fig = px.scatter(
    filtered_df,
    x="Rating",
    y="ReviewCount",
    color="Theme",
    hover_name="Cafe",
    size="ReviewCount"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Pie Chart
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
    values="Count"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# Metrics
st.subheader("Summary")

st.metric(
    "Total Cafes",
    len(filtered_df)
)

st.metric(
    "Average Rating",
    round(filtered_df["Rating"].mean(), 2)
)
