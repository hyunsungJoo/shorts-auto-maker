# 🎬 YouTube Shorts Auto Maker (RPA Version)

이 프로젝트는 추가 API 비용 없이 **기존 구독 계정(Gemini Advanced, Grok)**의 웹 세션을 활용하여 유튜브 쇼츠 영상을 자동으로 제작하는 툴입니다. 

컴퓨터 과학 전공자로서 학습한 **RPA(Robotic Process Automation)** 기술과 **비디오 편집 자동화** 기술을 결합하여 구현되었습니다.

---

## 🏗 프로젝트 구조 및 워크플로우



1.  **Script Generation (Gemini):** Playwright를 이용해 Gemini 웹에 접속, 특정 주제에 대한 쇼츠 대본(JSON) 생성.
2.  **Asset Generation (Grok):** 생성된 대본의 묘사를 바탕으로 Grok(x.com)에서 영상 및 이미지 소스를 생성하고 자동으로 다운로드.
3.  **Video Editing (MoviePy):** 수집된 영상, 자막, 배경음악을 레이어별로 합성하여 최종 `.mp4` 파일 렌더링.

---

## 🛠 기술 스택

-   **Language:** Python 3.12+
-   **Automation:** Playwright (Chromium)
-   **Video Engine:** MoviePy
-   **Environment Control:** python-dotenv, venv
-   **AI Models:** Google Gemini (Script), xAI Grok (Visuals)

---

## 🚀 시작하기 (Setup)

### 1. 가상환경 설정 및 패키지 설치
시스템 파이썬 환경을 보호하기 위해 반드시 가상환경 내에서 실행합니다.

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 필수 라이브러리 설치
pip install playwright moviepy python-dotenv
playwright install chromium