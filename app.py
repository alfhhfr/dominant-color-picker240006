# Nama	        : Alifah Fa'izah Rufaidah
# NPM		    : 140810240006
# Kelas		    : B

import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import io
import colorsys

# Page Config 
st.set_page_config(
    page_title="PickMyColor — Color Extractor",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Global CSS 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Outfit:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #0d0d0d !important;
    color: #f0ece4 !important;
    font-family: 'Outfit', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    max-width: 780px !important;
    padding: 3rem 2rem 6rem !important;
}

.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
}

.hero-eyebrow {
    font-family: 'Outfit', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #b89a6a;
    margin-bottom: 1rem;
}

.hero h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(2.8rem, 6vw, 4.2rem) !important;
    font-weight: 700 !important;
    line-height: 1.05 !important;
    color: #f0ece4 !important;
    letter-spacing: -0.02em !important;
}

.hero h1 em { font-style: italic; color: #b89a6a; }

.hero-sub {
    margin-top: 1rem;
    font-size: 15px;
    font-weight: 300;
    color: #7a7570;
}

.hero-line {
    width: 40px;
    height: 1px;
    background: #b89a6a;
    margin: 1.8rem auto 0;
    opacity: 0.6;
}

[data-testid="stFileUploader"] > div {
    background: #111110 !important;
    border: 1px solid #2a2925 !important;
    border-radius: 16px !important;
    padding: 2.5rem !important;
}

[data-testid="stFileUploader"] > div:hover {
    border-color: #b89a6a !important;
}

[data-testid="stFileUploader"] label {
    color: #7a7570 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
}

[data-testid="stImage"] img {
    border-radius: 12px !important;
    border: 1px solid #2a2925 !important;
}

.section-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4a4845;
    margin: 2rem 0 0.9rem;
}

.strip-wrap {
    border-radius: 14px;
    overflow: hidden;
    display: flex;
    height: 88px;
    border: 1px solid #1e1e1b;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 1.2rem;
}

.strip-swatch { flex: 1; }

.swatch-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    margin-bottom: 2rem;
}

.swatch-card {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #1e1e1b;
    background: #111110;
    transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1),
                box-shadow 0.25s ease;
}

.swatch-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 16px 40px rgba(0,0,0,0.5);
}

.swatch-thumb { height: 76px; width: 100%; }

.swatch-meta { padding: 10px 11px 13px; }

.swatch-hex {
    font-family: 'Outfit', sans-serif;
    font-size: 12px;
    font-weight: 600;
    color: #c8c4bc;
    letter-spacing: 0.04em;
}

.swatch-rgb {
    font-size: 9.5px;
    color: #4a4845;
    margin-top: 3px;
}

.swatch-name {
    font-family: 'Playfair Display', serif;
    font-size: 11px;
    font-style: italic;
    color: #6a6560;
    margin-top: 4px;
}

.css-export {
    background: #0a0a09;
    border: 1px solid #1e1e1b;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    color: #6a9f5a;
    line-height: 2;
    white-space: pre;
    overflow-x: auto;
    margin-top: 0.75rem;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2925, transparent);
    margin: 2rem 0;
}

.stDownloadButton > button {
    width: 100%;
    background: #b89a6a !important;
    color: #0d0d0d !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 1.5rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

.stDownloadButton > button:hover {
    background: #cdb07a !important;
    box-shadow: 0 8px 24px rgba(184,154,106,0.3) !important;
}

[data-testid="stExpander"] {
    background: #111110 !important;
    border: 1px solid #1e1e1b !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary {
    color: #7a7570 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
}

.empty-state {
    text-align: center;
    padding: 3rem 2rem;
}

.empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.2;
    display: block;
    color: #b89a6a;
}

.empty-state p {
    font-size: 14px;
    font-style: italic;
    font-family: 'Playfair Display', serif;
    color: #f0ece4;
}

.app-footer {
    text-align: center;
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid #1a1a17;
    font-size: 15px;
    color: #7a7570;
    letter-spacing: 0.12em;
}

