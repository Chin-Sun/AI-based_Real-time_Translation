import streamlit as st
import requests
import time
import os
import sys

# 🔹 Ensure the root directory is in the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import RESULTS_DIR
from utils.validators import is_valid_google_drive_link  # ✅ Import validation function

def timeline_tab():
    """⏳ Transcript with Timeline Tab"""
    st.subheader("⏳ Transcript with Timeline")

    drive_link = st.text_input("🔗 **Google Drive Video Link**", key="transcript_drive_link",
                            placeholder="Paste your video link here...",
                            help="Make sure your link is from Google Drive and shared publicly.")

    if st.button("🚀 Generate Transcript"):
        if not drive_link:
            st.warning("⚠️ Please enter a valid video link.")
        elif not is_valid_google_drive_link(drive_link):
            st.error("❌ Invalid Google Drive link. Please enter a correct Google Drive video link.")
        else:
            with st.status("⏳ Processing your video...", expanded=True) as status:
                steps = [
                    "📥 Downloading video...",
                    "🎵 Extracting audio...",
                    "📝 Transcribing with timestamps...",
                ]
                progress_bar = st.progress(0)

                for i, step in enumerate(steps):
                    st.write(step)
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(2)

                # 🔹 Send request to backend for transcript with timeline
                response = requests.post(
                    "http://127.0.0.1:5000/transcript",
                    json={"video_url": drive_link, "use_timeline": True},
                    timeout=300
                )

                if response.status_code == 200:
                    transcript_data = response.json()
                    transcript_text = transcript_data.get("transcript", "No transcript generated.")
                    file_path = transcript_data.get("file_path", "")

                    status.update(label="✅ Transcript Ready!", state="complete")
                    st.subheader("📜 Transcript with Timeline:")
                    st.text_area("Generated Transcript", transcript_text, height=300)

                    # 🔹 Provide a download button for the transcript file
                    if file_path and os.path.exists(file_path):
                        with open(file_path, "r") as file:
                            file_contents = file.read()
                        st.download_button(
                            label="📥 Download Transcript",
                            data=file_contents,
                            file_name="transcript_with_timestamps.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("❌ Transcript file not found! Check `results/` folder.")
                else:
                    status.update(label="❌ Error!", state="error")
                    st.error("Error: " + response.json().get("error", "Unknown error."))
