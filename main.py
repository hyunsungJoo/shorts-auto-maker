# main.py
import asyncio
import json
import os
from core.scraper import generate_script_from_gemini
from core.audio_gen import generate_audio_task
from core.image_gen import generate_images_from_pollinations
from core.video_gen import create_shorts_video # [추가] 영상 합성 모듈 임포트

async def start_production():
    print("🚀 쇼츠 자동 제작 파이프라인 가동 (Full Version)")
    print("-" * 30)
    
    # 1. 제미나이로부터 대본 생성 (RPA)
    script_data = await generate_script_from_gemini()
    
    if not script_data:
        print("❌ 단계 1(대본 생성) 실패로 인해 중단합니다.")
        return

    # 2. 결과물 저장 (백업 및 데이터 전달용)
    with open("latest_script.json", "w", encoding="utf-8") as f:
        json.dump(script_data, f, ensure_ascii=False, indent=2)
    print("💾 대본이 'latest_script.json'에 저장되었습니다.")

    # 3. 음성 파일 생성 (Edge-TTS)
    print("🎙️ 단계 2: 음성 합성을 시작합니다...")
    await generate_audio_task(script_data)
    print("✅ 음성 생성 완료 (경로: assets/audio/*.mp3)")
    print("-" * 30)

    # 4. 이미지 소스 생성 (Pollinations API)
    # CPU 부하 분산을 위해 to_thread로 실행
    print("🎨 단계 3: 이미지 생성을 시작합니다...")
    visual_success = await asyncio.to_thread(generate_images_from_pollinations, script_data)
    
    if not visual_success:
        print("\n⚠️ 이미지 생성 중 일부 오류가 발생했습니다. 확인이 필요합니다.")
        # 이미지가 하나도 없으면 영상 제작이 어려우므로 체크 필요

    print("-" * 30)

    # 5. 영상 합성 (MoviePy) - [최종 단계 추가]
    # 가장 무거운 작업이므로 역시 별도 스레드에서 처리합니다.
    print("🎬 단계 4: 최종 영상 편집 및 렌더링을 시작합니다...")
    video_success = await asyncio.to_thread(create_shorts_video, script_data)

    if video_success:
        print("\n✅ 모든 공정이 완료되었습니다! 'final_shorts.mp4'를 확인하세요.")
    else:
        print("\n❌ 영상 합성 단계에서 오류가 발생했습니다.")

if __name__ == "__main__":
    try:
        # 비동기 루프 시작
        asyncio.run(start_production())
    except KeyboardInterrupt:
        print("\n🛑 사용자에 의해 중단되었습니다.")