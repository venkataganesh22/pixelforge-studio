import os
import sys
from PIL import Image
import pytesseract
import cv2
import numpy as np

# Try to find tesseract executable in common Windows paths
tesseract_cmds = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    os.getenv("TESSERACT_CMD", "tesseract")
]
FOUND_TESSERACT_PATH = None

print("--- Initializing OCR Utils ---")
for cmd in tesseract_cmds:
    print(f"Checking for Tesseract at: {cmd}")
    if os.path.exists(cmd):
        FOUND_TESSERACT_PATH = cmd
        pytesseract.pytesseract.tesseract_cmd = cmd
        print(f"SUCCESS: Tesseract found and set to: {cmd}")
        break
else:
    print("WARNING: Tesseract executable not found in common paths.")

print(f"Current Tesseract cmd: {pytesseract.pytesseract.tesseract_cmd}")

def extract_text(img: Image.Image) -> str:
    """
    Extracts text from an image using Tesseract OCR with preprocessing.
    """
    # Double check path configuration inside function
    if FOUND_TESSERACT_PATH:
        pytesseract.pytesseract.tesseract_cmd = FOUND_TESSERACT_PATH
        if not os.access(FOUND_TESSERACT_PATH, os.X_OK):
             print(f"WARNING: Tesseract at {FOUND_TESSERACT_PATH} might not be executable!")
    else:
        print("CRITICAL: Tesseract path was not found during init!")

    # Add Tesseract directory to system PATH (helps with DLL loading and subprocess finding)
    if FOUND_TESSERACT_PATH:
        tess_dir = os.path.dirname(FOUND_TESSERACT_PATH)
        if tess_dir not in os.environ['PATH']:
            print(f"Adding Tesseract dir to PATH: {tess_dir}")
            os.environ['PATH'] += os.pathsep + tess_dir

    try:
        # Convert PIL to CV2
        img_np = np.array(img)
        
        # Convert to BGR if RGB (standard PIL is RGB)
        if len(img_np.shape) == 3:
            img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Preprocessing for better OCR
        # 1. Grayscale
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        
        # 2. Thresholding (Otsu's Binarization)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Run Tesseract
        tess_cmd = pytesseract.pytesseract.tesseract_cmd
        print(f"DEBUG: Executing Tesseract from: {tess_cmd}")
        print(f"DEBUG: Exists? {os.path.exists(tess_cmd)}")
        
        # Explicit verification
        if not os.path.exists(tess_cmd):
            print("CRITICAL: Tesseract executable disappeared!")
            return "Error: Internal configuration error. Tesseract file missing."

        print(f"Running Tesseract on image with shape {gray.shape}")
        text = pytesseract.image_to_string(gray)
        print(f"Tesseract output length: {len(text)}")
        
        if not text.strip():
            print("OCR Result: No text detected")
            return "No text detected. Try a clearer image."
            
        return text
        
    except pytesseract.TesseractNotFoundError:
        print("OCR Error: Tesseract not found (TesseractNotFoundError exception)")
        return "Error: Tesseract is not installed or not found in PATH."
    except Exception as e:
        print(f"OCR Error: {e}")
        return f"OCR Error: {str(e)}"

