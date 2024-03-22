import os
import time
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="ANOVA",
    layout="wide",
    page_icon=":bar_chart:",
)

# Load dataset
data_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../datasets/FourSessions.csv"))


def perm_test(dataset: pd.DataFrame):
    data_copied = dataset.copy()
    data_randomized = np.random.permutation(data_copied["Time"].to_numpy())
    list_permuted = np.split(data_randomized, 4)

    return np.var([np.mean(permuted_page) for permuted_page in list_permuted], ddof=1)


st.write("# ANOVA by hand using a Permutation Test")
col, _ = st.columns([1, 4])
with col:
    expander = st.expander("Show dataframe")
    expander.dataframe(data_df, use_container_width=True)

observed_variance = data_df.groupby("Page").mean().var().iloc[0]
st.metric(label="Observed variance of mean", value=f"{observed_variance:.3f}")

launch_button = st.button("Launch Permutation Test")
if launch_button:
    progress_bar, perm_variance = st.progress(0), []
    for i in range(3000):
        perm_variance.append(perm_test(data_df))
        progress_bar.progress((i + 1) / 3000, text="Performing the permutations")
    time.sleep(0.5)
    progress_bar.empty()

    st.write("#### Distribution of the variance of groups mean under the null hypothesis")
    fig = px.histogram(x=perm_variance, nbins=50)
    fig.add_vline(x=observed_variance, line_dash="dash", line_color="red", annotation_text="Obs variance of mean")

    st.plotly_chart(fig)
    st.metric(label="Resulting p-value", value=f"{np.mean([var > observed_variance for var in perm_variance]):.3f}")
