import asyncio
import json
import os
from core.scraper import generate_script_from_gemini
from core.audio_gen import generate_audio_task

async def start_production():
    print("🚀 쇼츠 자동 제작 파이프라인 가동!")
    
    # 1. 제미나이로부터 대본 생성 (비동기 호출)
    script_data = await generate_script_from_gemini()
    
    if not script_data:
        print("❌ 단계 1(대본 생성) 실패로 인해 중단합니다.")
        return

    # 2. 결과물 저장 (백업용)
    with open("latest_script.json", "w", encoding="utf-8") as f:
        json.dump(script_data, f, ensure_ascii=False, indent=2)
    print("💾 대본이 'latest_script.json'에 저장되었습니다.")

    # 3. 음성 파일 생성 (비동기 호출)
    print("🎙️ 음성 합성을 시작합니다...")
    await generate_audio_task(script_data)
    
    print("\n🎬 [대본 + 음성] 세트 준비 완료!")
    print("경로: assets/audio/*.mp3")
    print("-" * 30)
    print("이제 Grok 자동화 모듈을 실행할 준비가 되었습니다.")

if __name__ == "__main__":
    # 비동기 루프 시작
    asyncio.run(start_production())