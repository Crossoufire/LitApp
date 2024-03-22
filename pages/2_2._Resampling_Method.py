import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import scipy.stats as stats


st.set_page_config(
    page_title="Resampling method",
    layout="wide",
    page_icon=":bar_chart:",
)


def calculate_permutations(combined_data: np.array, permutations: int):
    """ Function calculating the permutations and return the mean difference """

    col, _ = st.columns([1, 2])

    with col:
        permuted_mean_diff = []
        progress_bar = st.progress(0)
        for i in range(permutations):
            np.random.shuffle(combined_data)
            permuted_group_A = combined_data[:len(data["Group_A"])]
            permuted_group_B = combined_data[len(data["Group_B"]):]
            mean_diff = np.mean(permuted_group_A) - np.mean(permuted_group_B)
            permuted_mean_diff.append(mean_diff)
            progress_bar.progress((i + 1) / permutations, text="Creating permutations...")
        time.sleep(0.5)
        progress_bar.empty()

    return permuted_mean_diff


def v_spacer(height: int, sidebar: bool = False):
    """ Create N vertical spaces """

    for _ in range(height):
        if sidebar:
            st.sidebar.write("\n")
        else:
            st.write("\n")


st.write("## The resampling method: two groups analysis")
st.divider()
st.write("""
- Presented below are the scores of two groups: `Group A` and `Group B`
- These groups were instructed using distinct methods: `Method A` and `Method B`
- The null hypothesis is that there is no difference between the two groups
- The alternative hypothesis is that `Method A` outperforms `Method B`
""")

col, _ = st.columns([1, 3])
with col:
    with st.expander("Show each group scores (editable)"):
        data = pd.DataFrame({
            "Group_A": [95, 79, 92, 95, 78, 92, 98, 100, 100, 100, 100],
            "Group_B": [75, 92, 92, 92, 92, 92, 92, 92, 92, 78, 48],
        })
        editable_df = st.data_editor(data, num_rows="dynamic", use_container_width=True)

obs_mean_diff = np.mean(editable_df["Group_A"]) - np.mean(editable_df["Group_B"])
metric = st.metric("Observed mean score difference", f"{obs_mean_diff:.2f} points")

st.write("""
##### Is this mean score difference significant?
1. Combine the results from the two different groups into a single dataset
2. Shuffle the combined data and then randomly draw (without replacement) a resample of the same size as `Group A`
3. From the remaining data, randomly draw (without replacement) a resample of the same size as `Group B`
4. You have now collected one set of resamples mirroring the sizes of the original groups
5. Calculate the mean difference for the resamples, and keep them. This constitutes one permutation iteration
6. Repeat the previous steps `R` times to yield a permutation distribution of the test statistic
""")
st.divider()

col, _ = st.columns([1, 5])
permutations = col.number_input("Number of permutations", min_value=1, max_value=100000, value=1000, step=1)

start_button = st.button("Start calculation")
if start_button:
    combined_data = np.concatenate([editable_df["Group_A"], editable_df["Group_B"]])
    permuted_mean_diff = calculate_permutations(combined_data, permutations)
    st.write("### Distribution of the mean score difference distribution under the null hypothesis")
    fig = px.histogram(x=permuted_mean_diff, nbins=50)
    fig.add_vline(x=obs_mean_diff, line_dash="dash", line_color="red", annotation_text="Obs mean diff")

    # noinspection PyUnresolvedReferences
    methods = {
        "Levene": stats.levene(editable_df["Group_A"], editable_df["Group_B"])[1],
        "Shapiro gA": stats.shapiro(editable_df["Group_A"])[1],
        "Shapiro gB": stats.shapiro(editable_df["Group_B"])[1],
        "T-test": stats.ttest_ind(editable_df["Group_A"], editable_df["Group_B"])[1],
        "Resampling": np.sum(np.abs(permuted_mean_diff) >= np.abs(obs_mean_diff)) / permutations,
    }
    p_values = {
        "Method": ["Levene", "Shapiro group A", "Shapiro group B", "T-test", "Resampling"],
        "p-value": [*methods.values()],
        "Status": [
            "✔️" if methods["Levene"] > 0.05 else "❌",
            "✔️" if methods["Shapiro gA"] > 0.05 else "❌",
            "✔️" if methods["Shapiro gB"] > 0.05 else "❌",
            "✔️" if (methods["T-test"] < 0.05 < methods["Levene"] and methods["Shapiro gA"] > 0.05
                     and methods["Shapiro gB"] > 0.05) else "❌",
            "✔️" if methods["Resampling"] < 0.05 else "❌",
        ],
        "Information": [
            "Groups from same variance population",
            "Group A drawn from Normal distribution",
            "Group B drawn from Normal distribution",
            "Reject null hypothesis (Levene & Shapiro OK)",
            "Reject null hypothesis (Non-parametric)",
        ]
    }

    col1, _, col2 = st.columns([1, 0.05, 1])
    col1.plotly_chart(fig, use_container_width=True)
    with col2:
        v_spacer(5)
        st.write("#### Different tests")
        st.dataframe(p_values, hide_index=True, use_container_width=True)


# --- Categorical Resampling ----------------------------------------------------------

# def perm_fun(x: pd.Series, nB: int):
#     idx_B = np.random.choice(x.index, nB, replace=False)
#     idx_A = np.logical_not(np.isin(x.index, idx_B))
#
#     mean_B = x.loc[idx_B].mean()
#     mean_A = x.loc[idx_A].mean()
#
#     return mean_B - mean_A

# nB = 22588
# box_total = pd.Series([1] * 382 + [0] * 45945)
# num_resamples = 1000
# permuted_differences = []
# for _ in tqdm(range(num_resamples), ncols=70):
#     permuted_differences.append(100 * perm_fun(box_total, nB))

# fig = px.histogram(x=permuted_differences, nbins=50)
# fig.add_vline(x=0.0368, line_dash="dash", line_color="red")
# st.plotly_chart(fig)
# obs_pct_diff = 100 * (200 / 23739 - 182 / 22588)
# st.write(f"Observed difference: {obs_pct_diff:.4f}%")
# st.write(f"P-value = {np.mean([diff > obs_pct_diff for diff in permuted_differences]):.4f}")
