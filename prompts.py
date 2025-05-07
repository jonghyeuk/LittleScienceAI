# prompts.py

def generate_overview_prompt(keyword: str) -> str:
    return f"""
🧪 [소논문 주제 분석 요청]

- 입력 키워드: {keyword}

아래 항목을 구성해줘:
1. 🧠 Overview – 주제 소개 및 중요성
2. 🔬 Mechanism – 주요 과학적 원리 (가능한 경우)
3. 🧩 Key Factors – 주요 변수 또는 실험 요소
4. 📊 Evidence – 논문 또는 데이터 기반 정리
5. 🧠 Interpretation – 과학적 해석과 활용 가능성
6. 🔗 References – 논문 제목, 저자, 연도 형태로 2~3개

⚠️ 대상은 고등학생이지만, 너무 단순화하지 마. 과학적 용어는 정의해서 사용해줘.
    """

