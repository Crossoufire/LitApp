import pandas as pd
import plotly.express as px
import streamlit as st
from data import USData
import statsmodels.api as sm


st.set_page_config(
    page_title="US Retail Analysis",
    layout="wide",
    page_icon=":bar_chart:",
)

# Instantiate class for queries
DataClass = USData()

st.title("Analyzing US Retail From 1992 to 2020")
all_retails = DataClass.get_all_available_retails()

col, _ = st.columns([1, 1.3])
retail = col.selectbox(
    label="**Select a service**",
    options=all_retails,
)
st.write("---")

left_col, _, right_col = st.columns([1, 0.05, 1])
with left_col:
    st.write(f"### Sales Evolution for: {retail}")
    col, _, col2 = st.columns([1, 0.5, 1])
    rolling_window = col.slider("Moving Average (months)", min_value=1, max_value=24, value=12)
    col2.write("")
    col2.write("")
    hide = col2.checkbox("Show Moving Average Only", True)
    data = DataClass.get_retails_data_per_month(retail, rolling_window)
    with st.expander("Show dataframe"):
        st.dataframe(data, use_container_width=True)
    if hide:
        fig = px.line(data, x="Months-Year", y="Moving Average", height=541,
                      labels={"Moving Average": f"{rolling_window} Months Average"})
    else:
        fig = px.line(data, x="Months-Year", y=["Moving Average", "Sales Per Month"], height=541)
    st.plotly_chart(fig, use_container_width=True)

    st.write(f"### YoY% Growth Evolution for: {retail}")
    data = DataClass.get_retails_growth(retail)
    with st.expander("Show dataframe"):
        st.dataframe(data, use_container_width=True)
    fig = px.line(data, x="Year", y="Previous Year Growth (%)", height=600)
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

    st.write(f"### AutoCorrelation Plot for: {retail}")
    data = DataClass.get_retails_data_per_month(retail, 0)
    data["Months-Year"] = pd.to_datetime(data["Months-Year"])
    data.index = data["Months-Year"]
    acf = sm.tsa.acf(data["Sales Per Month"], nlags=12)
    fig = px.bar(x=range(len(acf)), y=acf, height=400, labels={"y": "Auto-correlation", "x": "Lag (year)"})
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.write(f"### Sales Baseline (%) Evolution for: {retail}")
    data = DataClass.get_retails_index_evolution(retail)
    st.write(f"Baseline based on the year {data['Year'][0]}: {data['Index'][0]} k$")
    with st.expander("Show dataframe"):
        st.dataframe(data, use_container_width=True)
    fig = px.line(data, x="Year", y="Evolution (%)", height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.write(f"### Monthly Seasonality for: {retail}")
    data = DataClass.get_retails_data_per_month(retail, 0)
    toggler = st.radio("Select visualization", options=["Heatmap", "Box Plot"])
    data["Months-Year"] = pd.to_datetime(data["Months-Year"])
    data["Month"] = data["Months-Year"].dt.strftime("%b")
    data["Year"] = data["Months-Year"].dt.year
    monthly_sales = data.pivot_table(index="Month", columns="Year", values="Sales Per Month", aggfunc="sum")
    months_ordered = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_sales = monthly_sales.reindex(months_ordered)
    with st.expander("Show dataframe"):
        st.dataframe(monthly_sales, use_container_width=True)
    if toggler == "Heatmap":
        fig = px.imshow(monthly_sales, labels={"color": "Sales"}, x=monthly_sales.columns, y=monthly_sales.index,
                        color_continuous_scale="Turbo", height=495)
    else:
        fig = px.box(monthly_sales)
    st.plotly_chart(fig, use_container_width=True)

    st.write(f"### Partial AutoCorrelation Plot for: {retail}")
    data = DataClass.get_retails_data_per_month(retail, 0)
    data["Months-Year"] = pd.to_datetime(data["Months-Year"])
    data.index = data["Months-Year"]
    pacf = sm.tsa.pacf(data["Sales Per Month"], nlags=12)
    fig2 = px.bar(x=range(len(pacf)), y=pacf, height=420, labels={"x": "Lag (year)", "y": "Partial Auto-correlation"})
    st.plotly_chart(fig2, use_container_width=True)
