import streamlit as st
import os
import sys
import requests
import base64

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.validators import is_valid_google_drive_link
from utils.config import LANGUAGE_CODES, RESULTS_DIR

def subtitle_tab():
    """🔠 Subtitle Generation Tab"""
    st.subheader("🔠 Generate Subtitles")
    st.write("Enter a video URL and choose a target language to generate subtitles.")

    # 🔹 Input: Video URL
    drive_link = st.text_input("🔗 **Google Drive Video Link**", key="subtitle_drive_link",
                               placeholder="Paste your video link here...",
                               help="Make sure your link is from Google Drive and shared publicly.")

    # 🔹 Input: Target Language Selection
    languages = list(LANGUAGE_CODES.keys())
    target_language = st.selectbox("🌍 **Select Target Language for Subtitles**", languages, index=0)

    # 🔹 Get Language Code
    language_code = LANGUAGE_CODES[target_language]

    # 🔹 Generate Subtitles Button
    if st.button("🚀 Generate Subtitles"):
        if not drive_link:
            st.warning("⚠️ Please enter a valid video link.")
        elif not is_valid_google_drive_link(drive_link):
            st.error("❌ Invalid Google Drive link. Please enter a correct Google Drive video link.")
        elif not language_code:
            st.error("❌ Please enter a valid language code.")
        else:
            with st.status("⏳ Processing your video...", expanded=True):
                st.write("📥 Downloading video...")
                st.write("🎵 Extracting audio...")
                st.write(f"📝 Generating subtitles in {target_language} ({language_code})...")

                # 🔹 Send request to backend
                response = requests.post(
                    "http://127.0.0.1:5000/generate_subtitles",
                    json={"video_url": drive_link, "target_language": language_code},
                    timeout=300
                )

                if response.status_code == 200:
                    subtitle_data = response.json()
                    subtitle_path = subtitle_data.get("subtitle_file")
                    final_video = subtitle_data.get("final_video")  # This is the filename

                    st.success("✅ Subtitles generated successfully!")

                    # 🔹 Provide download buttons for subtitles
                    if subtitle_path:
                        subtitle_full_path = os.path.join(RESULTS_DIR, subtitle_path)
                        if os.path.exists(subtitle_full_path):
                            with open(subtitle_full_path, "r") as file:
                                file_contents = file.read()
                            st.download_button(
                                label="📥 Download Subtitles (SRT)",
                                data=file_contents,
                                file_name="subtitles.srt",
                                mime="text/plain"
                            )

                    # 🔹 Display Video and Provide Download Button
                    if final_video:
                        final_video_path = os.path.join(RESULTS_DIR, final_video)

                        if os.path.exists(final_video_path):
                            with open(final_video_path, "rb") as video_file:
                                video_bytes = video_file.read()

                            video_base64 = base64.b64encode(video_bytes).decode("utf-8")

                            # 🔹 Display Video (Centered with Size Limit)
                            st.markdown(
                                f"""
                                <style>
                                .centered-video {{
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                }}
                                video {{
                                    max-width: 640px;
                                    max-height: 360px;
                                    border-radius: 10px;
                                }}
                                </style>
                                <div class="centered-video">
                                    <video controls>
                                        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                                        Your browser does not support the video tag.
                                    </video>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            # 🔹 Download Button for Video
                            with open(final_video_path, "rb") as file:
                                st.download_button(
                                    label="🎬 Download Final Video",
                                    data=file,
                                    file_name="final_video_with_subtitles.mp4",
                                    mime="video/mp4"
                                )
                        else:
                            st.error("❌ Error: Final video not found.")
                else:
                    st.error(f"❌ Error: {response.json().get('error', 'Unknown error')}")
