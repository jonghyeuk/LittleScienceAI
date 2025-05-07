import streamlit as st
from fpdf import FPDF
import tempfile

# ✅ PDF 저장 함수
def create_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Nanum", "", "NanumGothic-Regular.ttf", uni=True)
    pdf.set_font("Nanum", size=12)

    for line in content.split("\n"):
        pdf.multi_cell(0, 8, txt=line)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name)

    with open(tmpfile.name, "rb") as f:
        st.download_button(
            label="📄 PDF 다운로드",
            data=f,
            file_name=f"{title}_설계가이드.pdf",
            mime="application/pdf"
        )

# ✅ 상태 초기화 함수
def reset_state():
    for key in st.session_state.keys():
        del st.session_state[key]
