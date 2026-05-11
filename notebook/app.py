

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Professional Artist Dashboard",
    page_icon="🎨",
    layout="wide"
)

st.markdown("""
<style>

body {
    background-color: #0B0F19;
}

.main {
    background: linear-gradient(to bottom right, #0B0F19, #111827);
    color: white;
}

h1 {
    font-size: 55px !important;
    font-weight: bold;
    color: #ffffff;
}

h2, h3 {
    color: #facc15;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1E3A8A, #7C3AED);
    padding: 20px;
    border-radius: 20px;
    color: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

.stDataFrame {
    border-radius: 20px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #111827, #1F2937);
}

</style>
""", unsafe_allow_html=True)


df = pd.read_csv("Artists.csv")



st.markdown("""
# 🎨 Professional Artist Analytics Dashboard

### Discover Insights, Trends & Historical Artist Data
""")

st.markdown("---")


st.sidebar.title("🎛 Dashboard Controls")

# Gender Filter
if "Gender" in df.columns:

    gender_option = st.sidebar.selectbox(
        "Select Gender",
        ["All"] + list(df["Gender"].dropna().unique())
    )

else:
    gender_option = "All"

# Nationality Filter
if "Nationality" in df.columns:

    nationality_option = st.sidebar.selectbox(
        "Select Nationality",
        ["All"] + sorted(
            list(df["Nationality"].dropna().unique())
        )
    )

else:
    nationality_option = "All"

# ---------------------------------------------------------
# FILTERING
# ---------------------------------------------------------

filtered_df = df.copy()

if gender_option != "All":

    filtered_df = filtered_df[
        filtered_df["Gender"] == gender_option
    ]

if nationality_option != "All":

    filtered_df = filtered_df[
        filtered_df["Nationality"] == nationality_option
    ]

# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.subheader("📊 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "🎨 Total Artists",
        len(filtered_df)
    )

with col2:

    if "Nationality" in filtered_df.columns:

        st.metric(
            "🌍 Nationalities",
            filtered_df["Nationality"].nunique()
        )

with col3:

    if "Gender" in filtered_df.columns:

        st.metric(
            "👥 Gender Types",
            filtered_df["Gender"].nunique()
        )

with col4:

    st.metric(
        "📂 Columns",
        len(filtered_df.columns)
    )

st.markdown("---")

# ---------------------------------------------------------
# CHARTS
# ---------------------------------------------------------

left_col, right_col = st.columns(2)

# ---------------------------------------------------------
# GENDER PIE CHART
# ---------------------------------------------------------

with left_col:

    if "Gender" in filtered_df.columns:

        st.subheader("👨‍🎨 Gender Distribution")

        gender_counts = (
            filtered_df["Gender"]
            .value_counts()
            .reset_index()
        )

        gender_counts.columns = ["Gender", "Count"]

        fig = px.pie(
            gender_counts,
            values="Count",
            names="Gender",
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Rainbow
        )

        fig.update_layout(
            paper_bgcolor="#111827",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ---------------------------------------------------------
# NATIONALITY BAR CHART
# ---------------------------------------------------------

with right_col:

    if "Nationality" in filtered_df.columns:

        st.subheader("🌍 Top Nationalities")

        nationality_counts = (
            filtered_df["Nationality"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        nationality_counts.columns = [
            "Nationality",
            "Count"
        ]

        fig = px.bar(
            nationality_counts,
            x="Nationality",
            y="Count",
            color="Count",
            color_continuous_scale="plasma"
        )

        fig.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.markdown("---")

# ---------------------------------------------------------
# BIRTH YEAR ANALYSIS
# ---------------------------------------------------------

if "BeginDate" in filtered_df.columns:

    st.subheader("📅 Artist Birth Year Trends")

    birth_years = pd.to_numeric(
        filtered_df["BeginDate"],
        errors="coerce"
    )

    fig = px.histogram(
        birth_years.dropna(),
        nbins=40,
        color_discrete_sequence=["#06B6D4"]
    )

    fig.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white",
        xaxis_title="Birth Year",
        yaxis_title="Artists"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# ---------------------------------------------------------
# LIFESPAN ANALYSIS
# ---------------------------------------------------------

if (
    "BeginDate" in filtered_df.columns
    and
    "EndDate" in filtered_df.columns
):

    st.subheader("⏳ Artist Lifespan Analysis")

    birth = pd.to_numeric(
        filtered_df["BeginDate"],
        errors="coerce"
    )

    death = pd.to_numeric(
        filtered_df["EndDate"],
        errors="coerce"
    )

    lifespan = death - birth

    avg_life = lifespan.mean()

    st.metric(
        "⭐ Average Lifespan",
        f"{avg_life:.1f} Years"
    )

    fig = px.histogram(
        lifespan.dropna(),
        nbins=30,
        color_discrete_sequence=["#F472B6"]
    )

    fig.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white",
        xaxis_title="Lifespan",
        yaxis_title="Artists"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")


if "DisplayName" in filtered_df.columns:

    st.subheader("🔍 Search Artist")

    search = st.text_input(
        "Enter Artist Name"
    )

    if search:

        results = filtered_df[
            filtered_df["DisplayName"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

        st.dataframe(
            results,
            use_container_width=True
        )

st.markdown("---")

st.subheader("📂 Full Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.markdown("""
<div style='text-align:center; padding:20px;'>

<h3 style='color:#9CA3AF;'>
🚀 Professional Dashboard Built with Streamlit & Plotly
</h3>

</div>
""", unsafe_allow_html=True)

