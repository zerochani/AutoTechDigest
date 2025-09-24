from services import rss_service, gemini_service, notion_service, kakao_service
from core.config import Settings


def run_workflow(settings: Settings):
    """AI 비서의 메인 워크플로우를 실행합니다."""
    # 1. 최신 기술 블로그 글 가져오기
    latest_article = rss_service.get_latest_article_info(settings.RSS_URL)
    if not latest_article:
        print("새로운 글을 찾지 못했습니다. 프로그램을 종료합니다.")
        return

    # 2. Gemini AI를 사용하여 글 요약하기
    summary = gemini_service.summarize_with_gemini(
        latest_article.content, settings.GEMINI_API_KEY
    )
    if "실패" in summary:
        print("AI 요약에 실패했습니다. 프로그램을 종료합니다.")
        return
    latest_article.summary = summary
    print("\n--- AI 요약 결과 (한국어) ---")
    print(latest_article.summary)

    # 3. 요약된 내용을 Notion에 저장하기
    notion_page_url = notion_service.save_to_notion(
        article=latest_article,
        notion_api_key=settings.NOTION_API_KEY,
        notion_database_id=settings.NOTION_DATABASE_ID,
        source=settings.SOURCE_NAME,
    )
    if not notion_page_url:
        print("Notion 저장에 실패했습니다. 프로그램을 종료합니다.")
        return
    latest_article.notion_page_url = notion_page_url

    # 4. 카카오톡으로 Notion 링크 보내기
    kakao_service.send_kakao_message(
        article=latest_article,
        rest_api_key=settings.KAKAO_REST_API_KEY,
        refresh_token=settings.KAKAO_REFRESH_TOKEN,
    )
