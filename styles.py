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
        .title {
            font-size: 28px;
            font-weight: bold;
            color: #1a1a1a;
            margin-bottom: 20px;
        }
        .section-header {
            font-size: 20px;
            font-weight: 600;
            margin-top: 25px;
            color: #333333;
        }
        .content-block {
            font-size: 16px;
            line-height: 1.6;
            margin-top: 10px;
            white-space: pre-wrap;
        }
        </style>
    """, unsafe_allow_html=True)
