import os
import pandas as pd
import streamlit as st
import plotly.express as px

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)


st.set_page_config(
    page_title="Riding Mowers",
    layout="wide",
    page_icon=":bar_chart:",
)

data_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../datasets/RidingMowers.csv"))


st.write("## Sales of Riding Mowers compared to lot size and income")
fig = px.scatter(data_df, x="Income", y="Lot_Size", color="Ownership", height=600,
                 labels={"Income": "Income (x1000 $)", "Lot_Size": "$Lot Size (ft<sup>2</sup>)"},
                 color_discrete_sequence=["green", "red"])
fig.update_traces(marker=dict(size=14, line=dict(width=1, color="black")))
fig.add_hline(y=19, line_color="black", line_width=3)
fig.add_vline(x=72, line_color="black", line_width=3)
st.plotly_chart(fig, use_container_width=True)
