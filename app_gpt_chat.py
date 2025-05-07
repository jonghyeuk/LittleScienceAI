import streamlit as st
from styles import set_custom_page_style  # set_page_config already applied in styles.py
from prompts import generate_overview_prompt
from utils import create_pdf, similarity
import pandas as pd
import openai
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
prompt = f"""
사용자가 제시한 관심 주제: {st.session_state.keyword}
1. 이 주제의 주요 과학적 의미와 배경을 설명해주세요.
2. 관련된 사회/환경적 이슈가 있다면 알려주세요.
3. 고등학생 수준의 탐구 주제로 적절한 예시 3가지를 제시해주세요.
"""
if "keyword" in st.session_state:
    keyword = st.session_state.keyword
else:
    st.warning("📝 먼저 탐색할 주제를 입력해주세요.")
    st.stop()  # 이후 코드 실행 방지

messages = [{"role": "user", "content": prompt}]
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)

# --- Custom Styles ---
set_custom_page_style()

# --- API Key 설정 ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- 데이터 불러오기 ---
@st.cache_data
def load_db():
    df = pd.read_excel("ISEF Final DB.xlsx")
    df = df.dropna(subset=["Project Title"])
    return df

df = load_db()

# --- GPT 응답 함수 ---
def get_overview_from_gpt(keyword):
    prompt = generate_overview_prompt(keyword)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# --- Streamlit 앱 ---
st.markdown("""
    <h1 style='text-align: center;'>🔬 Little Science AI</h1>
    <p style='text-align: center;'>과학 소논문 주제를 AI로 탐색하고 설계하는 도우미입니다.</p>
    <hr>
""", unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    st.markdown("### 🧠 탐구 주제 입력")
    keyword = st.text_input("관심 있는 과학 키워드를 입력하세요 (예: 꿀벌, 효소 반응 등)")
    if keyword:
        st.session_state.keyword = keyword
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.markdown("### 🧪 주제 분석 결과")
    with st.spinner("GPT가 주제를 분석 중입니다..."):
        overview = get_overview_from_gpt(st.session_state.keyword)
        st.session_state.gpt_analysis = overview
        df["similarity"] = df["Project Title"].apply(lambda x: similarity(st.session_state.keyword, x))
        st.session_state.similar = df.sort_values("similarity", ascending=False).head(5)
    st.markdown(f"""<div style='background-color:#f9f9f9;padding:1em;border-radius:8px;'>{overview}</div>""", unsafe_allow_html=True)

    st.markdown("### 📁 유사한 과학 주제")
    for _, row in st.session_state.similar.iterrows():
        st.markdown(f"- {row['Project Title']} ({row['Year']})")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 더 깊이 분석하기"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("🔁 처음으로"):
            st.session_state.step = 1
            st.rerun()

elif st.session_state.step == 3:
    st.markdown("### 📄 주제 심화 분석")
    st.markdown("""
    GPT 기반 분석을 바탕으로 작성된 예시입니다. 실제 보고서로 사용 시 전문가의 검토가 필요합니다.
    """)
    st.markdown(st.session_state.gpt_analysis)

    st.markdown("---")
    if st.button("📄 PDF 저장"):
        file_path = create_pdf(st.session_state.gpt_analysis)
        with open(file_path, "rb") as f:
            st.download_button("📥 PDF 다운로드", f, file_name="소논문_설계_가이드.pdf")

    if st.button("🔁 처음으로 돌아가기"):
        st.session_state.step = 1
        st.rerun()

