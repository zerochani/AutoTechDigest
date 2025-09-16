import feedparser
from datetime import datetime, timezone, timedelta

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

    # 한국 시간(KST, UTC+9)을 정의합니다.
    KST = timezone(timedelta(hours=9))

    published_time = latest_article.get("published_parsed")
    if published_time:
        # 피드에서 제공된 시간을 UTC로 간주하고 KST로 변환합니다.
        utc_time = datetime(*published_time[:6], tzinfo=timezone.utc)
        kst_time = utc_time.astimezone(KST)
        published_date = kst_time.strftime("%Y-%m-%d")
    else:
        # 현재 시간을 UTC로 가져와 KST로 변환합니다.
        kst_time = datetime.now(timezone.utc).astimezone(KST)
        published_date = kst_time.strftime("%Y-%m-%d")

    print("✅ 최신 글 정보 가져오기 성공!")
    return title, link, content_summary, published_date
