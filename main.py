import os
import feedparser
import google.generativeai as genai
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime # 날짜 처리를 위해 datetime 추가

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
        model = genai.GenerativeModel('gemini-1.5-flash')
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

def save_to_notion(title, link, summary, source, published_date):
    """요약된 글의 정보를 Notion 데이터베이스에 저장합니다."""
    print("Notion에 저장을 시작합니다...")
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

    if not NOTION_API_KEY or not DATABASE_ID:
        print("오류: Notion API 키 또는 데이터베이스 ID를 찾을 수 없습니다.")
        return

    try:
        notion = Client(auth=NOTION_API_KEY)
        
        # [수정] Notion 데이터베이스 속성 이름과 유형에 정확히 맞춤
        properties = {
            "제목": {"title": [{"text": {"content": title}}]},
            "url": {"url": link},
            "텍스트": {"rich_text": [{"text": {"content": summary}}]},
            "출처": {"rich_text": [{"text": {"content": source}}]},
            "게시일": {"date": {"start": published_date}} # 날짜 속성 추가
        }
        
        notion.pages.create(parent={"database_id": DATABASE_ID}, properties=properties)
        print("✅ Notion 데이터베이스에 저장 성공!")
        
    except Exception as e:
        print(f"Notion 저장 중 오류가 발생했습니다: {e}")

# --- 메인 실행 부분 ---
if __name__ == "__main__":
    RSS_URL = "https://techcrunch.com/feed/"
    SOURCE_NAME = "TechCrunch"
    
    # [수정] 게시일(article_date) 변수 추가
    article_title, article_link, article_content, article_date = get_latest_article_info(RSS_URL)
    
    if article_title:
        ai_summary = summarize_with_gemini(article_content)
        
        print("\n--- AI 요약 결과 (한국어) ---")
        print(ai_summary)
        
        if "실패" not in ai_summary:
            # [수정] 게시일(article_date)을 함께 전달
            save_to_notion(
                title=article_title, 
                link=article_link, 
                summary=ai_summary, 
                source=SOURCE_NAME, 
                published_date=article_date
            )

