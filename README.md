# 🎬 YouTube Shorts Auto Maker (Hybrid RPA Version)

이 프로젝트는 **기존 유료 구독 계정(Gemini Advanced)**의 강력한 추론 능력과 **경량 API(Pollinations, Edge-TTS)**의 기동성을 결합한 하이브리드형 유튜브 쇼츠 자동 제작 툴입니다. 

WSL2 환경에서의 브라우저 제어 이슈를 극복하고, **대본(RPA) → 음성(TTS) → 이미지(API) → 편집(MoviePy)**으로 이어지는 안정적인 엔드 투 엔드(End-to-End) 파이프라인을 구축합니다.

---

## 🏗 프로젝트 파이프라인 (The Pipeline)

1.  **Script (Gemini RPA):** Playwright를 통해 사용자의 **Gemini Advanced** 계정에 접속, 쇼펜하우어/니체 톤의 고퀄리티 JSON 대본을 생성합니다. (유료 계정의 지능 활용)
2.  **Audio (Edge-TTS):** 생성된 대본을 바탕으로 Microsoft Edge의 AI 성우를 통해 고음질 나레이션(.mp3)을 장면별로 생성합니다.
3.  **Visual (Pollinations API):** 대본의 `visual_prompt`를 활용하여 **무료/무제한 API** 방식으로 9:16 세로형 이미지를 생성합니다. (Grok RPA를 대체하여 안정성 확보)
4.  **Edit (MoviePy):** 모든 자산을 결합하여 자막이 포함된 최종 영상(.mp4)을 렌더링합니다. (**개발 예정**)

---

## 🛠 초기 세팅 (Setup)

### 1. 패키지 설치
WSL 환경의 가상환경(venv)에서 아래 명령어를 실행하세요.

```bash
# 가상환경 활성화
source venv/bin/activate

# 필수 패키지 설치
pip install playwright edge-tts moviepy python-dotenv requests playwright-stealth
playwright install chromium
2. WSL2 환경 최적화 (필수)
Ubuntu 24.04 이상의 환경에서 브라우저 실행 에러(SIGTRAP)를 방지하기 위해 아래 설정을 반드시 수행해야 합니다.

Bash
# 샌드박스 보안 제한 해제 (유료 계정 로그인 창 활성화용)
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0

# 디스플레이 변수 설정 (창을 띄워야 할 경우 필수)
export DISPLAY=:0
🚀 실행 방법 (Usage)
1. 환경 변수 설정 (.env)
프로젝트 루트에 .env 파일을 생성하고 본인의 크롬 경로를 입력합니다.

코드 스니펫
CHROME_USER_DATA=/home/joo/code/shorts-auto-maker/user_data
CHROME_PROFILE=Default
2. 파이프라인 가동
Bash
❯ python main.py
Step 1: Playwright가 제미나이에 접속해 대본을 생성합니다. (최초 실행 시 로그인 1회 필요)

Step 2: assets/audio/ 폴더에 장면별 음성이 저장됩니다.

Step 3: Pollinations API가 assets/images/ 폴더에 9:16 이미지를 생성합니다. (429 에러 방지를 위한 Throttling 적용 완료)

📂 프로젝트 구조
Plaintext
.
├── main.py                # 통합 파이프라인 컨트롤러
├── core/
│   ├── scraper.py         # Gemini Advanced RPA 제어 (Playwright)
│   ├── audio_gen.py       # Edge-TTS 음성 합성 모듈
│   ├── image_gen.py       # Pollinations API 이미지 생성 모듈
│   └── prompts.py         # 페르소나 및 JSON 스키마 관리
├── assets/
│   ├── audio/             # 생성된 나레이션 (.mp3)
│   └── images/            # 생성된 9:16 이미지 (.jpg)
├── user_data/             # 브라우저 세션 데이터 (로그인 정보 유지)
├── .env                   # 환경 변수 설정 파일
└── latest_script.json     # 최근 생성된 대본 데이터 (Backup)
📝 로드맵 (Roadmap)
[x] Gemini Advanced 유료 계정 연동 및 JSON 대본 추출 자동화

[x] Edge-TTS 기반 장면별 나레이션 생성 최적화

[x] Grok RPA를 대체하는 API 기반 고성능 이미지 생성 모듈 완성

[ ] Next Step: MoviePy 기반 이미지 슬라이드 쇼 및 동적 자막 렌더링 엔진 구축

[ ] 배경음악(BGM) 자동 선곡 및 오디오 믹싱 기능 추가