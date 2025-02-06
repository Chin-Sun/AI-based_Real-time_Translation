import os
import gdown
import whisper
from moviepy import *

import sys
import os

# 🔹 Ensure Python can find `utils/`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import RESULTS_DIR  # ✅ Import shared directory

# Ensure FFmpeg path is included
os.environ["PATH"] += os.pathsep + "C:/ffmpeg/bin"

def seconds_to_hms(seconds):
    """
    Converts seconds into hours, minutes, and seconds (hh:mm:ss).
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def get_google_drive_url(file_id):
    """
    Generates the direct download URL for a Google Drive file.
    """
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def download_video(drive_link, output_path="video.mp4"):
    """
    Download video from Google Drive given its shareable link.
    """
    try:
        file_id = drive_link.split("/d/")[1].split("/")[0]  # Extract file ID
        gdown.download(f"https://drive.google.com/uc?id={file_id}", output_path, quiet=False)
        print(f"✅ Video downloaded successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Error downloading video: {e}")
        return None

def extract_audio(video_path, audio_path="audio.wav"):
    """
    Extract audio from a video file.
    """
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        print(f"✅ Audio extracted successfully: {audio_path}")
        return audio_path
    except Exception as e:
        print(f"❌ Error extracting audio: {e}")
        return None

def transcribe_audio(audio_path, model_size="base"):
    """
    Transcribe audio to text using Whisper AI.
    """
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_path)
        return result
    except Exception as e:
        print(f"❌ Error transcribing audio: {e}")
        return None

# 🔹 Transcript Function (No Timeline, for Summarization)
def transcript(drive_link):
    """
    Get transcript from video URL (Plain Text).
    """
    video_path = download_video(drive_link)
    if not video_path:
        return None

    audio_path = extract_audio(video_path)
    if not audio_path:
        return None

    transcription_result = transcribe_audio(audio_path)
    if transcription_result:
        return transcription_result["text"]
    
    return None

def transcript_with_timeline(drive_link):
    """
    Get transcript with timestamps from video URL and save it in a shared directory.
    """
    transcript_path = os.path.join(RESULTS_DIR, "transcription_with_timestamps.txt")

    video_path = download_video(drive_link)
    if not video_path:
        return None

    audio_path = extract_audio(video_path)
    if not audio_path:
        return None

    transcription_result = transcribe_audio(audio_path)
    if not transcription_result:
        return None

    # Save the transcription with timestamps
    try:
        with open(transcript_path, 'w') as f:
            for segment in transcription_result['segments']:
                start_time = segment['start']
                text = segment['text']
                time_str = seconds_to_hms(start_time)  # Convert to hh:mm:ss
                f.write(f"At {time_str}: {text}\n")
        print(f"✅ Transcription with timestamps saved: {transcript_path}")
        return transcript_path  # Return absolute path
    except Exception as e:
        print(f"❌ Error saving transcription: {e}")
        return None

# 🔹 Save transcript (Plain Text)
def save_transcript(transcript, filename="transcript.txt"):
    """
    Save transcript to a text file.
    """
    try:
        with open(filename, "w") as f:
            f.write(transcript)
        print(f"✅ Transcript saved: {filename}")
    except Exception as e:
        print(f"❌ Error saving transcript: {e}")