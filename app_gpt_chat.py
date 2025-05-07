import streamlit as st
import pandas as pd
import openai
from openai import OpenAI
from prompts import generate_overview_prompt
from styles import set_custom_page_style
from utils import create_pdf, similarity

# ✅ 환경 설정
set_custom_page_style()
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ✅ 세션 초기화
if "step" not in st.session_state:
    st.session_state.step = 1

# ✅ 데이터 불러오기
@st.cache_data
def load_db():
    df = pd.read_excel("ISEF Final DB.xlsx")
    df = df.dropna(subset=["Project Title"])
    return df

df = load_db()

# ✅ GPT 분석 함수
def get_overview_from_gpt(keyword: str) -> str:
    prompt = generate_overview_prompt(keyword)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ✅ 타이틀
st.markdown("""
    <h1 style='text-align: center;'>🔬 Little Science AI</h1>
    <p style='text-align: center;'>과학 소논문 주제를 AI로 탐색하고 설계하는 도우미입니다.</p>
    <hr>
""", unsafe_allow_html=True)

# ✅ STEP 1: 주제 입력
if st.session_state.step == 1:
    st.markdown("### 🧠 탐구 주제 입력")
    keyword = st.text_input("관심 있는 과학 키워드를 입력하세요 (예: 꿀벌, 효소 반응 등)")
    if keyword:
        st.session_state.keyword = keyword
        st.session_state.step = 2
        st.rerun()

# ✅ STEP 2: GPT 분석 + 유사 DB 출력
elif st.session_state.step == 2:
    st.markdown("### 🧪 주제 분석 결과")
    with st.spinner("GPT가 주제를 분석 중입니다..."):
        keyword = st.session_state.keyword
        overview = get_overview_from_gpt(keyword)
        st.session_state.gpt_analysis = overview
        df["similarity"] = df["Project Title"].apply(lambda x: similarity(keyword, x))
        st.session_state.similar = df.sort_values("similarity", ascending=False).head(5)

    st.markdown(f"<div style='background-color:#f9f9f9;padding:1em;border-radius:8px;'>{overview}</div>", unsafe_allow_html=True)

    st.markdown("### 📁 유사한 과학 주제")
    for _, row in st.session_state.similar.iterrows():
        st.markdown(f"- {row['Project Title']} ({row['Year']})")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 더 깊이 분석하기"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("🔁 처음으로"):
            st.session_state.step = 1
            st.rerun()

# ✅ STEP 3: 심화 분석 + PDF 저장
elif st.session_state.step == 3:
    st.markdown("### 📄 주제 심화 분석")
    st.markdown("GPT 기반 분석을 바탕으로 작성된 예시입니다. 실제 보고서로 사용 시 전문가의 검토가 필요합니다.")
    st.markdown(st.session_state.gpt_analysis)

    if st.button("📄 PDF 저장"):
        file_path = create_pdf(st.session_state.gpt_analysis)
        with open(file_path, "rb") as f:
            st.download_button("📥 PDF 다운로드", f, file_name="소논문_설계_가이드.pdf")

    if st.button("🔁 처음으로 돌아가기"):
        st.session_state.step = 1
        st.rerun()

