import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Cafe Review Analysis Dashboard",
    page_icon="☕",
    layout="wide"
)

# -----------------------------
# Sample Dataset
# -----------------------------

data = {
    "Cafe":[
        "Blue Bottle Yeoksam",
        "Cafe Onion Seongsu",
        "Anthracite Hapjeong",
        "Layered Yeonnam",
        "Knotted Cheongdam",
        "Center Coffee",
        "Terarosa",
        "Fritz Coffee",
        "Coffee Libre",
        "Cafe Highwaist"
    ],

    "District":[
        "Gangnam",
        "Seongsu",
        "Hongdae",
        "Hongdae",
        "Gangnam",
        "Seongsu",
        "Jongno",
        "Jongno",
        "Hongdae",
        "Hongdae"
    ],

    "Theme":[
        "Study",
        "Instagram",
        "Study",
        "Dessert",
        "Dessert",
        "Study",
        "Study",
        "Traditional",
        "Specialty",
        "Instagram"
    ],

    "Rating":[
        4.8,
        4.9,
        4.7,
        4.6,
        4.8,
        4.7,
        4.8,
        4.6,
        4.8,
        4.7
    ],

    "ReviewCount":[
        1520,
        2450,
        1310,
        1890,
        2760,
        980,
        1180,
        1120,
        1040,
        1650
    ],

    "Keyword":[
        "quiet",
        "bakery",
        "workspace",
        "dessert",
        "sweet",
        "focus",
        "comfortable",
        "traditional",
        "quality",
        "photo"
    ]
}

df = pd.DataFrame(data)

# -----------------------------
# Title
# -----------------------------

st.title("☕ Cafe Review Analysis Dashboard")

st.markdown(
"""
Explore cafe ratings, review trends,
and customer preferences through interactive visualizations.
"""
)

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("Filter Options")

district_filter = st.sidebar.multiselect(
    "District",
    options=df["District"].unique(),
    default=df["District"].unique()
)

theme_filter = st.sidebar.multiselect(
    "Theme",
    options=df["Theme"].unique(),
    default=df["Theme"].unique()
)

search_cafe = st.sidebar.text_input(
    "Search Cafe"
)

filtered_df = df[
    (df["District"].isin(district_filter))
    &
    (df["Theme"].isin(theme_filter))
]

if search_cafe:
    filtered_df = filtered_df[
        filtered_df["Cafe"]
        .str.contains(search_cafe, case=False)
    ]

# -----------------------------
# Metrics
# -----------------------------

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Total Cafes",
    len(filtered_df)
)

col2.metric(
    "Average Rating",
    round(filtered_df["Rating"].mean(),2)
)

col3.metric(
    "Total Reviews",
    int(filtered_df["ReviewCount"].sum())
)

col4.metric(
    "Popular Theme",
    filtered_df["Theme"].mode()[0]
)

st.divider()

# -----------------------------
# Dataset
# -----------------------------

st.subheader("Cafe Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -----------------------------
# Scatter Plot
# -----------------------------

st.subheader("Rating vs Review Count")

fig = px.scatter(
    filtered_df,
    x="Rating",
    y="ReviewCount",
    color="Theme",
    size="ReviewCount",
    hover_name="Cafe"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# District Chart
# -----------------------------

col1,col2 = st.columns(2)

with col1:

    district_rating = (
        filtered_df
        .groupby("District")["Rating"]
        .mean()
        .reset_index()
    )

    fig2 = px.bar(
        district_rating,
        x="District",
        y="Rating",
        title="Average Rating by District"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

with col2:

    theme_count = (
        filtered_df["Theme"]
        .value_counts()
        .reset_index()
    )

    theme_count.columns=[
        "Theme",
        "Count"
    ]

    fig3 = px.pie(
        theme_count,
        names="Theme",
        values="Count"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# -----------------------------
# Keyword Analysis
# -----------------------------

st.subheader("Popular Review Keywords")

keyword_count = (
    filtered_df["Keyword"]
    .value_counts()
    .reset_index()
)

keyword_count.columns = [
    "Keyword",
    "Count"
]

fig4 = px.bar(
    keyword_count,
    x="Keyword",
    y="Count"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# -----------------------------
# Top Reviewed Cafes
# -----------------------------

st.subheader("Top Reviewed Cafes")

top_reviewed = (
    filtered_df
    .sort_values(
        by="ReviewCount",
        ascending=False
    )
)

st.dataframe(
    top_reviewed,
    use_container_width=True
)

# -----------------------------
# Insights
# -----------------------------

st.subheader("Dashboard Insights")

st.success(
f"""
Total Cafes: {len(filtered_df)}

Average Rating: {round(filtered_df['Rating'].mean(),2)}

Total Reviews: {filtered_df['ReviewCount'].sum()}
"""
)
