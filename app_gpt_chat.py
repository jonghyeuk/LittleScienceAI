import streamlit as st
import pandas as pd
from difflib import SequenceMatcher
from openai import OpenAI
from utils import create_pdf
from styles import set_page_style
set_page_style()
# --- 페이지 설정 ---
st.set_page_config(page_title="Little Science AI", layout="wide")

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
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    db["similarity"] = db["Project Title"].apply(lambda x: similarity(input_keyword, x))
    return db.sort_values(by="similarity", ascending=False).head(top_n)

# --- GPT 분석 프롬프트 ---
def generate_topic_analysis(keyword):
    prompt = f"""
    사용자가 제시한 키워드: {keyword}

    1. 이 키워드가 포함된 연구 주제 중 의미 있는 방향 3가지 제안
    2. 이 중 하나를 선택해 다음 항목에 맞춰 상세히 설명:
        - 🧠 Overview: 연구 소개 및 중요성
        - 🔬 Mechanism: 생리적/과학적 원리 설명
        - 🧩 Key Factors: 핵심 변수 또는 개입 요소
        - 📊 Evidence Synthesis: 논문 간 분석 및 비교
        - 🧠 Interpretation: 함의 및 확장 가능성
        - 🧾 Conclusion: 요약 결론 (2~4문장)
        - 🔗 References: 논문 제목 + 저자 + 연도 (2편 이상)

    설명은 명확한 과학 용어 정의와 예시 포함, 한자 대신 순수 한글만 사용.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- 첫 화면 버튼 ---
def home_button():
    if st.button("🔁 처음으로 돌아가기"):
        st.session_state.step = 1
        st.rerun()

# --- UI 본문 컨테이너 ---
def render_document(content):
    st.markdown("""
        <div style='max-width: 900px; margin: auto; padding: 2rem; background-color: white; border-radius: 10px;'>
    """, unsafe_allow_html=True)
    st.markdown(content)
    st.markdown("""</div>""", unsafe_allow_html=True)

# --- Step 1: 주제 입력 ---
if st.session_state.step == 1:
    st.title("🔬 Little Science AI: 과학 기반 소논문 설계 가이드")
    st.markdown("💬 아래에 관심 키워드를 입력하세요 (예: 꿀벌, 온도, 기후 변화 등)")
    keyword = st.text_input("🧠 키워드 입력")
    if keyword:
        st.session_state.keyword = keyword
        st.session_state.step = 2
        st.rerun()

# --- Step 2: 분석 및 추천 ---
elif st.session_state.step == 2:
    st.subheader("📊 주제 분석 결과")
    with st.spinner("AI가 주제를 분석 중입니다..."):
        overview = generate_topic_analysis(st.session_state.keyword)
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
    prompt = f"""
    사용자가 관심 있는 주제: {st.session_state.keyword}
    해당 주제와 관련해 잘 알려지지 않았지만 연구 가치가 높은 틈새 주제 3가지를 제안하고,
    각 주제에 대해 연구 목적, 기대 효과, 확장성 관점에서 설명하라.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    st.session_state.niche = response.choices[0].message.content
    render_document(st.session_state.niche)

    if st.button("📄 PDF로 저장"):
        file_path = create_pdf(st.session_state.keyword + "_리포트", st.session_state.overview + "\n\n" + st.session_state.niche)
        with open(file_path, "rb") as f:
            st.download_button("📥 PDF 다운로드", f, file_name=file_path)
    home_button()
