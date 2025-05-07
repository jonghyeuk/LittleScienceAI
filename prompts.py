# prompts.py

def topic_analysis_prompt(keyword):
    return f"""
    사용자가 제시한 키워드: {keyword}

    1. 이 키워드가 포함된 연구 주제 중 의미 있는 방향 3가지 제안
    2. 이 중 하나를 선택해 다음 항목에 맞춰 상세히 설명:
        - 🧠 Overview: 연구 소개 및 중요성
        - 🔬 Mechanism: 과학적 원리 설명
        - 🧩 Key Factors: 핵심 변수 또는 개입 요소
        - 📊 Evidence Synthesis: 논문 간 분석 및 비교
        - 🧠 Interpretation: 함의 및 확장 가능성
        - 🧾 Conclusion: 요약 결론 (2~4문장)
        - 🔗 References: 논문 제목 + 저자 + 연도 (2편 이상)

    설명은 명확한 과학 용어 정의와 예시 포함, 한자 대신 순수 한글만 사용.
    """

def niche_topic_prompt(keyword):
    return f"""
    사용자가 관심 있는 주제: {keyword}
    해당 주제와 관련해 잘 알려지지 않았지만 연구 가치가 높은 틈새 과학 주제 3가지를 제안하고,
    각 주제에 대해 연구 목적, 기대 효과, 확장성 관점에서 설명하라.
    """