[data-testid="stAlert"] {
    background: #111110 !important;
    border: 1px solid #b89a6a33 !important;
    border-radius: 10px !important;
    color: #7a7570 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
}
</style>
""", unsafe_allow_html=True)


# Utilities 

def rgb_to_hex(r, g, b):
    return "#{:02X}{:02X}{:02X}".format(int(r), int(g), int(b))


def hex_to_rgb(hex_str):
    h = hex_str.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def get_luminance(r, g, b):
    return 0.299 * r + 0.587 * g + 0.114 * b


def text_on_color(hex_str):
    r, g, b = hex_to_rgb(hex_str)
    return "#0d0d0d" if get_luminance(r, g, b) > 140 else "#f0ece4"


def get_color_name(hex_str):
    r, g, b = hex_to_rgb(hex_str)
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    hue = h * 360
    sat = s * 100
    light = v * 100

    if sat < 10:
        if light < 20:  return "Onyx"
        if light < 45:  return "Graphite"
        if light < 70:  return "Silver"
        return "Ivory"

    if hue < 10 or hue >= 350: return "Rosewood" if light < 50 else "Blush"
    if hue < 20:  return "Mahogany"  if light < 50 else "Coral"
    if hue < 40:  return "Sienna"    if light < 50 else "Apricot"
    if hue < 65:  return "Ochre"     if light < 50 else "Champagne"
    if hue < 80:  return "Olive"     if light < 50 else "Citrine"
    if hue < 150: return "Emerald"   if light < 50 else "Sage"
    if hue < 175: return "Viridian"  if light < 50 else "Celadon"
    if hue < 200: return "Teal"      if light < 50 else "Aqua"
    if hue < 240: return "Cobalt"    if light < 50 else "Periwinkle"
    if hue < 265: return "Indigo"    if light < 50 else "Wisteria"
    if hue < 290: return "Amethyst"  if light < 50 else "Lavender"
    if hue < 320: return "Plum"      if light < 50 else "Lilac"
    if hue < 350: return "Carmine"   if light < 50 else "Petal"
    return "Crimson"


def extract_palette(image: Image.Image, n: int = 5) -> list:
    img = image.convert("RGB")
    img.thumbnail((150, 150), Image.LANCZOS)
    arr = np.array(img).reshape(-1, 3).astype(float)

    # filter near-black and near-white
    mask = ~(
        ((arr[:, 0] > 242) & (arr[:, 1] > 242) & (arr[:, 2] > 242)) |
        ((arr[:, 0] < 12)  & (arr[:, 1] < 12)  & (arr[:, 2] < 12))
    )
    arr = arr[mask]

    if len(arr) < n:
        return [rgb_to_hex(*p) for p in arr[:n]]

    km = KMeans(n_clusters=n, n_init=12, random_state=0)
    km.fit(arr)

    centers = sorted(km.cluster_centers_, key=lambda c: get_luminance(*c), reverse=True)
    return [rgb_to_hex(*c) for c in centers]


def make_palette_image(colors: list, w=500, h=100) -> bytes:
    img = Image.new("RGB", (w, h))
    sw = w // len(colors)
    for i, hex_c in enumerate(colors):
        r, g, b = hex_to_rgb(hex_c)
        for x in range(i * sw, min((i + 1) * sw, w)):
            for y in range(h):
                img.putpixel((x, y), (r, g, b))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# UI 
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Dominant Color Picker </div>
    <h1>Pick<em>MyColor</em></h1>
    <p class="hero-sub">Upload an image. Discover its soul — five colors at a time.</p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg", "webp", "bmp"],
    label_visibility="collapsed",
)

if uploaded:
    image = Image.open(uploaded)

    st.markdown('<div class="section-label">Your image</div>', unsafe_allow_html=True)
    st.image(image, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    with st.spinner("Analysing colour composition..."):
        colors = extract_palette(image, 5)

    # color strip
    st.markdown('<div class="section-label">Dominant palette</div>', unsafe_allow_html=True)
    strip = '<div class="strip-wrap">' + "".join(
        f'<div class="strip-swatch" style="background:{c}" title="{c}"></div>'
        for c in colors
    ) + '</div>'
    st.markdown(strip, unsafe_allow_html=True)

    # swatch cards
    cards = '<div class="swatch-grid">'
    for hex_c in colors:
        r, g, b = hex_to_rgb(hex_c)
        name = get_color_name(hex_c)
        fg = text_on_color(hex_c)
        cards += f"""
        <div class="swatch-card">
            <div class="swatch-thumb" style="background:{hex_c};
                 display:flex;align-items:flex-end;padding:8px;">
                <span style="font-size:9px;font-weight:600;color:{fg};
                      opacity:0.55;letter-spacing:0.05em;font-family:Outfit,sans-serif;">
                    {hex_c}
                </span>
            </div>
            <div class="swatch-meta">
                <div class="swatch-hex">{hex_c}</div>
                <div class="swatch-rgb">rgb({r}, {g}, {b})</div>
                <div class="swatch-name">{name}</div>
            </div>
        </div>"""
    cards += '</div>'
    st.markdown(cards, unsafe_allow_html=True)

    st.info("✦  Hover over the swatches to see each color. Copy the HEX codes above for use in your projects.")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # CSS Export
    with st.expander("✦  Export as CSS Variables"):
        css_lines = "\n".join(f"  --palette-{i+1}: {c};" for i, c in enumerate(colors))
        css_block = f":root {{\n{css_lines}\n}}"
        st.markdown(f'<div class="css-export">{css_block}</div>', unsafe_allow_html=True)
        st.code(css_block, language="css")

    # download
    st.markdown('<div class="section-label" style="margin-top:2rem">Export palette</div>', unsafe_allow_html=True)
    st.download_button(
        label="⬇  Download palette image (.png)",
        data=make_palette_image(colors),
        file_name="your_palette.png",
        mime="image/png",
    )

else:
    st.markdown("""
    <div class="empty-state">
        <span class="empty-icon">◈</span>
        <p>No image yet — upload one above to begin.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="app-footer">
    ALIFAH FAIZAH RUFAIDAH &nbsp;·&nbsp; 140810240006  &nbsp;·&nbsp; B
</div>
""", unsafe_allow_html=True)
