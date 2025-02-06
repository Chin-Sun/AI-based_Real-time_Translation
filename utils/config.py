import os

# 🔹 Define the directory to store processed results
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "..", "results")

# 🔹 Ensure the results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

# 🔹 Supported Language Codes
LANGUAGE_CODES = {
    "English": "en",
    "French": "fr",
    "italian": "it",
    "Spanish": "es",
    "German": "de"
}
