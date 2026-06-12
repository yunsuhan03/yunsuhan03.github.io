import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# Page Config
# ----------------------------------

st.set_page_config(
    page_title="Cafe Review Dashboard",
    layout="wide"
)

st.title("☕ Cafe Review Analysis Dashboard")

st.write(
    """
    Explore cafe ratings, review counts,
    themes, and customer preferences.
    """
)

# ----------------------------------
# Sample Dataset
# ----------------------------------

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
        "Jamsil",
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
        4.2,
        4.6
    ],

    "ReviewCount": [
        500,
        320,
        410,
        280,
        390
    ]
}

df = pd.DataFrame(data)

# ----------------------------------
# Sidebar Filters
# ----------------------------------

st.sidebar.header("Filter Options")

district = st.sidebar.selectbox(
    "Select District",
    ["All"] + list(df["District"].unique())
)

theme = st.sidebar.selectbox(
    "Select Theme",
    ["All"] + list(df["Theme"].unique())
)

# ----------------------------------
# Filtering
# ----------------------------------

filtered_df = df.copy()

if district != "All":
    filtered_df = filtered_df[
        filtered_df["District"] == district
    ]

if theme != "All":
    filtered_df = filtered_df[
        filtered_df["Theme"] == theme
    ]

# ----------------------------------
# Metrics
# ----------------------------------

st.subheader("Summary")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Average Rating",
        round(filtered_df["Rating"].mean(), 2)
    )

with col2:
    st.metric(
        "Total Cafes",
        len(filtered_df)
    )

# ----------------------------------
# Data Table
# ----------------------------------

st.subheader("Cafe Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ----------------------------------
# Scatter Plot
# ----------------------------------

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

# ----------------------------------
# Pie Chart
# ----------------------------------

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
)        "Best desserts",
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
