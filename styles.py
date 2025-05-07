import streamlit as st

def set_custom_page_style():
    # ✅ 기본 페이지 레이아웃 설정
    st.set_page_config(
        page_title="Little Science AI",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # ✅ CSS 스타일 삽입: A4 중심 문서 스타일
    st.markdown("""
        <style>
            /* 전체 배경 및 텍스트 정렬 */
            .main {
                max-width: 800px;
                margin: 0 auto;
                padding: 2rem;
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            }

            /* 버튼 정렬 */
            div.stButton > button {
                width: 100%;
                border-radius: 8px;
                font-weight: bold;
                background-color: #4CAF50;
                color: white;
            }

            /* 경고 및 메시지 정돈 */
            .stAlert {
                font-size: 0.95rem;
            }

            /* Markdown 제목 여백 */
            h1, h2, h3 {
                margin-top: 2rem;
                margin-bottom: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)
