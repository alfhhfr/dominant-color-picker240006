import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="Dominant Color Picker",
    page_icon="🎨",
    layout="centered"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7fb;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: #222;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 40px;
        font-size: 18px;
    }

    .color-box {
        height: 120px;
        border-radius: 15px;
        margin-bottom: 10px;
        border: 2px solid white;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }

    .hex-text {
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HEADER
# =========================
st.markdown('<div class="title">🎨 Dominant Color Picker</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Upload gambar dan dapatkan 5 warna dominan otomatis</div>',
    unsafe_allow_html=True
)

# =========================
# FUNCTION RGB TO HEX
# =========================
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(rgb)

# =========================
# FUNCTION EXTRACT COLORS
# =========================
def extract_colors(image, num_colors=5):
    image = image.resize((200, 200))

    img_array = np.array(image)

    img_array = img_array.reshape((-1, 3))

    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(img_array)

    colors = kmeans.cluster_centers_.astype(int)

    return colors

# =========================
# IMAGE UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "Upload gambar",
    type=["jpg", "jpeg", "png"]
)

# =========================
# PROCESS IMAGE
# =========================
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')

    st.image(image, caption="Gambar yang diupload", use_container_width=True)

    st.markdown("## 🎯 Hasil Palet Warna")

    colors = extract_colors(image)

    cols = st.columns(5)

    for idx, color in enumerate(colors):
        hex_color = rgb_to_hex(color)

        with cols[idx]:
            st.markdown(
                f'''
                <div class="color-box" style="background-color:{hex_color};"></div>
                <div class="hex-text">{hex_color}</div>
                ''',
                unsafe_allow_html=True
            )

    st.success("Palet warna berhasil dibuat!")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "<center>Dibuat menggunakan Streamlit & Machine Learning</center>",
    unsafe_allow_html=True
)