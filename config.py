import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 불러옵니다.
load_dotenv()

# --- API 키 ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
KAKAO_REFRESH_TOKEN = os.getenv("KAKAO_REFRESH_TOKEN")
KAKAO_ACCESS_TOKEN = os.getenv("KAKAO_ACCESS_TOKEN")

# --- Notion ---
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# --- RSS ---
RSS_URL = "https://techcrunch.com/feed/"
SOURCE_NAME = "TechCrunch"
