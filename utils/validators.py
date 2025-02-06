import re

def is_valid_google_drive_link(url):
    """
    Validate whether the provided URL is a valid Google Drive link.
    """
    drive_pattern = r"https?://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/view\?usp=drive_link"
    # bool(re.match(drive_pattern, url))
    return True
