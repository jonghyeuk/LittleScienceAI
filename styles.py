# styles.py

import streamlit as st

# 반드시 맨 위에서 바로 실행되도록!
st.set_page_config(
    page_title="Little Science AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def set_custom_page_style():
    st.markdown(
        """
        <style>
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                padding: 0.6em 1.2em;
                font-size: 1em;
                border-radius: 6px;
                border: none;
            }
            .stMarkdown, .stTextInput {
                font-family: 'Nanum Gothic', sans-serif;
                font-size: 1.05em;
            }
            .block-container {
                padding-top: 3rem;
                padding-bottom: 3rem;
                max-width: 800px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

