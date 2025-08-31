# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------- SAMPLE DATA GENERATION -----------------
def generate_sample_data():
    np.random.seed(42)
    years = [2022, 2023, 2024, 2025]
    quarters = [1, 2, 3, 4]
    crops = ["Maize", "Rice", "Groundnut", "Millet", "Cassava"]

    data = []
    for year in years:
        for q in quarters:
            for crop in crops:
                production = np.random.randint(500, 5000)  # tons
                area = np.random.randint(100, 1000)       # hectares
                yield_rate = round(production / area, 2)  # tons per hectare
                farmers = np.random.randint(50, 500)      # number of farmers
                data.append([year, q, crop, production, area, yield_rate, farmers])

    df = pd.DataFrame(data, columns=["Year", "Quarter", "Crop", "Production", "Area", "Yield", "Farmers"])
    return df

df = generate_sample_data()

# ----------------- STREAMLIT DASHBOARD -----------------
st.set_page_config(page_title="Agriculture Data Dashboard", layout="wide")

st.title("🌾 Agriculture Monitoring Dashboard")
st.markdown("Track agricultural performance across **years and quarters**")

# Sidebar filters
st.sidebar.header("Filters")
year_filter = st.sidebar.multiselect("Select Year(s)", options=df["Year"].unique(), default=df["Year"].unique())
quarter_filter = st.sidebar.multiselect("Select Quarter(s)", options=df["Quarter"].unique(), default=df["Quarter"].unique())
crop_filter = st.sidebar.multiselect("Select Crop(s)", options=df["Crop"].unique(), default=df["Crop"].unique())

# Apply filters
filtered_df = df[(df["Year"].isin(year_filter)) & (df["Quarter"].isin(quarter_filter)) & (df["Crop"].isin(crop_filter))]

# ----------------- KPI SECTION -----------------
st.subheader("📌 Key Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Production (tons)", f"{filtered_df['Production'].sum():,}")
with col2:
    st.metric("Total Area (ha)", f"{filtered_df['Area'].sum():,}")
with col3:
    st.metric("Average Yield (tons/ha)", f"{filtered_df['Yield'].mean():.2f}")
with col4:
    st.metric("Total Farmers", f"{filtered_df['Farmers'].sum():,}")

# ----------------- VISUALIZATIONS -----------------
st.subheader("📊 Visualizations")

# Production by crop
fig1 = px.bar(filtered_df, x="Crop", y="Production", color="Crop", barmode="group",
              title="Production by Crop", text_auto=True)
st.plotly_chart(fig1, use_container_width=True)

# Yearly trend
fig2 = px.line(filtered_df.groupby(["Year", "Quarter"]).sum().reset_index(),
               x="Quarter", y="Production", color="Year", markers=True,
               title="Quarterly Production Trend")
st.plotly_chart(fig2, use_container_width=True)

# Yield comparison
fig3 = px.box(filtered_df, x="Crop", y="Yield", color="Crop",
              title="Yield Distribution per Crop")
st.plotly_chart(fig3, use_container_width=True)

# Farmers distribution
fig4 = px.pie(filtered_df, names="Crop", values="Farmers", title="Farmers Involved per Crop")
st.plotly_chart(fig4, use_container_width=True)

# ----------------- DATA TABLE -----------------
st.subheader("📂 Data Table")
st.dataframe(filtered_df)

# Download button
st.download_button("📥 Download Filtered Data", data=filtered_df.to_csv(index=False).encode("utf-8"),
                   file_name="agriculture_data.csv", mime="text/csv")
