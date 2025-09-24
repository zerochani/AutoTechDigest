from notion_client import Client
from models.article import Article


def save_to_notion(
    article: Article, notion_api_key: str, notion_database_id: str, source: str
) -> str | None:
    """요약된 글의 정보를 Notion 데이터베이스에 저장하고, 생성된 페이지의 URL을 반환합니다."""
    print("Notion에 저장을 시작합니다...")
    if not notion_api_key or not notion_database_id:
        print("오류: Notion API 키 또는 데이터베이스 ID를 찾을 수 없습니다.")
        return None

    try:
        notion = Client(auth=notion_api_key)

        properties = {
            "제목": {"title": [{"text": {"content": article.title}}]},
            "url": {"url": article.link},
            "텍스트": {"rich_text": [{"text": {"content": article.summary}}]},
            "출처": {"rich_text": [{"text": {"content": source}}]},
            "게시일": {"date": {"start": article.published_date}},
        }

        new_page = notion.pages.create(
            parent={"database_id": notion_database_id}, properties=properties
        )
        page_id = new_page.get("id")
        if page_id:
            page_id_no_hyphen = page_id.replace("-", "")
            page_url = f"https://www.notion.so/{page_id_no_hyphen}"
            print("✅ Notion 데이터베이스에 저장 성공!")
            return page_url
        else:
            print("오류: 생성된 Notion 페이지의 ID를 찾을 수 없습니다.")
            return None

    except Exception as e:
        print(f"Notion 저장 중 오류가 발생했습니다: {e}")
        return None
