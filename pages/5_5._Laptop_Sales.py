import os
import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Laptop Sales",
    layout="wide",
    page_icon=":bar_chart:",
)


pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)
month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


laptop_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../datasets/LaptopSales.csv"))

laptop_df["Date"] = pd.to_datetime(laptop_df["Date"])
laptop_df["Month"] = laptop_df["Date"].dt.month_name()
laptop_df["Week"] = laptop_df["Date"].dt.isocalendar().week
laptop_df["Day"] = laptop_df["Date"].dt.day_name()
group_month_df = laptop_df.groupby(["Month"])["Retail Price"].sum()
group_month_df = group_month_df.reindex(month_order)
group_week_df = laptop_df.groupby(["Week"])["Retail Price"].sum()
group_day_df = laptop_df.groupby(["Day"])["Retail Price"].sum()
group_day_df = group_day_df.reindex(day_order)
laptop_df["Config_bin"] = pd.cut(laptop_df["Configuration"], bins=10)
config_df = laptop_df.groupby(["Config_bin"])["Retail Price"].mean().reset_index()
config_df["Config_bin"] = config_df["Config_bin"].astype(str)
stores_df = laptop_df.groupby(["Store Postcode"])["Retail Price"].agg(["sum", "mean"]).reset_index()


st.write("## Laptop Sales in 2008")
expander = st.expander("Show Dataframe description")
expander.write(laptop_df.describe())

col, col2 = st.columns([1, 1])
with col:
    tabs = st.tabs(["Mean Retail Price", "Month", "Week", "Day"])
    with tabs[0]:
        fig = px.histogram(laptop_df, x="Retail Price", nbins=50, title="Distribution of Laptop selling price")
        st.plotly_chart(fig, use_container_width=True)
    with tabs[1]:
        fig = px.bar(group_month_df, y="Retail Price", title="Laptop selling price 2008", height=600)
        st.plotly_chart(fig, use_container_width=True)
    with tabs[2]:
        fig = px.bar(group_week_df, y="Retail Price", title="Laptop selling price 2008", height=600)
        st.plotly_chart(fig, use_container_width=True)
    with tabs[3]:
        fig = px.bar(group_day_df, y="Retail Price", title="Laptop selling price 2008", height=600)
        st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(stores_df, x="Store Postcode", y="mean", labels={"mean": "Mean Retail Price"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(config_df, x="Config_bin", y="Retail Price", title="Price change with configuration", height=500,
                 labels={"Config_bin": "Configurations (binned)", "Retail Price": "Mean Retail Price"})
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(stores_df, x="Store Postcode", y="sum", labels={"sum": "Sum of Retail Price"})
    st.plotly_chart(fig, use_container_width=True)
