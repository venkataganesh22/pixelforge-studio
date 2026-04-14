import os
import requests
import io
from PIL import Image

# Use the XL model for better reliability and quality
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

def get_headers():
    token = os.getenv("HF_TOKEN")
    if not token:
        return None
    return {"Authorization": f"Bearer {token}"}

def generate_image_from_text(prompt):
    headers = get_headers()
    if not headers:
        return None, "HF_TOKEN not found in environment variables."

    try:
        # We send the request to the new router URL
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=30)
        
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content)), None
        elif response.status_code == 404:
            return None, "Model not found. Please check the model ID."
        elif response.status_code == 503:
            return None, "Model is starting up. Try again in 20 seconds."
        else:
            return None, f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return None, f"Connection Error: {e}"
