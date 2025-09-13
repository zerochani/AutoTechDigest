import os
import feedparser
import google.generativeai as genai
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime  # 날짜 처리를 위해 datetime 추가
import requests
import json

# .env 파일에서 환경 변수를 불러옵니다.
load_dotenv()

# --- 함수 정의 부분 ---


def get_latest_article_info(rss_url):
    """RSS 피드에서 가장 최신 글의 정보(제목, 링크, 내용, 게시일)를 가져옵니다."""
    print(f"'{rss_url}'에서 최신 글을 가져오는 중...")
    try:
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            print("오류: 피드에서 글을 찾을 수 없습니다.")
            return None, None, None, None
    except Exception as e:
        print(f"RSS 피드를 파싱하는 중 오류가 발생했습니다: {e}")
        return None, None, None, None

    latest_article = feed.entries[0]
    title = latest_article.title
    link = latest_article.link
    content_summary = latest_article.get("summary", "내용 요약 없음")

    # [수정] 게시일 정보 가져오기 및 형식 변환
    published_time = latest_article.get("published_parsed")
    if published_time:
        # YYYY-MM-DD 형식의 문자열로 변환
        published_date = datetime(*published_time[:6]).strftime("%Y-%m-%d")
    else:
        # 게시일 정보가 없을 경우 오늘 날짜로 설정
        published_date = datetime.now().strftime("%Y-%m-%d")

    print("✅ 최신 글 정보 가져오기 성공!")
    return title, link, content_summary, published_date


def summarize_with_gemini(content):
    """Gemini AI를 사용해 주어진 내용을 한국어로 요약합니다."""
    # (이 함수는 이전과 동일합니다. 생략)
    print("Gemini AI로 한국어 요약을 시작합니다...")
    try:
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=GEMINI_API_KEY)
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


def update_kakao_token():
    """리프레시 토큰을 사용하여 새로운 액세스 토큰을 발급받고 환경 변수에 저장합니다."""
    print("카카오 액세스 토큰을 갱신합니다...")
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("KAKAO_REST_API_KEY"),
        "refresh_token": os.getenv("KAKAO_REFRESH_TOKEN"),
    }
    response = requests.post(url, data=data)

    if response.status_code == 200:
        token_data = response.json()
        new_access_token = token_data.get("access_token")

        # .env 파일에 직접 쓰기보다는, 현재 실행 세션의 환경 변수를 업데이트합니다.
        # (주의: 이 방식은 .env 파일을 직접 수정하지 않으므로, 영구 저장되지 않습니다.)
        os.environ["KAKAO_ACCESS_TOKEN"] = new_access_token
        print("✅ 새로운 액세스 토큰 발급 성공!")
        return new_access_token
    else:
        print(f"카카오 토큰 갱신 실패: {response.text}")
        return None


def send_kakao_message(title, summary, link):
    """'나에게 보내기' API를 사용하여 카카오톡 메시지를 전송합니다."""
    print("카카오톡 메시지 전송을 시작합니다...")
    access_token = os.getenv("KAKAO_ACCESS_TOKEN")

    # 액세스 토큰이 없거나 유효하지 않을 경우를 대비해 갱신 시도
    if not access_token:
        access_token = update_kakao_token()
        if not access_token:
            print(
                "오류: 카카오 액세스 토큰을 얻을 수 없어 메시지를 전송할 수 없습니다."
            )
            return

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": f"Bearer {access_token}"}

    # 카카오톡 메시지 템플릿 생성
    template_object = {
        "object_type": "feed",
        "content": {
            "title": f"📰 {title}",
            "description": summary,
            "image_url": "https://t1.kakaocdn.net/kakaocorp/kakaocorp/admin/6562f7bc017800001.png?type=thumb&opt=C72x72",  # 카카오 기본 로고
            "link": {"web_url": link, "mobile_web_url": link},
        },
        "buttons": [
            {
                "title": "기사 전문 보기",
                "link": {"web_url": link, "mobile_web_url": link},
            }
        ],
    }

    data = {"template_object": json.dumps(template_object)}

    response = requests.post(url, headers=headers, data=data)

    # 만약 토큰 만료(401) 오류가 발생하면, 토큰을 갱신하고 다시 시도
    if response.status_code == 401:
        print("액세스 토큰이 만료되었습니다. 갱신 후 다시 시도합니다.")
        new_access_token = update_kakao_token()
        if new_access_token:
            headers["Authorization"] = f"Bearer {new_access_token}"
            response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("✅ 카카오톡 메시지 전송 성공!")
    else:
        print(f"카카오톡 메시지 전송 실패: {response.text}")


def save_to_notion(title, link, summary, source, published_date):
    """요약된 글의 정보를 Notion 데이터베이스에 저장하고, 생성된 페이지의 URL을 반환합니다."""
    print("Notion에 저장을 시작합니다...")
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

    if not NOTION_API_KEY or not DATABASE_ID:
        print("오류: Notion API 키 또는 데이터베이스 ID를 찾을 수 없습니다.")
        return None  # 실패 시 None 반환

    try:
        notion = Client(auth=NOTION_API_KEY)

        properties = {
            "제목": {"title": [{"text": {"content": title}}]},
            "url": {"url": link},
            "텍스트": {"rich_text": [{"text": {"content": summary}}]},
            "출처": {"rich_text": [{"text": {"content": source}}]},
            "게시일": {"date": {"start": published_date}},
        }

        new_page = notion.pages.create(
            parent={"database_id": DATABASE_ID}, properties=properties
        )
        page_id = new_page.get("id")
        if page_id:
            # ID에서 하이픈 제거
            page_id_no_hyphen = page_id.replace("-", "")
            # Notion 페이지 URL 형식에 맞게 조합
            page_url = f"https://www.notion.so/{page_id_no_hyphen}"
            print("✅ Notion 데이터베이스에 저장 성공!")
            return page_url  # 성공 시 페이지 URL 반환
        else:
            print("오류: 생성된 Notion 페이지의 ID를 찾을 수 없습니다.")
            return None

    except Exception as e:
        print(f"Notion 저장 중 오류가 발생했습니다: {e}")
        return None  # 실패 시 None 반환


# --- 메인 실행 부분 ---
if __name__ == "__main__":
    RSS_URL = "https://techcrunch.com/feed/"
    SOURCE_NAME = "TechCrunch"

    # [수정] 게시일(article_date) 변수 추가
    article_title, article_link, article_content, article_date = (
        get_latest_article_info(RSS_URL)
    )

    if article_title:
        ai_summary = summarize_with_gemini(article_content)

        print("\n--- AI 요약 결과 (한국어) ---")
        print(ai_summary)

        if "실패" not in ai_summary:
            # Notion에 저장하고 생성된 페이지의 URL을 받음
            notion_page_url = save_to_notion(
                title=article_title,
                link=article_link,
                summary=ai_summary,
                source=SOURCE_NAME,
                published_date=article_date,
            )

            # Notion 저장이 성공하여 유효한 URL이 반환되었을 경우에만 카카오톡 메시지 전송
            if notion_page_url:
                send_kakao_message(
                    title=article_title, summary=ai_summary, link=notion_page_url
                )
