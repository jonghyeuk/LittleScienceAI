import streamlit as st

def set_custom_page_style():
    # 페이지 설정 (이 함수는 앱 시작 시 가장 먼저 호출되어야 함)
    st.set_page_config(page_title="Little Science AI", layout="wide")

    # 사용자 정의 CSS 스타일
    st.markdown("""
        <style>
            html, body {
                font-family: 'Nanum Gothic', sans-serif;
                background-color: #f5f7fa;
            }

            .reportview-container .main {
                padding: 2rem 4rem;
            }

            h1, h2, h3 {
                color: #3b3b3b;
            }

            .stButton>button {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 0.6em 1.2em;
                border: none;
            }

            .stButton>button:hover {
                background-color: #45a049;
                color: white;
            }

            .stMarkdown {
                line-height: 1.6;
            }
        </style>
    """, unsafe_allow_html=True)
