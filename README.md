🎬 YouTube Shorts Auto Maker (RPA Version)
이 프로젝트는 추가 API 비용 없이 **기존 구독 계정(Gemini Advanced, Grok)**의 웹 세션을 활용하여 유튜브 쇼츠 영상을 자동으로 제작하는 툴입니다.

🏗 프로젝트 구조 및 워크플로우
Script Generation: Playwright를 이용해 Gemini 웹에 접속, 페르소나 기반의 쇼츠 대본(JSON) 생성.

Asset Generation: 대본의 묘사를 바탕으로 Grok(x.com)에서 영상 및 이미지 소스 생성 및 다운로드.

Video Editing: MoviePy를 활용하여 영상, 자막, 배경음악을 합성하여 최종 .mp4 파일 렌더링.

🛠 기술 스택
Language: Python 3.12+

Automation: Playwright (Chromium)

Video Engine: MoviePy

Environment: python-dotenv, venv

🚀 시작하기 (Setup)
1. 가상환경 설정 및 패키지 설치
시스템 파이썬 환경을 보호하기 위해 반드시 가상환경 내에서 실행합니다.

Bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 필수 라이브러리 설치
pip install playwright moviepy python-dotenv
playwright install chromium
2. 환경 변수 설정 (.env)
본인의 크롬 프로필 경로를 설정하여 로그인 세션을 공유합니다. (보안을 위해 .env 파일은 Git 커밋에서 제외합니다.)

Plaintext
CHROME_USER_DATA=/Users/yourname/Library/Application Support/Google/Chrome
CHROME_PROFILE=Default
3. 현재 구현된 기능
[x] 프로젝트 구조 설계 및 .gitignore 설정

[x] Playwright 기반 Gemini 웹 세션 연동 기초 (scraper.py)

[ ] Gemini 응답 JSON 파싱 및 정제 (진행 중)

[ ] Grok 영상 생성 자동화 (예정)

📌 주의사항
Login Session: 실행 전 실제 크롬 브라우저에서 Gemini와 x.com에 로그인이 되어 있어야 합니다.

Headless Mode: 초기 개발 시에는 동작 확인을 위해 headless=False 옵션을 사용합니다.

Rate Limit: 계정 보호를 위해 요청 간에 적절한 time.sleep 또는 wait_for_timeout을 권장합니다.