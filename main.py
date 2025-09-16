import config
from services.rss_service import get_latest_article_info
from services.gemini_service import summarize_with_gemini
from services.notion_service import save_to_notion
from services.kakao_service import send_kakao_message

def main():
    """AI 비서의 메인 실행 함수"""
    # 1. 최신 기술 블로그 글 가져오기
    article_title, article_link, article_content, article_date = get_latest_article_info(
        config.RSS_URL
    )

    if not article_title:
        print("새로운 글을 찾지 못했습니다. 프로그램을 종료합니다.")
        return

    # 2. Gemini AI를 사용하여 글 요약하기
    ai_summary = summarize_with_gemini(article_content)
    print("\n--- AI 요약 결과 (한국어) ---")
    print(ai_summary)

    if "실패" in ai_summary:
        print("AI 요약에 실패했습니다. 프로그램을 종료합니다.")
        return

    # 3. 요약된 내용을 Notion에 저장하기
    notion_page_url = save_to_notion(
        title=article_title,
        link=article_link,
        summary=ai_summary,
        source=config.SOURCE_NAME,
        published_date=article_date,
    )

    # 4. Notion 저장 실패 시 프로그램 종료
    if not notion_page_url:
        print("Notion 저장에 실패했습니다. 프로그램을 종료합니다.")
        return

    # 5. 카카오톡으로 Notion 링크 보내기
    send_kakao_message(title=article_title, summary=ai_summary, link=notion_page_url)


if __name__ == "__main__":
    main()
