import streamlit as st

def set_custom_styles():
    st.markdown("""
        <style>
        /* 전체 블록 가운데 정렬 */
        .main .block-container {
            max-width: 800px;
            margin: 0 auto;
            padding-top: 2rem;
        }

        /* 제목 간격 조절 */
        h1, h2, h3 {
            margin-bottom: 1rem;
        }

        /* 버튼 여백 */
        .stButton > button {
            margin-top: 1rem;
            margin-bottom: 1.5rem;
        }

        /* 마크다운 텍스트 여백 */
        .stMarkdown {
            margin-bottom: 1.5rem;
        }

        /* 다운로드 버튼 정렬 */
        .stDownloadButton {
            text-align: center;
            margin: 1.5rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

