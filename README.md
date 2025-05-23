[![Real Time Translation Based on AI](/ai.png)](https://drive.google.com/file/d/15HyKCIQCapjHQqBC5Ib1zLj0PZ-PJWSs/view?usp=sharing)
# Hackstorm Trio 🚀

Welcome to **Hackstorm Trio**, a project built in just **12 hours** during **ConUHacks IX**, a hackathon that brought together over 500 hackers.

# ClipGenius

This project is a streamlined platform designed to transform multilingual video content into intelligent, structured output. It leverages state-of-the-art AI models and toolkits to automate the generation of subtitles, summarize textual content, and support real-time translation and speech recognition. The solution is delivered through a simple and intuitive Streamlit-based user interface.


# 💡 Key Features
- **Intelligent Subtitle Generation**  
Automatically extracts and generates accurate subtitles from video using OpenCV and MoviePy, enabling seamless content accessibility.  

- **🧠 Precise Text Summarization**  
Employs Hugging Face Transformers for high-accuracy content summarization, making lengthy transcripts easier to digest.  

- **🗣 Real-Time Translation & Speech Recognition**  
Utilizes Google Translate API and OpenAI Whisper to provide multilingual audio processing and instant transcription for global users.  

- **🖥 Seamless User Interface**  
Built with Streamlit, the interface allows users to upload videos, configure output formats, and visualize results effortlessly.  

- **🌍 Multilingual Support**  
Designed for global scalability, it supports various languages and ensures smooth content delivery to international audiences.  

## 🛠️ Technologies Used
- **Frontend:** Streamlit
- **Backend:** Flask
- **Other:** OpenCV / Whisper / DeepTranslator / Transformers ...

## 📽️ Demo
🔗 [Live Demo](https://drive.google.com/file/d/15HyKCIQCapjHQqBC5Ib1zLj0PZ-PJWSs/view?usp=sharing) <!-- Replace with your deployed link or demo video -->



## 🖼️ Slides
🔗 [Link](https://docs.google.com/presentation/d/1qJCVv_6w7r9BogDKMFAWBl-uOdJzI8CR/edit?usp=sharing&ouid=114519568541965646466&rtpof=true&sd=true) <!-- Replace with your deployed link or demo video -->

## 📽️ Subtitle Generation Example
🔗 [Input video](https://drive.google.com/file/d/1x2HlTWOH2_rJJWeEU7xl5na-mtfCqKV2/view?usp=drive_link) <!-- Replace with your deployed link or demo video -->

🔗 [Output video](https://drive.google.com/file/d/1KZcbv3ilAZyG3vM2Q9QxBA-EalwO3Ls0/view?usp=sharing) <!-- Replace with your deployed link or demo video -->


## 🏃‍♂️ How to Run
### **1. Clone the Repository**
```bash
git clone https://github.com/shaghayegh-ghasemi/HackstormTrio.git
cd HackstormTrio
```

### **2. Install Dependencies**
```bash
conda env create -f environment.yml
```

### **3. Run the Application**
```bash
cd frontend
streamlit run frontend_app.py --server.port=8501

cd utils
python backend_app.py 
```

## 👥 Team Members
👤 [Shaghayegh Ghasemi](https://github.com/shaghayegh-ghasemi)  
👤 [Milad Khanchi](https://github.com/Milad-Khanchi)  
👤 [Qian Sun](https://github.com/Chin-Sun)  

## ⭐ Support & Contribution
- If you like this project, please give it a ⭐ on GitHub!
- Contributions are welcome! Feel free to open an issue or submit a pull request.
