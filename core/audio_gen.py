# core/audio_gen.py
import asyncio
import edge_tts
import os

async def generate_audio_task(script_data):
    """데이터를 직접 전달받아 음성을 생성하는 핵심 함수"""
    audio_dir = "assets/audio"
    os.makedirs(audio_dir, exist_ok=True)
    
    # 쇼펜하우어 톤에 맞는 묵직한 남성 목소리
    voice = "ko-KR-InJoonNeural" 
    scenes = script_data.get("scenes", [])
    
    print(f"🎙️ [Audio] '{script_data.get('title')}' 음성 생성 중...")

    for i, scene in enumerate(scenes):
        text = scene.get("text", "")
        if not text: continue

        output_path = f"{audio_dir}/scene_{i}.mp3"
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        print(f"   - 장면 {i} 완료")

    print("✅ 모든 음성 파일 생성 완료!")