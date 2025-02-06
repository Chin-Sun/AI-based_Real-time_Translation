import os
import datetime
from dotenv import load_dotenv
from transformers import T5Tokenizer, T5ForConditionalGeneration
import sys

# 🔹 Ensure Python can find `utils/`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import RESULTS_DIR  # ✅ Import shared directory

# Load environment variables
load_dotenv()

# Initialize the tokenizer and model
tokenizer = T5Tokenizer.from_pretrained("t5-base")
model = T5ForConditionalGeneration.from_pretrained("t5-base")

def summarize_text(video_transcript, save=True):
    """
    Generate a summary from a video transcript.
    If `save=True`, the summary is saved to a file.
    Returns the summary text and the file path if saved.
    """
    # Prepend the task prefix for T5
    input_text = "summarize: " + video_transcript
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    file_path = None  # Default: No file saved
    if save:
        file_path = save_summary(summary)

    return summary, file_path

def save_summary(summary_text, filename=None):
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_{timestamp}.txt"

    results_dir = RESULTS_DIR
    os.makedirs(results_dir, exist_ok=True)  # Ensure directory exists
    summary_path = os.path.join(results_dir, filename)

    print(f"📁 Saving summary at: {summary_path}")  # Debug line

    try:
        with open(summary_path, "w") as f:
            f.write(summary_text)
        print(f"✅ Summary saved: {summary_path}")
        return summary_path
    except Exception as e:
        print(f"❌ Error saving summary: {e}")
        return None

