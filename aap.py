import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Web Analytics", layout="wide")
st.title("📊 Modern Website Analytics Dashboard")

# 2. Optimized Data Loading
@st.cache_data
def get_analytics_data():
    df = pd.read_csv("analytics_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = get_analytics_data()

# 3. Sidebar Filters
st.sidebar.header("Dashboard Filters")
selected_source = st.sidebar.multiselect(
    "Select Traffic Source:",
    options=df["Traffic_Source"].unique(),
    default=df["Traffic_Source"].unique()
)

# Apply Filter
filtered_df = df[df["Traffic_Source"].isin(selected_source)]

# 4. KPI Top Metrics Cards
total_views = filtered_df["Page_Views"].sum()
avg_duration = filtered_df["Session_Duration"].mean()
total_conversions = filtered_df["Conversions"].sum()

col1, col2, col3 = st.columns(3)
col1.metric(label="Total Page Views", value=f"{total_views:,}")
col2.metric(label="Avg Session (Sec)", value=f"{avg_duration:.1f}s")
col3.metric(label="Total Conversions", value=f"{total_conversions:,}")

st.markdown("---")

# 5. Visualizations Layout
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Traffic Trends Over Time")
    trend_fig = px.line(
        filtered_df, x="Date", y="Page_Views", color="Traffic_Source",
        labels={"Page_Views": "Views"}, markers=True
    )
    st.plotly_chart(trend_fig, use_container_width=True)

with chart_col2:
    st.subheader("Device Distribution Share")
    pie_fig = px.pie(
        filtered_df, values="Page_Views", names="Device", 
        hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(pie_fig, use_container_width=True)
