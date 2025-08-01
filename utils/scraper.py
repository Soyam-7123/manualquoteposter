# --- utils/scraper.py ---
import requests
import os
from dotenv import load_dotenv

load_dotenv()
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

def download_unsplash_images_api(query="nature", count=5, save_dir="images/"):
    os.makedirs(save_dir, exist_ok=True)
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page={count}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url).json()

    for i, result in enumerate(response.get("results", [])):
        img_url = result["urls"]["regular"]
        img_data = requests.get(img_url).content
        with open(os.path.join(save_dir, f"{query}_{i}.jpg"), "wb") as f:
            f.write(img_data)
    return f"{len(response.get('results', []))} Unsplash images downloaded."