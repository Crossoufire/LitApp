import streamlit as st


st.set_page_config(
    page_title="My Analysis App",
    layout="wide",
    page_icon=":bar_chart:",
)

st.sidebar.success("Select an Analysis")
st.sidebar.markdown(
    f"""
    <style>
        [data-testid="stSidebarNav"] > ul {{
            min-height: {37}vh;
        }} 
    </style>
    """,
    unsafe_allow_html=True,
)


st.write("""
    <div style="background-color: #111827; padding: 10px; border-radius: 10px; text-align: center; 
    margin-bottom: 30px;">
        <h1>Welcome to My Analysis Streamlit App! 👋</h1>
        <h4>Created by <a href="https://github.com/Crossoufire">Vincent Delmas</a></h4>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    #### This app display analysis on various subjects including
    - Analysis of US retail and food services sectors
    - The statistical resampling method
    - etc...
""")
