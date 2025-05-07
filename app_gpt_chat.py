import streamlit as st
import pandas as pd
from openai import OpenAI
from prompts import generate_overview_prompt
from styles import set_custom_page_style
from utils import create_pdf, similarity

# --- 페이지 설정 및 스타일 ---
st.set_page_config(page_title="AI 기반 소논문 설계 가이드", layout="centered")
set_custom_page_style()

# --- API 키 및 클라이언트 ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- 데이터 로딩 ---
@st.cache_data
def load_db():
    df = pd.read_excel("ISEF Final DB.xlsx")
    return df

df = load_db()

# --- GPT 분석 함수 ---
def query_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- 유사 주제 추출 ---
def find_similar_topics(input_keyword, db, top_n=3):
    db["similarity"] = db["Project Title"].apply(lambda x: similarity(input_keyword, x))
    return db.sort_values(by="similarity", ascending=False).head(top_n)

# --- 앱 흐름 ---
st.title("🧪 주제 분석 결과")

if "step" not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    keyword = st.text_input("🔍 탐구하고 싶은 주제를 입력하세요 (예: 미세플라스틱, 꿀벌 개체 수 감소 등)")
    if keyword:
        st.session_state.keyword = keyword
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.markdown("### 🧠 주제 개요 및 추천")
    with st.spinner("GPT가 과학적 의미를 분석 중입니다..."):
        prompt = generate_overview_prompt(st.session_state.keyword)
        gpt_analysis = query_gpt(prompt)
        st.session_state.gpt_analysis = gpt_analysis
        similar = find_similar_topics(st.session_state.keyword, df)
        st.session_state.similar = similar
    st.markdown(gpt_analysis)
    st.markdown("---")
    st.markdown("### 📂 유사한 고등학생 논문 주제")
    if similar["similarity"].max() < 0.3:
        st.info("유사한 논문이 DB에 없습니다. 새로운 연구 주제를 탐색해보세요!")
    else:
        for _, row in similar.iterrows():
            st.markdown(f"- 📌 {row['Project Title']} ({row['Year']})")
    if st.button("👉 GPT 분석 기반 심층 보고서 보기"):
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.markdown("### 🧪 GPT 기반 분석 보고서")
    st.markdown(st.session_state.gpt_analysis)
    st.markdown("---")
    st.markdown("이 문서는 GPT 분석 결과이며 참고용으로만 활용 가능합니다.")
    if st.button("📄 PDF 저장"):
        file_path = create_pdf(st.session_state.gpt_analysis)
        with open(file_path, "rb") as f:
            st.download_button("📥 PDF 다운로드", f, file_name="소논문_가이드.pdf")
    if st.button("🧠 틈새 주제 제안 받기"):
        st.session_state.step = 4
        st.rerun()

elif st.session_state.step == 4:
    st.markdown("### 🧬 틈새 주제 및 실험 설계 가이드")
    st.markdown("아래는 GPT가 제안한 창의적 주제와 간단한 설계 아이디어입니다.")
    # GPT 틈새 제안 추가 가능
    if st.button("🔁 다시 시작하기"):
        st.session_state.clear()
        st.rerun()

