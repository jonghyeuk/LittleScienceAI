# utils.py

import streamlit as st
from fpdf import FPDF
import tempfile
from difflib import SequenceMatcher

# 한글 PDF 생성 함수
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Nanum", '', fname="NanumGothic-Regular.ttf", uni=True)
    pdf.set_font("Nanum", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, txt=line)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name)
        return tmpfile.name

# 유사도 계산 함수
def similarity(a, b):
    if not isinstance(a, str) or not isinstance(b, str):
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()
