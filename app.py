import streamlit as st
import io
import os
import numpy as np
from PIL import Image, ImageEnhance

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PixelForge Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg-primary: #0a0a0f;
    --bg-card: #12121a;
    --bg-card2: #1a1a26;
    --accent: #7c6af7;
    --accent2: #e879f9;
    --accent3: #38bdf8;
    --text-primary: #f0f0ff;
    --text-muted: #8888aa;
    --border: rgba(124,106,247,0.2);
    --glow: 0 0 30px rgba(124,106,247,0.15);
}

/* Global */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* Main background */
.stApp {
    background: radial-gradient(ellipse at 20% 20%, rgba(124,106,247,0.08) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 80%, rgba(232,121,249,0.06) 0%, transparent 60%),
                var(--bg-primary) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* Header */
.hero-header {
    text-align: center;
    padding: 2rem 0 1.5rem;
}
.hero-header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7c6af7 0%, #e879f9 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -1px;
}
.hero-header p {
    color: var(--text-muted);
    font-size: 1.05rem;
    margin-top: 0.4rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 14px !important;
    padding: 6px !important;
    border: 1px solid var(--border) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: var(--text-muted) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    padding: 8px 18px !important;
    border: none !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: white !important;
    box-shadow: 0 2px 12px rgba(124,106,247,0.35) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.5rem !important;
}

/* Cards */
.feature-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    box-shadow: var(--glow);
    transition: border-color 0.2s;
}
.feature-card:hover { border-color: rgba(124,106,247,0.45); }

.result-card {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.2rem;
    margin-top: 1rem;
}

/* Section labels */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.5rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 1.5rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(124,106,247,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,106,247,0.45) !important;
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #059669 0%, #0891b2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    width: 100% !important;
    padding: 0.6rem !important;
    box-shadow: 0 4px 15px rgba(5,150,105,0.3) !important;
}

/* Sliders */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}
.stSlider [data-baseweb="slider"] div[data-testid="stThumbValue"] {
    color: var(--accent) !important;
}

/* Selectbox */
.stSelectbox [data-baseweb="select"] > div {
    background: var(--bg-card2) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 14px !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}

