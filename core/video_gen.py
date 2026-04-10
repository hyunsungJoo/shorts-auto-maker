# core/video_gen.py
import os

# MoviePy v2.x 버전 임포트 (v2.2.1 대응)
try:
    from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
except ImportError:
    # 혹시 모를 하위 버전 호환용
    from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

def create_shorts_video(script_data):
    print("🎬 단계 4: 영상 합성을 시작합니다... (MoviePy 2.x)")
    print("-" * 30)

    # 1. 경로 설정
    audio_dir = os.path.join(os.getcwd(), "assets", "audio")
    image_dir = os.path.join(os.getcwd(), "assets", "images")
    output_path = "final_shorts.mp4"
    
    # [중요] WSL 환경 한글 폰트 경로 (나눔고딕 기준)
    # fc-list :lang=ko 명령어로 본인 환경의 경로를 확인하세요.
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothicCoding.ttf" 

    scenes = script_data.get("scenes", [])
    clips = []

    for i, scene in enumerate(scenes, 1):
        try:
            # 파일 경로 (audio_gen.py 저장 규칙에 맞춤)
            audio_path = os.path.join(audio_dir, f"scene_{i-1}.mp3") 
            image_path = os.path.join(image_dir, f"scene_{i:02d}.jpg")

            if not os.path.exists(audio_path) or not os.path.exists(image_path):
                print(f"⚠️ 장면 {i}: 소스 파일 누락 (Audio: {os.path.exists(audio_path)}, Image: {os.path.exists(image_path)})")
                continue

            # 2. 오디오 클립 생성 및 길이 측정
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration

            # 3. 이미지 클립 생성 (MoviePy 2.x에서는 with_duration 사용 권장)
            img_clip = ImageClip(image_path).with_duration(duration)

            # 4. 자막(TextClip) 생성 (MoviePy 2.x 문법 적용)
            txt_clip = TextClip(
                text=scene.get("narration", ""),
                font=font_path,
                font_size=50,
                color='white',
                stroke_color='black',
                stroke_width=2,
                method='caption', # 자동 줄바꿈
                size=(img_clip.w * 0.8, None)
            ).with_duration(duration).with_position(('center', img_clip.h * 0.7))

            # 5. 합성 및 오디오 주입
            video_scene = CompositeVideoClip([img_clip, txt_clip]).with_audio(audio_clip)
            clips.append(video_scene)
            print(f"🎞️ 장면 {i} 합성 완료 ({duration:.2f}초)")

        except Exception as e:
            print(f"❌ 장면 {i} 에러: {e}")

    # 6. 최종 렌더링
    if clips:
        print("\n🚀 최종 인코딩 시작... (CPU 풀가동)")
        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        print(f"\n🎉 제작 완료! 파일: {output_path}")
        return True
    else:
        print("❌ 합성할 클립이 없습니다.")
        return False