import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="POP Generator by ElMBS", layout="wide")

# Sidebar kiri: Upload dan Input
with st.sidebar:
    st.header("🎨 POP Generator by ElMBS")

    st.markdown("🖼️ **Gaskeun input background POP-nya abangku!! 🔥🔥**")
    bg_file = st.file_uploader("Upload Background (rasio A4)", type=["jpg", "jpeg", "png"])

    st.markdown("📌 **Cusss upload logonyaaa! Maksimal 6 ya, jangan barbar 😆**")
    logo_files = st.file_uploader("Upload Logo Produk", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    st.markdown("---")
    st.markdown("✍️ **Tulis nama produknya... yang jualan kamu, yang laku kita 🤝**")
    judul = st.text_input("Judul Produk", "TRISENSA CERAMICS 80X80")
    judul_font_size = st.slider("🔠 Geser fontnya biar judulnya makin cihuy! 😍", 10, 100, 42)

    st.markdown("---")
    st.markdown("💰 **Masukin harga asli... tenang, nanti kita coret 😎**")
    harga_normal = st.number_input("Harga Normal", value=269141)

    st.markdown("🔥 **Harga promo paling nendang? Masukin sini brooo 💸**")
    harga_promo = st.number_input("Harga Promo", value=248013)

    st.markdown("📏 **/m, /pcs, /dus, bebas bang... asal jangan /mantan 😅**")
    satuan = st.text_input("Satuan", value="m")

# Font default
try:
    font_judul = ImageFont.truetype("arial.ttf", judul_font_size)
    font_harga = ImageFont.truetype("arial.ttf", 36)
    font_promo = ImageFont.truetype("arial.ttf", 60)
except:
    font_judul = ImageFont.load_default()
    font_harga = ImageFont.load_default()
    font_promo = ImageFont.load_default()

# Halaman utama (preview)
st.title("📦 Preview Desain POP Abangkuu!")

if bg_file and logo_files:
    bg_image = Image.open(bg_file).convert("RGBA")
    bg_width, bg_height = bg_image.size
    draw = ImageDraw.Draw(bg_image)

    # Logo Produk
    max_logo = min(6, len(logo_files))
    spacing = 20
    total_logo_width = int(bg_width * 0.6)
    logo_area_width = total_logo_width - (spacing * (max_logo - 1))
    logo_width = logo_area_width // max_logo
    logo_y = int(bg_height * 0.08)
    start_x = (bg_width - total_logo_width) // 2

    for i, logo_file in enumerate(logo_files[:6]):
        logo = Image.open(logo_file).convert("RGBA")
        aspect_ratio = logo.width / logo.height
        resized_logo = logo.resize((logo_width, int(logo_width / aspect_ratio)))
        logo_x = start_x + i * (logo_width + spacing)
        bg_image.paste(resized_logo, (logo_x, logo_y), resized_logo)

    # Judul Produk
    if hasattr(draw, "textbbox"):
        bbox = draw.textbbox((0, 0), judul, font=font_judul)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    else:
        text_w, text_h = draw.textsize(judul, font=font_judul)

    text_x = (bg_width - text_w) // 2
    text_y = logo_y + int(logo_width / 1.6) + 25
    draw.text((text_x, text_y), judul, fill="black", font=font_judul)

    # Harga Normal (Coret)
    harga_text = f"Rp {harga_normal:,.0f}".replace(",", ".") + f"/{satuan}"
    harga_w, harga_h = draw.textsize(harga_text, font=font_harga)
    harga_x = int(bg_width * 0.3)
    harga_y = text_y + 100
    draw.text((harga_x, harga_y), harga_text, fill="red", font=font_harga)
    draw.line((harga_x, harga_y + harga_h // 2, harga_x + harga_w, harga_y + harga_h // 2), fill="red", width=3)

    # Harga Promo
    promo_text = f"Rp {harga_promo:,.0f}".replace(",", ".") + f"/{satuan}"
    promo_w, promo_h = draw.textsize(promo_text, font=font_promo)
    promo_x = int(bg_width * 0.3)
    promo_y = harga_y + harga_h + 30
    draw.text((promo_x, promo_y), promo_text, fill="red", font=font_promo)

    # Preview dan Download
    st.image(bg_image, caption="🔥 Preview POP kamu siap download!")

    buffer = io.BytesIO()
    bg_image.save(buffer, format="PNG")
    st.download_button("⬇️ Download POP", data=buffer.getvalue(), file_name="POP_final.png", mime="image/png")

else:
    st.warning("📢 Upload background dan minimal 1 logo dulu ya abangku!")
