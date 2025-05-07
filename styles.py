# styles.py

import streamlit as st

def set_page_style():
    st.markdown("""
    <style>
    .reportview-container {
        padding: 2rem 4rem;
        background-color: #fdfdfd;
        font-family: 'Nanum Gothic', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.5em;
    }
    </style>
    """, unsafe_allow_html=True)

