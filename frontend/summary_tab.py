import streamlit as st
import requests
import time
import sys
import os

# Add the root project directory to Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.transcript import transcript
from utils.validators import is_valid_google_drive_link  # ✅ Import validation function
from utils.config import RESULTS_DIR

def summary_tab():
    """📜 Video Summarization Tab"""
    st.subheader("📜 Video Summary")

    drive_link = st.text_input("🔗 **Google Drive Video Link**", key="summary_drive_link",
                               placeholder="Paste your video link here...",
                               help="Make sure your link is from Google Drive and shared publicly.")

    if st.button("🚀 Generate Summary"):
        if not drive_link:
            st.warning("⚠️ Please enter a valid video link.")
        elif not is_valid_google_drive_link(drive_link):
            st.error("❌ Invalid Google Drive link. Please enter a correct Google Drive video link.")
        else:
            with st.status("⏳ Processing your video...", expanded=True) as status:
                steps = [
                    "📥 Downloading video...",
                    "🎵 Extracting audio...",
                    "📝 Transcribing...",
                    "🤖 Generating summary...",
                ]

                progress_bar = st.progress(0)

                for i, step in enumerate(steps):
                    st.write(step)
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(2)  # Simulating processing time

                # 🔹 Extract transcript before calling summarization API
                st.write("⏳ Extracting transcript from video...")
                transcript_text = transcript(drive_link)  # Calls transcript function

                if not transcript_text:
                    status.update(label="❌ Error!", state="error")
                    st.error("Failed to extract transcript.")
                    return

                # 🔹 Send transcript to backend for summarization
                response = requests.post(
                    "http://127.0.0.1:5000/summarize",
                    json={"transcript": transcript_text}  # ✅ Now sending "transcript"
                )

                if response.status_code == 200:
                    summary_data = response.json()
                    summary_text = summary_data.get("summary", "No summary generated.")
                    file_path = summary_data.get("file_path")

                    status.update(label="✅ Summary Ready!", state="complete")
                    st.subheader("📜 Summary:")
                    st.text_area("Generated Summary", summary_text, height=200)

                    # 🔹 Provide a download button for the summary file
                    if file_path and os.path.exists(file_path):
                        with open(file_path, "r") as file:
                            file_contents = file.read()
                        st.download_button(
                            label="📥 Download Summary",
                            data=file_contents,
                            file_name="summary.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("❌ Summary file not found!")

                else:
                    status.update(label="❌ Error!", state="error")
                    st.error("Error: " + response.json().get("error", "Unknown error."))
