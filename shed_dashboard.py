import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
df = pd.read_excel("shed_sample_filtered_updated.xlsx")
df["Company Name"] = df["Company Name"].str.strip()

# Page Setup
st.set_page_config(page_title="Shed Comparison Dashboard", layout="wide")
st.markdown("## 🏠 Wright County Shed Storage Comparison")

# Sidebar
st.sidebar.title("🔍 Filter Options")
all_companies = sorted(df["Company Name"].unique())
if "selected_companies" not in st.session_state:
    st.session_state.selected_companies = all_companies.copy()

# Buttons
col1, col2 = st.sidebar.columns([1, 1])
if col1.button("✅ Select All"):
    st.session_state.selected_companies = all_companies.copy()
if col2.button("🚫 Deselect All"):
    st.session_state.selected_companies = []

# Multiselect
selected = st.sidebar.multiselect(
    "Choose companies to include:",
    options=all_companies,
    default=st.session_state.selected_companies,
)
filtered_df = df[df["Company Name"].isin(selected)]

# Toggle between price modes
price_mode = st.sidebar.radio("Scatter Plot Y-axis", ["Price/Month ($)", "Price per Sq Ft"])

# Tabs
tab1, tab2 = st.tabs(["📊 Visualizations", "📋 Full Data Table"])

with tab1:
    st.markdown("### 📈 Scatter Plot: Size vs Price")

    fig_scatter = px.scatter(
        filtered_df,
        x="Square Feet",
        y=price_mode,
        color="Company Name",
        hover_data=["Unit Size (ft)", "Price/Month ($)", "Price per Sq Ft"],
        title=f"{price_mode} vs Shed Size",
        height=500,
        template="simple_white"
    )
    fig_scatter.update_traces(marker=dict(size=10, opacity=0.7), selector=dict(mode='markers'))
    fig_scatter.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("### 📊 Bar Chart: Avg Price per Sq Ft by Company")

    avg_price_sqft = (
        filtered_df.groupby("Company Name")["Price per Sq Ft"]
        .mean()
        .sort_values()
        .reset_index()
    )

    fig_bar = px.bar(
        avg_price_sqft,
        x="Price per Sq Ft",
        y="Company Name",
        orientation="h",
        title="Average Price per Sq Ft",
        height=500,
        template="simple_white"
    )
    fig_bar.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### 🏆 Best Value Companies (Lowest $/SqFt)")
    st.dataframe(avg_price_sqft.head(5), use_container_width=True)

    st.download_button(
        "📥 Download Filtered Data as CSV",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_shed_data.csv",
        mime="text/csv"
    )

with tab2:
    st.markdown("### 📋 Filterable Shed Data Table")
    st.dataframe(filtered_df, use_container_width=True)
