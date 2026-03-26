import os
import json
import re
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from core.prompts import get_automated_shorts_prompt

load_dotenv()

async def generate_script_from_gemini():
    """비동기 방식으로 제미나이에서 대본을 생성하고 추출"""
    async with async_playwright() as p:
        user_data_dir = os.getenv("CHROME_USER_DATA")
        profile = os.getenv("CHROME_PROFILE", "Default")

        if not user_data_dir:
            print("❌ 에러: .env 파일에 CHROME_USER_DATA 경로를 설정해주세요.")
            return None

        # 브라우저 실행
        context = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False, # 동작 확인을 위해 브라우저를 띄움
            args=[f"--profile-directory={profile}"]
        )
        
        page = await context.new_page()
        
        try:
            print("🌐 제미나이 접속 중...")
            await page.goto("https://gemini.google.com/app", timeout=60000)
            
            prompt = get_automated_shorts_prompt()
            
            input_selector = "div[role='textbox']"
            await page.wait_for_selector(input_selector, timeout=30000)
            
            print("🤖 AI에게 주제 기획 및 대본 작성을 요청합니다...")
            await page.fill(input_selector, prompt)
            await page.keyboard.press("Enter")
            
            # 답변이 생성될 때까지 대기
            response_selector = ".model-response-text"
            await page.wait_for_selector(response_selector, timeout=60000)
            
            # 스트리밍 답변 완료를 위해 잠시 추가 대기
            await asyncio.sleep(7) 
            
            raw_text = await page.inner_text(response_selector)
            
            # JSON 데이터 추출
            json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            
            if json_match:
                script_data = json.loads(json_match.group())
                print(f"\n✅ 주제 선정 완료: {script_data.get('topic')}")
                await context.close()
                return script_data
            else:
                print("❌ 에러: 응답에서 JSON 형식을 찾지 못했습니다.")
                await context.close()
                return None

        except Exception as e:
            print(f"❌ Scraper 오류 발생: {e}")
            await context.close()
            return None