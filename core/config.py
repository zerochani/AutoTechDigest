from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    애플리케이션 설정을 관리하는 클래스.
    .env 파일에서 환경 변수를 로드합니다.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # API Keys
    GEMINI_API_KEY: str
    NOTION_API_KEY: str
    KAKAO_REST_API_KEY: str
    KAKAO_REFRESH_TOKEN: str
    KAKAO_ACCESS_TOKEN: str | None = None

    # Notion
    NOTION_DATABASE_ID: str

    # RSS
    RSS_URL: str = "https://techcrunch.com/feed/"
    SOURCE_NAME: str = "TechCrunch"


settings = Settings()
