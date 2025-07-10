import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="POP Generator Optimal", layout="wide")

st.title("🎨 POP Generator Optimal")
st.markdown("Buat desain brosur promo yang fun, simpel, dan powerful!")

st.subheader("📤 Upload Gambar")

col1, col2 = st.columns(2)

with col1:
    bg_file = st.file_uploader("Upload Background (rasio A4)", type=["jpg", "jpeg", "png"])
with col2:
    logo_files = st.file_uploader("Upload Logo Produk (maksimal 6 file)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

st.subheader("📝 Input Judul POP")
judul = st.text_input("Judul Produk:", "TRISENSA CERAMICS 80X80")
judul_font_size = st.slider("Ukuran Font Judul", 10, 150, 50)

# Font default bawaan sistem
try:
    font_judul = ImageFont.truetype("arial.ttf", judul_font_size)
except:
    font_judul = ImageFont.load_default()

# Proses Gambar Jika Sudah Upload
if bg_file and logo_files:
    bg_image = Image.open(bg_file).convert("RGBA")
    bg_width, bg_height = bg_image.size
    draw = ImageDraw.Draw(bg_image)

    # Gambar Judul di Tengah
    if hasattr(draw, "textbbox"):  # PIL >= 8.0
        bbox = draw.textbbox((0, 0), judul, font=font_judul)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    else:  # fallback
        text_w, text_h = draw.textsize(judul, font=font_judul)

    text_x = (bg_width - text_w) // 2
    text_y = int(bg_height * 0.22)  # bawah logo
    draw.text((text_x, text_y), judul, fill="black", font=font_judul)

    # Gambar logo produk sejajar
    max_logo = min(6, len(logo_files))
    spacing = 20
    total_logo_width = int(bg_width * 0.6)
    logo_area_width = total_logo_width - (spacing * (max_logo - 1))
    logo_width = logo_area_width // max_logo
    logo_y = int(bg_height * 0.12)

    start_x = (bg_width - total_logo_width) // 2

    for i, logo_file in enumerate(logo_files[:6]):
        logo = Image.open(logo_file).convert("RGBA")
        aspect_ratio = logo.width / logo.height
        resized_logo = logo.resize((logo_width, int(logo_width / aspect_ratio)))
        logo_x = start_x + i * (logo_width + spacing)
        bg_image.paste(resized_logo, (logo_x, logo_y), resized_logo)

    # PREVIEW dan Download
    st.subheader("🖼️ Preview")
    st.image(bg_image, caption="Preview POP", use_column_width=True)

    buffer = io.BytesIO()
    bg_image.save(buffer, format="PNG")
    st.download_button("⬇️ Download POP", data=buffer.getvalue(), file_name="POP.png", mime="image/png")

else:
    st.info("Silakan upload background dan minimal 1 logo produk terlebih dahulu.")
