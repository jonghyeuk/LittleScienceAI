# app_gpt_chat.py (4단계 틈새주제 + PDF 저장 추가 완료)
import streamlit as st
from openai import OpenAI
import pandas as pd
import time
import requests
from difflib import SequenceMatcher
from fpdf import FPDF

# --- 페이지 설정 ---
st.set_page_config(page_title="Little Science AI", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- 시스템 역할 설정 ---
SYSTEM_PROMPT = """
너는 little science AI라는 이름의 과학전문 AI야. 네 역할은 복잡한 과학적 주제를 명확하고 증거 기반으로 설명해주는 것이며, 대상 독자는 일반 대중부터 연구자까지 다양해.

다음 원칙을 철저히 따를 것:
1. 객관성
2. 깊이
3. 명확성
4. 인용 기준 (논문 제목, 저자, 연도)
5. 구조화된 응답 (Overview, Mechanism, Key Factors, Evidence, Interpretation, Conclusion, References)
"""

# --- 데이터 불러오기 (자체 DB)
@st.cache_data
def load_db():
    return pd.read_excel("ISEF Final DB.xlsx")

df = load_db()

# --- 유사도 기반 논문 추천 ---
def search_similar_titles(input_text, db):
    def similarity(a, b):
        return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()
    db["similarity"] = db["Project Title"].apply(lambda x: similarity(input_text, x))
    return db.sort_values("similarity", ascending=False).head(3)

# --- 감마 스타일 텍스트 출력 ---
def typewriter(text, delay=0.01):
    output = st.empty()
    full = ""
    for char in text:
        full += char
        output.markdown(full)
        time.sleep(delay)

# --- arXiv 논문 검색 ---
def search_arxiv(query, max_results=3):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return []
    entries = resp.text.split("<entry>")[1:]
    results = []
    for entry in entries:
        title = entry.split("<title>")[1].split("</title>")[0].strip().replace('\n', ' ')
        summary = entry.split("<summary>")[1].split("</summary>")[0].strip().replace('\n', ' ')
        link = entry.split("<id>")[1].split("</id>")[0].strip()
        results.append({"title": title, "summary": summary, "link": link})
    return results

# --- GPT 요약 ---
def summarize_abstract(text):
    prompt = f"다음 논문 초록을 요약하고 핵심 내용을 구조화해줘:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# --- 고등학생 논문 추론 분석 ---
def analyze_student_paper(title):
    prompt = f"""
    아래는 고등학생이 작성한 과학 소논문의 제목입니다. 이 제목을 바탕으로 연구 주제의 배경, 실험 목적, 가능했던 방법, 결론 등을 추론해 과학적으로 분석해주세요.

    제목: {title}

    형식:
    - 🧠 연구 배경
    - 🔬 실험 목적
    - 🧪 실험 설계 예상
    - 📊 변수 및 결과 예측
    - 📘 과학적 의미와 한계
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# --- 틈새 주제 제안 ---
def suggest_gap_topics(base_topic):
    prompt = f"다음 주제를 기반으로 아직 탐구되지 않은 틈새 과학 주제를 2~3개 추천하고, 그 과학적 의미와 가능성을 설명해줘:\n\n{base_topic}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# --- PDF 저장 ---
def save_as_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Nanum", '', fname="NanumGothic-Regular.ttf", uni=True)
    pdf.set_font("Nanum", size=12)
    for line in content.split("\n"):
        pdf.multi_cell(0, 8, txt=line)
    pdf_file = f"{title}.pdf"
    pdf.output(pdf_file)
    return pdf_file

# --- 대화 시작 ---
st.title("🧬 Little Science AI")
st.markdown("과학 주제를 대화로 탐색하고, 실험 아이디어 및 최신 논문까지 연결합니다.")

if "chat" not in st.session_state:
    st.session_state.chat = []
if "report" not in st.session_state:
    st.session_state.report = ""

# --- 대화 흐름 ---
for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(msg)

user_input = st.chat_input("궁금한 과학 주제를 알려주세요!")
if user_input:
    st.session_state.chat.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    report_text = f"## 사용자 입력 주제\n{user_input}\n\n"

    with st.chat_message("assistant"):
        with st.spinner("분석 중입니다..."):
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            ai_reply = response.choices[0].message.content
            typewriter(ai_reply)
            st.session_state.chat.append(("assistant", ai_reply))
            report_text += f"\n## GPT 분석\n{ai_reply}\n\n"

        st.markdown("\n---\n### 📁 유사 소논문 분석")
        similar = search_similar_titles(user_input, df)
        if not similar.empty:
            for i, row in similar.iterrows():
                st.markdown(f"- **{row['Project Title']}** ({row['Year']})")
                if st.button(f"📘 이 논문 추론 분석하기", key=row['Project Title']):
                    student_summary = analyze_student_paper(row['Project Title'])
                    st.markdown(student_summary)
                    report_text += f"\n### 유사 논문 분석 - {row['Project Title']}\n{student_summary}\n\n"

        st.markdown("\n---\n### 🔎 arXiv 최신 논문")
        papers = search_arxiv(user_input)
        for paper in papers:
            st.markdown(f"**{paper['title']}**\n\n[{paper['link']}]({paper['link']})")
            if st.button(f"📄 이 논문 요약하기", key=paper['title']):
                summary = summarize_abstract(paper['summary'])
                st.markdown(summary)
                report_text += f"\n### arXiv 논문 요약 - {paper['title']}\n{summary}\n\n"

        st.markdown("\n---\n### 🌱 틈새 주제 제안")
        gap = suggest_gap_topics(user_input)
        st.markdown(gap)
        report_text += f"\n## 틈새 주제 제안\n{gap}\n\n"

        st.session_state.report = report_text

        st.markdown("\n💬 추가로 궁금한 것이 있다면 이어서 질문해주세요!")

# --- PDF 다운로드 ---
if st.session_state.report:
    if st.button("📥 최종 보고서 PDF로 저장"):
        filepath = save_as_pdf("Little_Science_Report", st.session_state.report)
        with open(filepath, "rb") as f:
            st.download_button("📄 PDF 다운로드", f, file_name=filepath)
