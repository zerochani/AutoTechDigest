from dataclasses import dataclass


@dataclass
class Article:
    """기사 정보를 담는 데이터 클래스"""

    title: str
    link: str
    content: str
    published_date: str
    summary: str = ""
    source: str = ""
    notion_page_url: str = ""
