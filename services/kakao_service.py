import os
import requests
import json
from models.article import Article


def update_kakao_token(rest_api_key: str, refresh_token: str) -> str | None:
    """리프레시 토큰을 사용하여 새로운 액세스 토큰을 발급받습니다."""
    print("카카오 액세스 토큰을 갱신합니다...")
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": rest_api_key,
        "refresh_token": refresh_token,
    }
    response = requests.post(url, data=data)

    if response.status_code == 200:
        token_data = response.json()
        new_access_token = token_data.get("access_token")
        print("✅ 새로운 액세스 토큰 발급 성공!")
        return new_access_token
    else:
        print(f"카카오 토큰 갱신 실패: {response.text}")
        return None


def send_kakao_message(article: Article, rest_api_key: str, refresh_token: str):
    """'나에게 보내기' API를 사용하여 카카오톡 메시지를 전송합니다."""
    print("카카오톡 메시지 전송을 시작합니다...")

    access_token = update_kakao_token(rest_api_key, refresh_token)
    if not access_token:
        print("오류: 카카오 액세스 토큰을 얻을 수 없어 메시지를 전송할 수 없습니다.")
        return

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": f"Bearer {access_token}"}

    template_object = {
        "object_type": "feed",
        "content": {
            "title": f"📰 {article.title}",
            "description": article.summary,
            "image_url": "https://t1.kakaocdn.net/kakaocorp/kakaocorp/admin/6562f7bc017800001.png?type=thumb&opt=C72x72",
            "link": {
                "web_url": article.notion_page_url,
                "mobile_web_url": article.notion_page_url,
            },
        },
        "buttons": [
            {
                "title": "Notion 페이지 열기",
                "link": {
                    "web_url": article.notion_page_url,
                    "mobile_web_url": article.notion_page_url,
                },
            }
        ],
    }

    data = {"template_object": json.dumps(template_object)}

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("✅ 카카오톡 메시지 전송 성공!")
    else:
        print(f"카카오톡 메시지 전송 실패: {response.text}")
