# styles.py

import streamlit as st

def set_custom_page_style():
    st.markdown(
        """
        <style>
            .reportview-container {
                padding: 2rem 5rem;
                background-color: #f8f9fa;
                font-family: 'Nanum Gothic', sans-serif;
            }
            h1, h2, h3 {
                color: #222831;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 0.5em 1em;
                margin-top: 10px;
            }
            .stMarkdown {
                max-width: 800px;
                margin: auto;
                padding: 2rem;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            }
        </style>
        """,
        unsafe_allow_html=True
    )
