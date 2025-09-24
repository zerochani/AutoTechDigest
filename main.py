from core.config import settings
from core.workflow import run_workflow


def main():
    """AI 비서의 메인 실행 함수"""
    run_workflow(settings)


if __name__ == "__main__":
    main()
