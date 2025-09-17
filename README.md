# AI 기술 뉴스 요약 및 Notion 자동화 비서 🤖

**매일 쏟아지는 해외 IT 기술 아티클, 이제 AI가 핵심만 요약하고 Notion에 자동으로 정리해 드립니다.**


---

## 🧐 프로젝트 소개 (Motivation)

개발자를 꿈꾸는 학생으로서 최신 기술 동향을 따라가는 것은 매우 중요합니다. 하지만 매일 수많은 해외 기술 블로그와 뉴스를 확인하고, 할 것도 많아서 많은 글들을 꾸준히 읽는 것이 쉽지 않습니다. 그래서 '매일 최신기사 요약본을 내 노션에 저장해주면 어떨까'하는 생각으로 이 프로젝트를 진행하게되었습니다.

이러한 **비효율적인 정보 소비 과정**을 자동화하여, 저는 더 중요한 학습과 개발에 집중하고 싶었습니다. 이 프로젝트는 **RSS 피드, Gemini AI, Notion API**를 결합하여 정보 수집부터 요약, 정리까지의 전 과정을 자동화하는 개인 맞춤형 학습 비서를 목표로 합니다.

## ✨ 주요 기능 (Features)

* **📰 최신 아티클 자동 수집**: 지정된 기술 블로그(예: TechCrunch)의 RSS 피드를 통해 새로운 글을 자동으로 가져옵니다.
* **🧠 AI 기반 한국어 요약**: Google의 **Gemini AI (1.5 Flash)**를 사용하여 영어로 된 긴 글의 핵심 내용을 자연스러운 한국어로 요약합니다.
* **🗂️ Notion 데이터베이스 자동 저장**: AI가 요약한 결과물을 글의 제목, 원문 링크, 출처, 게시일과 함께 지정된 Notion 데이터베이스에 자동으로 저장합니다.
* **💬 카카오톡 알림**: 요약 및 저장이 완료되면 지정된 카카오톡 채널로 알림 메시지를 발송합니다.
* **⏰ 매일 자동 실행**: **GitHub Actions**를 통해 매일 정해진 시간(한국 시간 오전 9시)에 전체 프로세스가 사람의 개입 없이 자동으로 실행됩니다.

## 🛠️ 사용한 기술 (Tech Stack)

* **Language**: `Python 3.13`
* **AI Model**: `Google Gemini 1.5 Flash API`
* **Automation**: `GitHub Actions`
* **Database**: `Notion API`
* **Libraries**:
    * `google-generativeai`
    * `notion-client`
    * `feedparser`
    * `python-dotenv`

## 🚀 설치 및 실행 방법 (Setup)

1.  **프로젝트 복제**
    ```bash
    git clone [https://github.com/](https://github.com/)[Your-GitHub-ID]/[Repository-Name].git
    cd [Repository-Name]
    ```

2.  **가상 환경 생성 및 활성화**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **필수 라이브러리 설치**
    ```bash
    pip install -r requirements.txt
    ```

4.  **.env 파일 설정**
    프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 아래 내용을 채워주세요.
    ```
    GEMINI_API_KEY="AIza..."
    NOTION_API_KEY="secret_..."
    NOTION_DATABASE_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    KAKAO_REST_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    KAKAO_REFRESH_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```

5.  **스크립트 수동 실행**
    ```bash
    python3 main.py
    ```

##  Notion Database URL
https://www.notion.so/2631f8b7773e8047b871c621b19bb2a1?v=2631f8b7773e80dbb94c000c85533afc