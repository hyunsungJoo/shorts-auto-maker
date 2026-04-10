# core/image_gen.py
import requests
import os
import time
import random

def generate_images_from_pollinations(script_data):
    print("🎨 단계 3: 이미지 소스 생성을 시작합니다... (Throttling 적용)")
    print("-" * 30)

    images_dir = os.path.join(os.getcwd(), "assets", "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    scenes = script_data.get("scenes", [])
    success_count = 0
    
    for i, scene in enumerate(scenes, 1):
        prompt = scene.get("visual_prompt", scene.get("narration", ""))
        file_path = os.path.join(images_dir, f"scene_{i:02d}.jpg")

        # 이미 이미지가 존재하면 스킵 (중복 생성 방지용 - 필요시 주석 해제)
        # if os.path.exists(file_path): 
        #    success_count += 1; continue

        optimized_prompt = f"{prompt[:100]}, 1990s ghibli style, vintage anime, high quality" # 100자 제한
        encoded_prompt = requests.utils.quote(optimized_prompt)
        
        # 429 방지를 위해 요청마다 랜덤 시드 부여
        seed = random.randint(1, 999999)
        api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=720&height=1280&seed={seed}&nologo=true"

        # --- 재시도 로직 시작 ---
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🖌️ [장면 {i}/{len(scenes)}] 생성 중... (시도 {attempt+1}/{max_retries})")
                response = requests.get(api_url, timeout=40) # 타임아웃 넉넉히

                if response.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    print(f"✅ 저장 완료: scene_{i:02d}.jpg")
                    success_count += 1
                    break # 성공했으므로 재시도 루프 탈출
                
                elif response.status_code == 429:
                    wait_time = (attempt + 1) * 10 # 429일 땐 더 길게 대기
                    print(f"⚠️ Rate Limit(429) 발생! {wait_time}초 후 재시도합니다...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ 서버 에러 (HTTP: {response.status_code})")
                    break

            except Exception as e:
                print(f"❌ 연결 오류: {e}")
                time.sleep(5) # 잠시 대기 후 다시 시도

        # 다음 장면 요청 전 서버에게 쉴 시간을 줍니다 (가장 중요!)
        # 컴공식 'Throttling' 기법
        if i < len(scenes):
            sleep_sec = 5 
            print(f"💤 서버 부하 방지를 위해 {sleep_sec}초 대기...")
            time.sleep(sleep_sec)

    print("-" * 30)
    return success_count == len(scenes)