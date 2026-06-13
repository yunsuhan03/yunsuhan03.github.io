import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Cafe Review Analysis Dashboard",
    page_icon="☕",
    layout="wide"
)

# --------------------------------------------------
# Real Seoul Cafe Dataset
# --------------------------------------------------

data = {

    "Cafe":[
        "Cafe Onion Anguk",
        "Fritz Coffee Dohwa",
        "Coffee Hanyakbang",
        "Thanks Nature Cafe",
        "Fritz Coffee Wonseo",
        "Center Coffee Gwanghwamun",
        "Cafe Pokpo",
        "The Spot Fabulous",
        "Cafe Coin",
        "Cheongsudang Bakery"
    ],

    "District":[
        "Jongno",
        "Mapo",
        "Jung-gu",
        "Hongdae",
        "Jongno",
        "Jung-gu",
        "Seodaemun",
        "Jung-gu",
        "Jung-gu",
        "Jongno"
    ],

    "Theme":[
        "Instagram",
        "Study",
        "Traditional",
        "Animal",
        "Study",
        "Specialty",
        "Nature",
        "Instagram",
        "Dessert",
        "Dessert"
    ],

    "Rating":[
        4.2,
        4.3,
        4.5,
        4.5,
        4.4,
        4.4,
        4.4,
        4.2,
        4.4,
        4.3
    ],

    "ReviewCount":[
        4519,
        2842,
        2361,
        980,
        867,
        797,
        956,
        1174,
        686,
        1472
    ],

    "Keyword":[
        "bakery",
        "workspace",
        "vintage",
        "animals",
        "quiet",
        "specialty",
        "nature",
        "photo",
        "cake",
        "dessert"
    ]
}

df = pd.DataFrame(data)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("☕ Cafe Review Analysis Dashboard")

st.markdown(
"""
Explore cafe ratings, review trends,
and customer preferences through interactive visualizations.
"""
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Filter Options")

district_filter = st.sidebar.multiselect(
    "Select District",
    options=sorted(df["District"].unique()),
    default=sorted(df["District"].unique())
)

theme_filter = st.sidebar.multiselect(
    "Select Theme",
    options=sorted(df["Theme"].unique()),
    default=sorted(df["Theme"].unique())
)

search_cafe = st.sidebar.text_input(
    "Search Cafe"
)

# --------------------------------------------------
# Filter Data
# --------------------------------------------------

filtered_df = df[
    (df["District"].isin(district_filter))
    &
    (df["Theme"].isin(theme_filter))
]

if search_cafe:
    filtered_df = filtered_df[
        filtered_df["Cafe"].str.contains(
            search_cafe,
            case=False
        )
    ]

# --------------------------------------------------
# KPI Section
# --------------------------------------------------

st.subheader("Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

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
    f"{filtered_df['ReviewCount'].sum():,}"
)

col4.metric(
    "Popular Theme",
    filtered_df["Theme"].mode()[0]
    if not filtered_df.empty
    else "-"
)

st.divider()

# --------------------------------------------------
# Dataset Table
# --------------------------------------------------

st.subheader("Cafe Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# --------------------------------------------------
# Scatter Plot
# --------------------------------------------------

st.subheader("Rating vs Review Count")

fig1 = px.scatter(
    filtered_df,
    x="Rating",
    y="ReviewCount",
    color="Theme",
    size="ReviewCount",
    hover_name="Cafe",
    title="Cafe Popularity Analysis"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# --------------------------------------------------
# Charts
# --------------------------------------------------

col1, col2 = st.columns(2)

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

    theme_count.columns = [
        "Theme",
        "Count"
    ]

    fig3 = px.pie(
        theme_count,
        names="Theme",
        values="Count",
        title="Theme Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# --------------------------------------------------
# Keyword Analysis
# --------------------------------------------------

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
    y="Count",
    title="Keyword Trends"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# --------------------------------------------------
# Top Reviewed Cafes
# --------------------------------------------------

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

# --------------------------------------------------
# Insights
# --------------------------------------------------

st.subheader("Dashboard Insights")

if not filtered_df.empty:

    best_cafe = filtered_df.loc[
        filtered_df["Rating"].idxmax()
    ]["Cafe"]

    st.success(
        f"""
        Total Cafes Analyzed: {len(filtered_df)}

        Average Rating: {round(filtered_df['Rating'].mean(),2)}

        Total Reviews: {filtered_df['ReviewCount'].sum():,}

        Highest Rated Cafe: {best_cafe}
        """
    )

else:

    st.warning(
        "No cafes match the selected filters."
    )