/* Text area */
.stTextArea textarea {
    background: var(--bg-card2) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Text input */
.stTextInput input {
    background: var(--bg-card2) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* Success / info / warning */
.stSuccess { background: rgba(5,150,105,0.12) !important; border-color: #059669 !important; border-radius: 10px !important; }
.stInfo    { background: rgba(56,189,248,0.10) !important; border-color: #38bdf8 !important; border-radius: 10px !important; }
.stWarning { background: rgba(245,158,11,0.10) !important; border-color: #f59e0b !important; border-radius: 10px !important; }
.stError   { background: rgba(239,68,68,0.10)  !important; border-color: #ef4444 !important; border-radius: 10px !important; }

/* Image display */
.stImage { border-radius: 12px; overflow: hidden; }

/* Metric */
[data-testid="stMetric"] {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 0.8rem 1rem !important;
}
[data-testid="stMetricLabel"] { color: var(--text-muted) !important; }
[data-testid="stMetricValue"] { color: var(--text-primary) !important; font-family: 'Syne', sans-serif !important; }

/* Divider */
hr { border-color: var(--border) !important; }

/* Expander */
.streamlit-expanderHeader {
    background: var(--bg-card2) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* Spinner */
.stSpinner > div > div { border-top-color: var(--accent) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def pil_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    if fmt.upper() in ("JPEG", "JPG") and img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")
    img.save(buf, format=fmt.upper() if fmt.upper() != "JPG" else "JPEG")
    return buf.getvalue()

def show_image_pair(original, result, left_label="Original", right_label="Result"):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="section-label">{left_label}</div>', unsafe_allow_html=True)
        st.image(original, use_container_width=True)
    with c2:
        st.markdown(f'<div class="section-label">{right_label}</div>', unsafe_allow_html=True)
        st.image(result, use_container_width=True)

def download_widget(img: Image.Image, filename: str, fmt: str = "PNG"):
    data = pil_to_bytes(img, fmt)
    mime = "image/jpeg" if fmt.upper() in ("JPEG","JPG") else f"image/{fmt.lower()}"
    st.download_button(
        label="⬇  Download Image",
        data=data,
        file_name=filename,
        mime=mime,
        use_container_width=True,
    )

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1>✦ PixelForge Studio</h1>
    <p>AI-powered image processing & generation workspace</p>
</div>
""", unsafe_allow_html=True)


   
# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🖼  Image Studio", "✨  AI Image Generator"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — IMAGE STUDIO
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Upload your image")
    uploaded = st.file_uploader(
        "Drag & drop or click to browse",
        type=["jpg", "jpeg", "png", "bmp", "webp", "tiff", "gif"],
        label_visibility="collapsed",
    )

    if uploaded:
        original_image = Image.open(uploaded)
        w, h = original_image.size
        mode = original_image.mode

        # Stats bar
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Width", f"{w}px")
        m2.metric("Height", f"{h}px")
        m3.metric("Mode", mode)
        m4.metric("Format", uploaded.name.split(".")[-1].upper())

        st.markdown("---")

        # ── Sub-tabs ──────────────────────────────────────────────────────────
        s1, s2, s3, s4, s5 = st.tabs([
            "🔄 Convert", "🎨 Filters", "✏ Sketch", "📝 OCR", "✂ Crop"
        ])

        # ── FORMAT CONVERSION ─────────────────────────────────────────────────
        with s1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown("**Convert image to another format**")
            col1, col2 = st.columns([1, 1])
            with col1:
                target_fmt = st.selectbox(
                    "Target format",
                    ["PNG", "JPEG", "BMP", "WEBP", "TIFF", "ICO"],
                    index=0,
                )
            with col2:
                if target_fmt == "JPEG":
                    quality = st.slider("JPEG Quality", 10, 100, 90)
                else:
                    quality = 95

            if st.button("Convert Now", key="convert_btn"):
                from utils.format_convert import convert_image
                with st.spinner("Converting…"):
                    converted = convert_image(original_image.copy(), target_fmt)
                st.success(f"Converted to {target_fmt} successfully!")
                show_image_pair(original_image, converted, "Original", f"→ {target_fmt}")
                ext = "jpg" if target_fmt == "JPEG" else target_fmt.lower()
                download_widget(converted, f"converted.{ext}", target_fmt)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── FILTERS ───────────────────────────────────────────────────────────
        with s2:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown("**Apply OpenCV image filters**")

            FILTERS = {
                "🌑 Grayscale":   "grayscale",
                "🌫 Gaussian Blur": "blur",
                "🔄 Invert":      "invert",
                "🟤 Sepia":       "sepia",
                "⚡ Edge Detect": "edge",
                "🔆 Sharpen":     "sharpen",
                "🗿 Emboss":      "emboss",
                "☀ Brightness":  "brightness",
            }

            filter_label = st.selectbox("Choose a filter", list(FILTERS.keys()))
            filter_type  = FILTERS[filter_label]

            intensity = 15
            if filter_type in ("blur", "brightness"):
                intensity = st.slider("Intensity", 1, 51, 15, step=2,
                                      help="For blur: kernel size (odd). For brightness: boost value.")

            if st.button("Apply Filter", key="filter_btn"):
                from utils.image_filters import apply_filter
                with st.spinner(f"Applying {filter_label}…"):
                    result = apply_filter(original_image.copy(), filter_type, intensity=intensity)
                show_image_pair(original_image, result, "Original", filter_label)
                download_widget(result, f"filtered_{filter_type}.png", "PNG")

            st.markdown('</div>', unsafe_allow_html=True)

        # ── PENCIL SKETCH ─────────────────────────────────────────────────────
        with s3:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown("**Transform your photo into a pencil sketch**")

            col1, col2 = st.columns([1,1])
            with col1:
                sketch_mode = st.radio("Sketch style", ["Classic B&W", "Coloured"], horizontal=True)
            with col2:
                blur_strength = st.slider("Blur Strength", 5, 51, 21, step=2,
                                          help="Higher = softer pencil strokes")

            if st.button("Generate Sketch", key="sketch_btn"):
                import cv2
                with st.spinner("Sketching…"):
                    img_np = np.array(original_image.convert("RGB"))
                    gray   = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
                    inv    = cv2.bitwise_not(gray)
                    blurred = cv2.GaussianBlur(inv, (blur_strength, blur_strength), 0)
                    sketch_bw = cv2.divide(gray, 255 - blurred, scale=256)
                    if sketch_mode == "Coloured":
                        sketch_img  = Image.fromarray(sketch_bw)
                        color_layer = original_image.convert("RGB").resize(sketch_img.size)
                        result = Image.blend(sketch_img.convert("RGB"), color_layer, alpha=0.3)
                    else:
                        result = Image.fromarray(sketch_bw)

                show_image_pair(original_image, result, "Original", "✏ Sketch")
                download_widget(result, "sketch.png", "PNG")

            st.markdown('</div>', unsafe_allow_html=True)

        # ── OCR ───────────────────────────────────────────────────────────────
        with s4:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown("**Extract text from your image using Tesseract OCR**")

            preprocess = st.checkbox("Apply preprocessing (threshold + denoise)", value=True)

            if st.button("Extract Text", key="ocr_btn"):
                try:
                    import pytesseract, cv2
                    with st.spinner("Reading text…"):
                        img_np = np.array(original_image.convert("RGB"))
                        gray   = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
                        if preprocess:
                            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                        text = pytesseract.image_to_string(gray)

                    if text.strip():
                        st.success(f"Extracted {len(text.split())} words")
                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        st.text_area("Extracted Text", text, height=250)
                        st.download_button(
                            "⬇  Download as .txt",
                            data=text,
                            file_name="extracted_text.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning("No text detected. Try a clearer image with printed or handwritten text.")
                except Exception as e:
                    st.error(f"OCR Error: {e}\n\nMake sure Tesseract is installed: `sudo apt install tesseract-ocr`")

            st.markdown('</div>', unsafe_allow_html=True)

        # ── CROP ─────────────────────────────────────────────────────────────
        with s5:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown("**Crop your image to a specific region**")

            st.image(original_image, caption=f"Original ({w}×{h})", use_container_width=True)
            st.markdown("---")
            st.markdown("**Set crop boundaries (pixels)**")

            c1, c2 = st.columns(2)
            c3, c4 = st.columns(2)
            with c1: left   = st.number_input("Left",   0, w-1, 0)
            with c2: right  = st.number_input("Right",  1, w,   w)
            with c3: top    = st.number_input("Top",    0, h-1, 0)
            with c4: bottom = st.number_input("Bottom", 1, h,   h)

            # Quick presets
            st.markdown("**Or use a preset ratio:**")
            p1, p2, p3, p4 = st.columns(4)
            preset = None
            if p1.button("1:1 Square"):  preset = "1:1"
            if p2.button("16:9 Wide"):   preset = "16:9"
            if p3.button("4:3 Classic"): preset = "4:3"
            if p4.button("3:2 Photo"):   preset = "3:2"

            if preset:
                ratios = {"1:1":(1,1), "16:9":(16,9), "4:3":(4,3), "3:2":(3,2)}
                rw, rh = ratios[preset]
                new_h = int(w * rh / rw)
                if new_h <= h:
                    top_preset = (h - new_h) // 2
                    st.session_state["crop_vals"] = (0, top_preset, w, top_preset + new_h)
                    st.info(f"Preset {preset}: left=0, top={top_preset}, right={w}, bottom={top_preset+new_h}")

            if st.button("Crop Image", key="crop_btn"):
                if left >= right or top >= bottom:
                    st.error("Invalid crop: right must be > left and bottom > top.")
                else:
                    with st.spinner("Cropping…"):
                        cropped = original_image.crop((int(left), int(top), int(right), int(bottom)))
                    cw, ch = cropped.size
                    st.success(f"Cropped to {cw}×{ch}px")
                    show_image_pair(original_image, cropped, "Original", "✂ Cropped")
                    download_widget(cropped, "cropped.png", "PNG")

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center; padding: 4rem 2rem; color: #8888aa;">
            <div style="font-size:4rem; margin-bottom:1rem;">🖼</div>
            <div style="font-size:1.1rem; font-weight:500; color:#b0b0cc;">Upload an image to get started</div>
            <div style="font-size:0.85rem; margin-top:0.4rem;">Supports JPG, PNG, BMP, WEBP, TIFF, GIF</div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — AI IMAGE GENERATOR
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(124,106,247,0.12) 0%, rgba(232,121,249,0.08) 100%);
                border: 1px solid rgba(124,106,247,0.25); border-radius:16px; padding:1.4rem; margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif; font-size:1.2rem; font-weight:700; 
                    background:linear-gradient(135deg,#7c6af7,#e879f9); -webkit-background-clip:text;
                    -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:0.4rem;">
            ✨ Stable Diffusion XL
        </div>
        <div style="color:#8888aa; font-size:0.9rem;">
            Generate stunning images from text prompts using the SDXL model via HuggingFace Inference API.
            Add your API token in the sidebar to begin.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("**Describe the image you want to create**")

        prompt = st.text_area(
            "Prompt",
            placeholder="A majestic dragon soaring over a neon-lit cyberpunk city at sunset, ultra-detailed, cinematic lighting…",
            height=130,
            label_visibility="collapsed",
        )

        with st.expander("⚙ Advanced Options"):
            neg_prompt = st.text_area(
                "Negative prompt (what to avoid)",
                placeholder="blurry, low quality, distorted, ugly, watermark…",
                height=80,
            )
            style_preset = st.selectbox("Style enhancement", [
                "None", "Photorealistic", "Oil Painting", "Watercolor",
                "Anime", "Concept Art", "Digital Art", "Sketch",
            ])

        style_suffixes = {
            "None": "",
            "Photorealistic": ", photorealistic, 8k, RAW photo, highly detailed",
            "Oil Painting": ", oil painting, thick brushstrokes, canvas texture, art by Rembrandt",
            "Watercolor": ", watercolor illustration, soft edges, paper texture",
            "Anime": ", anime art style, vibrant colors, Studio Ghibli",
            "Concept Art": ", concept art, matte painting, ArtStation trending",
            "Digital Art": ", digital art, sharp edges, vibrant, DeviantArt",
            "Sketch": ", pencil sketch, charcoal drawing, hand-drawn",
        }

        if st.button("🪄  Generate Image", key="generate_btn", use_container_width=True):
            if not prompt.strip():
                st.warning("Please enter a prompt.")
            else:
                final_prompt = prompt + style_suffixes.get(style_preset, "")
                from utils.text_to_image import generate_image_from_text
                with st.spinner("🎨 Generating your image… (this may take 20–40 seconds)"):
                    img, err = generate_image_from_text(final_prompt)

                if err:
                    st.error(f"Generation failed: {err}")
                else:
                    st.session_state["generated_image"] = img
                    st.session_state["gen_prompt"] = prompt

        st.markdown('</div>', unsafe_allow_html=True)

        # Prompt inspiration
        st.markdown("**💡 Prompt inspiration**")
        examples = [
            "A misty Japanese forest temple at dawn, golden light, cinematic",
            "Astronaut riding a horse on Mars, photorealistic, epic scale",
            "Portrait of a cyberpunk samurai, neon rain, highly detailed",
            "Underwater city of Atlantis, bioluminescent creatures, fantasy art",
            "A cozy library in an ancient tree, warm lighting, magical realism",
        ]
        for ex in examples:
            if st.button(f"↗ {ex[:60]}…" if len(ex)>60 else f"↗ {ex}", key=f"ex_{ex[:20]}"):
                st.session_state["example_prompt"] = ex
                st.info(f"Copied to clipboard — paste into the prompt box: *{ex}*")

    with col_right:
        st.markdown('<div class="result-card" style="min-height:400px">', unsafe_allow_html=True)
        if "generated_image" in st.session_state:
            gen_img = st.session_state["generated_image"]
            st.markdown('<div class="section-label">Generated Image</div>', unsafe_allow_html=True)
            st.image(gen_img, use_container_width=True)
            st.markdown(f"<small style='color:#8888aa'>Prompt: *{st.session_state.get('gen_prompt','')}*</small>", unsafe_allow_html=True)
            st.markdown("---")
            download_widget(gen_img, "ai_generated.png", "PNG")
            c1, c2 = st.columns(2)
            with c1:
                download_widget(gen_img, "ai_generated.jpg", "JPEG")
            with c2:
                download_widget(gen_img, "ai_generated.webp", "WEBP")
        else:
            st.markdown("""
            <div style="display:flex; flex-direction:column; align-items:center; 
                        justify-content:center; height:380px; color:#8888aa; text-align:center;">
                <div style="font-size:5rem; margin-bottom:1rem; opacity:0.3">🖼</div>
                <div style="font-size:1rem; font-weight:500; color:#b0b0cc">Your generated image will appear here</div>
                <div style="font-size:0.82rem; margin-top:0.5rem">Enter a prompt and hit Generate</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#55557a; font-size:0.78rem; padding:0.5rem 0 1rem">
    ✦ PixelForge Studio · Built with Streamlit, OpenCV & HuggingFace
</div>
""", unsafe_allow_html=True)
