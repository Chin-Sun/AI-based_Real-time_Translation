import sys
import os

# 🔹 Ensure Python can find `utils/`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.transcript import transcript_with_timeline, transcript
from utils.summarization import summarize_text
from utils.translate import extract_and_translate_transcript
from utils.subtitle import generate_subtitles
from utils.config import RESULTS_DIR, LANGUAGE_CODES
from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# --- API 1: Extract Transcript from Video with timeline ---
@app.route('/transcript', methods=['POST'])
def get_transcript():
    """Extract transcript from uploaded video."""
    try:
        data = request.json
        video_url = data.get("video_url")
        use_timeline = data.get("use_timeline", False)  # Default to False

        if not video_url:
            return jsonify({"error": "No video URL provided"}), 400

        if use_timeline:
            transcript_path = transcript_with_timeline(video_url)  # Generate timeline transcript
            if transcript_path and os.path.exists(transcript_path):
                with open(transcript_path, "r") as file:
                    timeline_transcript = file.read()
                return jsonify({"transcript": timeline_transcript, "file_path": transcript_path})  # ✅ Correct path
            return jsonify({"error": "Failed to generate transcript with timestamps"}), 500
        else:
            plain_transcript = transcript(video_url)  # Generate plain transcript
            if plain_transcript:
                return jsonify({"transcript": plain_transcript})
            return jsonify({"error": "Failed to generate transcript"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- API 2: Summarization (Basic) ---
@app.route('/summarize', methods=['POST'])
def get_summary():
    """Generate AI-powered video summary and return file path for download"""
    try:
        data = request.json
        transcript_text = data.get("transcript")

        if not transcript_text:
            return jsonify({"error": "No transcript provided"}), 400

        # ✅ Now correctly handles both summary and file path
        summary, file_path = summarize_text(transcript_text, save=True)

        return jsonify({"summary": summary, "file_path": file_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# --- API 3: Translate Summary ---
@app.route('/translate', methods=['POST'])
def translate_text_api():
    """
    API endpoint to extract the transcript and translate it.
    """
    try:
        data = request.json
        video_url = data.get("video_url")
        target_language = data.get("target_language", "fr")  # Default to French

        if not video_url:
            return jsonify({"error": "No video URL provided"}), 400

        if target_language not in LANGUAGE_CODES.values():
            return jsonify({"error": "Unsupported language"}), 400

        transcript_data = extract_and_translate_transcript(video_url, target_language)

        if "error" in transcript_data:
            return jsonify({"error": transcript_data["error"]}), 500

        original_transcript_path = transcript_data.get("original_transcript")
        translated_transcript_path = transcript_data.get("translated_transcript")

        # Ensure original transcript is read correctly
        if original_transcript_path and os.path.exists(original_transcript_path):
            with open(original_transcript_path, "r", encoding="utf-8") as file:
                original_transcript = file.read()
        else:
            return jsonify({"error": "Failed to retrieve original transcript"}), 500

        # Ensure translated transcript is read correctly
        if translated_transcript_path and os.path.exists(translated_transcript_path):
            with open(translated_transcript_path, "r", encoding="utf-8") as file:
                translated_transcript = file.read()
        else:
            return jsonify({"error": "Failed to retrieve translated transcript"}), 500

        return jsonify({
            "message": "Translation completed successfully",
            "original_transcript": original_transcript,
            "original_transcript_path": original_transcript_path,
            "translated_transcript": translated_transcript,
            "translated_transcript_path": translated_transcript_path
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- API 4: Generate Subtitles ---
@app.route('/generate_subtitles', methods=['POST'])
def generate_subtitles_api():
    """API endpoint to generate subtitles for a given video."""
    try:
        data = request.json
        video_url = data.get("video_url")
        target_language = data.get("target_language")

        # 🔹 Validate inputs
        if not video_url:
            return jsonify({"error": "No video URL provided"}), 400
        if target_language not in LANGUAGE_CODES.values():
            return jsonify({"error": "Unsupported language. Supported languages: " + ", ".join(LANGUAGE_CODES.keys())}), 400

        # 🔹 Call the subtitle generation function
        final_video_path = generate_subtitles(video_url, target_language)
        
        # 🔹 Define subtitle file path (assuming the function saves subtitles as `subtitles.srt`)
        subtitle_file_path = os.path.join(os.path.dirname(final_video_path), "subtitles.srt")

        if not os.path.exists(final_video_path) or not os.path.exists(subtitle_file_path):
            return jsonify({"error": "Subtitle generation failed."}), 500

        # 🔹 Return subtitle file and processed video file path
        response_data = {
            "final_video": final_video_path,
            "subtitle_file": subtitle_file_path
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000, threads=4)