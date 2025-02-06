import streamlit as st
from summary_tab import summary_tab
from transcript_tab import timeline_tab
from translate_tab import translate_tab
from subtitle_tab import subtitle_tab


# Set Page Configuration
st.set_page_config(
    page_title="Hackstorm Trio",
    page_icon="⚡",
    layout="wide"
)

# Centered layout with optimal whitespace
left_space, content, right_space = st.columns([1, 3, 1])  # Adjusted to make content wider

with content:  # Content will take 3/5 of the page width
    st.markdown("<h2 style='text-align: center;'> Welcome to Hackstorm Trio's AI-powered Video Processing Tool!</h2>", unsafe_allow_html=True)

    # 🔹 Input Field Styling 🔹
    st.markdown(
        """
        <style>
        .small-input input {
            width: 50% !important;  /* Adjust width (balanced) */
            margin: 0 auto !important; /* Center the input field */
            display: flex !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 
    # --- Navigation Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["⏳ Timeline", "📜 Summary", "🌍 Translate", "🔠 Add Subtitles"])

    # --- Load Each Feature in a Separate File ---
    with tab1:
        timeline_tab()

    with tab2:
        summary_tab()

    with tab3:
        translate_tab()

    with tab4:
        subtitle_tab()

    # --- Push Contributors Section Lower ---
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    # --- 📌 Contributors Section ---
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>👨‍💻 Hackstorm Trio Contributors 🚀</h2>", unsafe_allow_html=True)

    # Contributor details (Replace with actual image URLs and GitHub links)
    contributors = [
        {
            "name": "Shaghayegh Ghasemi",
            "image": "https://i.imgur.com/3OfYuGo.jpeg",
            "github": "https://github.com/shaghayegh-ghasemi"
        },
        {
            "name": "Milad Khanchi",
            "image": "https://i.imgur.com/OnJeHZS.jpeg",
            "github": "https://github.com/Milad-Khanchi"
        },
        {
            "name": "Qian Sun",
            "image": "https://i.imgur.com/wac0u2c.jpeg",
            "github": "https://github.com/chin-sun"
        }
    ]

    # Custom CSS for Centering Name & GitHub Link
    st.markdown(
        """
        <style>
        .profile-container {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            text-align: center;
        }
        .profile-pic {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid #ddd;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .profile-text {
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        }
        .profile-link {
            text-align: center;
            font-size: 14px;
            color: #007BFF;
            text-decoration: none;
            font-weight: bold;
        }
        .profile-link:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Centered Layout for Contributors
    cols = st.columns(3)

    for i, contributor in enumerate(contributors):
        with cols[i]:
            st.markdown(
                f"""
                <div class="profile-container">
                    <img src="{contributor['image']}" class="profile-pic">
                    <p class="profile-text">{contributor['name']}</p>
                    <a href="{contributor['github']}" class="profile-link">🔗 GitHub Profile</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Footer Branding
    st.markdown("---")
    st.markdown("🔹 **Hackstorm Trio** - AI-Powered Innovation 🚀")
    st.markdown("💡 Developed with ❤️ by Hackstorm Trio")
