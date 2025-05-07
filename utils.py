from fpdf import FPDF
import tempfile
from difflib import SequenceMatcher

# ✅ 문자열 유사도 계산 함수
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# ✅ 한글 지원 PDF 생성 함수
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()

    # ✅ 한글 폰트 등록
    pdf.add_font("Nanum", '', "NanumGothic-Regular.ttf", uni=True)
    pdf.set_font("Nanum", '', 12)

    # ✅ 텍스트 줄 단위로 PDF에 기록
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, txt=line)

    # ✅ 임시파일로 PDF 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name)
        return tmpfile.name

