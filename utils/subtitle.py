import os
import sys
import cv2
import numpy as np
import pysrt
from moviepy import *
from datetime import timedelta
from deep_translator import GoogleTranslator
from PIL import Image, ImageDraw, ImageFont

# 🔹 Ensure Python can find `utils/`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import RESULTS_DIR  # ✅ Use shared results directory
from utils.transcript import download_video, extract_audio, transcribe_audio  # ✅ Reuse transcript functions

# Ensure 'results' directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)


### **🔹 Function: Translate Transcription**
def translate_text(text, target_language="fr"):
    """
    Translate text to the specified target language using Google Translate.
    """
    translator = GoogleTranslator(source="auto", target=target_language)
    return translator.translate(text)


def translate_transcription(transcription, target_language="fr"):
    """
    Translate each segment in the transcription.
    """
    for segment in transcription["segments"]:
        segment["text"] = translate_text(segment["text"], target_language)
    return transcription


### **🔹 Function: Generate Subtitles in SRT Format**
def generate_srt(transcription, srt_filename="subtitles.srt"):
    """
    Generate an SRT subtitle file from the transcribed text.
    """
    def format_timestamp(seconds):
        td = timedelta(seconds=seconds)
        timestamp = str(td).replace(".", ",")[:12] if "." in str(td) else str(td) + ",000"
        return timestamp

    srt_path = os.path.join(RESULTS_DIR, srt_filename)
    srt_content = ""

    for i, segment in enumerate(transcription["segments"]):
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"].strip()
        srt_content += f"{i + 1}\n{start} --> {end}\n{text}\n\n"

    with open(srt_path, "w", encoding="utf-8") as srt_file:
        srt_file.write(srt_content)

    print(f"✅ Subtitles saved at: {srt_path}")
    return srt_path


### **🔹 Function: Overlay Subtitles on Video**
def overlay_subtitles(video_path, srt_path, output_filename="output_video.mp4"):
    """
    Overlay subtitles onto a video using OpenCV.
    """
    video = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))

    output_path = os.path.join(RESULTS_DIR, output_filename)
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    subs = pysrt.open(srt_path)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 40)

    max_width = frame_width - 100

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(frame_pil)

        current_time = video.get(cv2.CAP_PROP_POS_MSEC) / 1000

        for sub in subs:
            start_time = sub.start.ordinal / 1000.0
            end_time = sub.end.ordinal / 1000.0
            if start_time <= current_time <= end_time:
                text = sub.text
                words = text.split()
                lines = []
                current_line = ""

                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    bbox = draw.textbbox((0, 0), test_line, font=font)
                    text_width = bbox[2] - bbox[0]

                    if text_width > max_width:
                        lines.append(current_line)
                        current_line = word
                    else:
                        current_line = test_line

                lines.append(current_line)

                text_height = (bbox[3] - bbox[1] + 10) * len(lines)
                position = (50, frame_height - text_height - 50)
                y_offset = position[1]

                for line in lines:
                    draw.text((position[0], y_offset), line, font=font, fill=(255, 255, 255))
                    y_offset += bbox[3] - bbox[1] + 10

        frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
        out.write(frame)

    video.release()
    out.release()

    # 🔹 Add original audio back to the video
    final_output = os.path.join(RESULTS_DIR, "final_video_with_subtitles.mp4")
    video_clip = VideoFileClip(output_path)
    original_audio = VideoFileClip(video_path).audio
    final_video = video_clip.with_audio(original_audio)
    final_video.write_videofile(final_output, codec="libx264", audio_codec="aac")

    print(f"✅ Final video with subtitles saved at: {final_output}")
    return final_output


### **🔹 Main Function: Process Video & Generate Subtitles**
def generate_subtitles(gdrive_url, target_language="fr"):
    """
    Process video: Download, extract audio, transcribe, translate, generate subtitles, and overlay on video.
    """
    print("📥 Downloading video...")
    video_path = download_video(gdrive_url)

    print("🎵 Extracting audio...")
    audio_path = extract_audio(video_path)

    print("📝 Transcribing audio...")
    transcription = transcribe_audio(audio_path)

    print(f"🌍 Translating subtitles to {target_language}...")
    translated_transcription = translate_transcription(transcription, target_language)

    print("📜 Generating subtitle file...")
    srt_path = generate_srt(translated_transcription)

    print("🎬 Overlaying subtitles onto video...")
    final_video_path = overlay_subtitles(video_path, srt_path)

    return final_video_path


### **🔹 Run the Script for Testing**
if __name__ == "__main__":
    test_gdrive_url = "https://drive.google.com/file/d/1x2HlTWOH2_rJJWeEU7xl5na-mtfCqKV2/view?usp=drive_link"
    final_video = generate_subtitles(test_gdrive_url, "fr")
    print(f"✅ Final processed video: {final_video}")
