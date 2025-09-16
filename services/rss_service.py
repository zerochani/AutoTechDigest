import feedparser
from datetime import datetime

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

    published_time = latest_article.get("published_parsed")
    if published_time:
        published_date = datetime(*published_time[:6]).strftime("%Y-%m-%d")
    else:
        published_date = datetime.now().strftime("%Y-%m-%d")

    print("✅ 최신 글 정보 가져오기 성공!")
    return title, link, content_summary, published_date
