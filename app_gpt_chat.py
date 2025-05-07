# app_gpt_chat.py (prompts.py 분리 반영)
import streamlit as st
import pandas as pd
from styles import set_custom_styles
from difflib import SequenceMatcher
from openai import OpenAI
from utils import create_pdf
from prompts import topic_analysis_prompt, niche_topic_prompt
from styles import set_page_style

# --- 페이지 설정 ---
st.set_page_config(page_title="AI 기반 소논문 설계 가이드", layout="wide")
set_custom_styles()  # 화면 정렬 및 스타일 적용

# --- 세션 초기화 ---
if "step" not in st.session_state:
    st.session_state.step = 1

# --- OpenAI 클라이언트 ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- 데이터 불러오기 ---
@st.cache_data
def load_db():
    return pd.read_excel("ISEF Final DB.xlsx")

df = load_db()

# --- 유사도 분석 함수 ---
def find_similar_topics(input_keyword, db, top_n=3):
def similarity(a, b):
    if not isinstance(a, str) or not isinstance(b, str):
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    db["similarity"] = db["Project Title"].apply(lambda x: similarity(input_keyword, x))
    return db.sort_values(by="similarity", ascending=False).head(top_n)

# --- GPT 호출 ---
def query_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- 홈 버튼 ---
def home_button():
    if st.button("🔁 처음으로 돌아가기"):
        st.session_state.step = 1
        st.rerun()

# --- 화면 가운데 문서 스타일 출력 ---
def render_document(content):
    st.markdown("""
        <div style='max-width: 900px; margin: auto; padding: 2rem; background-color: white; border-radius: 10px;'>
    """, unsafe_allow_html=True)
    st.markdown(content)
    st.markdown("""</div>""", unsafe_allow_html=True)

# --- Step 1: 키워드 입력 ---
if st.session_state.step == 1:
    st.title("🔬 Little Science AI: 과학 기반 소논문 설계 가이드")
    st.markdown("💬 아래에 관심 키워드를 입력하세요 (예: 꿀벌, 온도, 기후 변화 등)")
    keyword = st.text_input("🧠 키워드 입력")
    if keyword:
        st.session_state.keyword = keyword
        st.session_state.step = 2
        st.rerun()

# --- Step 2: 주제 분석 및 유사 논문 ---
elif st.session_state.step == 2:
    st.subheader("📊 주제 분석 결과")
    with st.spinner("AI가 주제를 분석 중입니다..."):
        overview = query_gpt(topic_analysis_prompt(st.session_state.keyword))
        st.session_state.overview = overview
        similar = find_similar_topics(st.session_state.keyword, df)
        st.session_state.similar = similar

    render_document(overview)

    st.subheader("📁 유사한 고등학생 실제 논문 (ISEF DB)")
    if similar["similarity"].iloc[0] < 0.4:
        st.warning("📌 유사 논문이 없습니다. 새로운 주제로 시도해 보세요!")
    else:
        for _, row in similar.iterrows():
            st.markdown(f"- {row['Project Title']} ({row['Year']}년)")

    if st.button("🧠 추천 틈새 주제 보기"):
        st.session_state.step = 3
        st.rerun()
    home_button()

# --- Step 3: 틈새 주제 추천 ---
elif st.session_state.step == 3:
    st.subheader("🧩 틈새 주제 제안 + 연구 확장")
    response = query_gpt(niche_topic_prompt(st.session_state.keyword))
    st.session_state.niche = response
    render_document(response)

    if st.button("📄 PDF로 저장"):
        file_path = create_pdf(st.session_state.keyword + "_리포트", st.session_state.overview + "\n\n" + response)
        with open(file_path, "rb") as f:
            st.download_button("📥 PDF 다운로드", f, file_name=file_path)
    home_button()
