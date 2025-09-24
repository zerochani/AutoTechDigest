import google.generativeai as genai


def summarize_with_gemini(content: str, api_key: str) -> str:
    """Gemini AI를 사용해 주어진 내용을 한국어로 요약합니다."""
    print("Gemini AI로 한국어 요약을 시작합니다...")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        당신은 해외 최신 IT 기술 기사를 한국 대학생들에게 설명해주는 친절한 전문가입니다.
        아래의 영어로 된 기사 본문을 읽고, 핵심 내용과 중요성을 한국어로 3~4문장으로 요약해주세요.
        부드럽고 친근한 말투를 사용해주세요.
        ---
        [영어 기사 본문]
        {content}
        ---
        """
        response = model.generate_content(prompt)
        print("✅ AI 한국어 요약 성공!")
        return response.text
    except Exception as e:
        print(f"Gemini AI 요약 중 오류가 발생했습니다: {e}")
        return "AI 요약에 실패했습니다."
