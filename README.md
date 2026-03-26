# 🎬 YouTube Shorts Auto Maker (RPA Version)

이 프로젝트는 추가 API 비용 없이 **기존 구독 계정(Gemini Advanced, Grok)**의 웹 세션을 활용하여 유튜브 쇼츠 영상을 자동으로 제작하는 툴입니다. 

RPA(Robotic Process Automation) 기술로 LLM 웹 인터페이스를 제어하고, 생성된 데이터를 음성 합성 및 비디오 편집 엔진과 연결하는 엔드 투 엔드(End-to-End) 자동화 파이프라인을 구축합니다.

---

## 🏗 프로젝트 파이프라인

1.  **Script (Gemini):** AI가 스스로 주제를 선정하고 쇼펜하우어/니체 톤의 고퀄리티 JSON 대본 생성.
2.  **Audio (Edge-TTS):** 생성된 대본을 바탕으로 Microsoft Edge의 AI 성우를 통해 나레이션(.mp3) 자동 합성.
3.  **Visual (Grok):** 대본의 영어 묘사(Visual Prompt)를 바탕으로 Grok에서 영상/이미지 소스 생성. (**진행 중**)
4.  **Edit (MoviePy):** 모든 자산을 결합하여 자막이 포함된 최종 쇼츠 영상(.mp4) 렌더링. (**예정**)

---

## 🛠 초기 세팅 (Setup)

### 1. 패키지 설치
시스템 환경 보호를 위해 반드시 가상환경(venv)을 활성화한 후 진행하세요.

```bash
# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 필수 패키지 설치
pip install playwright edge-tts moviepy python-dotenv
playwright install chromium
2. 환경 변수 설정 (.env)
프로젝트 루트에 .env 파일을 생성하고 본인의 크롬 경로를 입력합니다.

코드 스니펫
CHROME_USER_DATA=/Users/yourname/Library/Application Support/Google/Chrome
CHROME_PROFILE=Default
🚀 실행 방법 (Usage)
프로젝트의 모든 과정(대본 생성 + 음성 합성)은 main.py 하나로 통합 실행됩니다.

⚠️ 실행 전 주의사항
크롬 브라우저 종료: 실행 전 반드시 모든 크롬 창을 닫아주세요. (데이터 폴더 점유 에러 방지)

로그인 확인: 크롬 프로필에 Gemini와 X(Grok) 로그인이 되어 있어야 세션 공유가 가능합니다.

🏃 파이프라인 가동
가상환경이 활성화된 상태에서 터미널에 아래 명령어를 입력하세요.

Bash
❯ python main.py
수행 결과:

Playwright가 제미나이 웹에 접속하여 주제 선정 및 대본을 작성합니다.

작성된 데이터는 latest_script.json 파일로 로컬에 저장됩니다.

곧바로 edge-tts가 가동되어 assets/audio/ 폴더에 장면별 나레이션 파일이 생성됩니다.

📂 프로젝트 구조
Plaintext
.
├── main.py              # 통합 실행 파일 (Pipeline)
├── core/
│   ├── scraper.py       # Gemini 대본 추출 모듈 (Async)
│   ├── audio_gen.py     # Edge-TTS 음성 생성 모듈
│   └── prompts.py       # 페르소나 및 프롬프트 관리
├── assets/
│   └── audio/           # 생성된 나레이션 (.mp3) 저장소
├── .env                 # 환경 변수 (Git 제외)
├── .gitignore           # 추적 제외 설정
└── latest_script.json   # 최근 생성된 대본 데이터
📝 로드맵 (Roadmap)
[x] Gemini 기반 동적 주제 선정 및 JSON 대본 추출 자동화

[x] Edge-TTS 연동 및 장면별 음성 자동 합성 파이프라인 구축

[ ] Next Step: Grok 웹 인터페이스 자동 제어 및 이미지/영상 다운로드 로직 구현

[ ] MoviePy 기반 타임라인 정렬 및 자막 렌더링 엔진 완성