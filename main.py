# main.py
import asyncio
import json
import os
from core.scraper import generate_script_from_gemini
from core.audio_gen import generate_audio_task
# [추가] 그록 대신 새로 만든 이미지 생성 모듈 임포트
from core.image_gen import generate_images_from_pollinations 

async def start_production():
    print("🚀 쇼츠 자동 제작 파이프라인 가동!")
    print("-" * 30)
    
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
    print("🎙️ 단계 2: 음성 합성을 시작합니다...")
    await generate_audio_task(script_data)
    print("✅ 음성 생성 완료 (경로: assets/audio/*.mp3)")
    print("-" * 30)

    # [수정] 4. 이미지 소스 생성 (API 호출)
    # generate_images_from_pollinations는 동기 함수이므로 await를 붙이지 않습니다.
    # 하지만성능을 위해 asyncio.to_thread로 감싸서 비동기처럼 돌리는 게 더 '컴공'스럽습니다.
    print("🎨 단계 3: 이미지 생성을 시작합니다...")
    visual_success = await asyncio.to_thread(generate_images_from_pollinations, script_data)
    
    if visual_success:
        print("\n🎬 [대본 + 음성 + 이미지] 모든 소스 준비 완료!")
        print("경로: assets/images/*.jpg")
    else:
        print("\n⚠️ 이미지 생성 중 일부 오류가 발생했습니다. 확인이 필요합니다.")

    print("-" * 30)
    print("이제 마지막 단계인 'MoviePy 영상 편집'만 남았습니다.")

if __name__ == "__main__":
    try:
        # 비동기 루프 시작
        asyncio.run(start_production())
    except KeyboardInterrupt:
        print("\n🛑 사용자에 의해 중단되었습니다.")