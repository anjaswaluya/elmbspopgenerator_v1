import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Setup
st.set_page_config(page_title="POP Generator by ElMBS", layout="wide")
st.title("🎯 POP Generator aLA ALA V1")

# Sidebar UI
with st.sidebar:
    st.header("🎨 Settings")
    st.markdown("🖼️ **Gaskeun bg-nya!**")
    bg_file = st.file_uploader("Upload Background (rasio A4)", type=["jpg", "jpeg", "png"])

    st.markdown("📌 **Cusss upload logonyaaa! Maksimal 6 ya, jangan barbar 😆**")
    logos = st.file_uploader("Upload Logo Produk", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    st.markdown("✍️ **Tulis nama produknya... yang jualan kamu, yang laku kita 🤝**")
    title = st.text_input("Judul Produk", "TRISENSA CERAMICS 80X80")
    title_size = st.slider("🔠 Ukuran Font Judul", 10, 120, 50)

    st.markdown("💰 **Masukin harga asli... tenang, nanti kita coret 😎**")
    price_old = st.number_input("Harga Normal", value=269141)

    st.markdown("🔥 **Harga promo paling nendang? Masukin sini brooo 💸**")
    price_new = st.number_input("Harga Promo", value=248013)

    st.markdown("📏 **/m, /pcs, /dus, bebas bang... asal jangan /mantan 😅**")
    unit = st.text_input("Satuan (ex: m, pcs)", "m")

# Helper font loader
def load_font(sz, bold=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", sz)
    except:
        return ImageFont.load_default()

# Helper text center
def center_text(draw, text, font, center_x, y, fill="black"):
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    draw.text((center_x - w // 2, y), text, font=font, fill=fill)

# Start render
if bg_file and logos:
    bg = Image.open(bg_file).convert("RGBA")
    W, H = bg.size
    draw = ImageDraw.Draw(bg)

    # Logo
    logo_h = int(H * 0.15)
    n = min(len(logos), 6)
    gap = int((W - n * logo_h) / (n + 1))
    y0 = int(H * 0.1)
    x_cursor = gap
    for i, f in enumerate(logos[:6]):
        im = Image.open(f).convert("RGBA")
        ar = im.width / im.height
        w0 = int(logo_h * ar)
        im = im.resize((w0, logo_h), resample=Image.Resampling.LANCZOS)
        bg.paste(im, (x_cursor, y0), im)
        x_cursor += w0 + gap

    # Judul
    font_title = load_font(title_size, bold=True)
    y_title = y0 + logo_h + int(H * 0.02)
    center_text(draw, title, font_title, W // 2, y_title)

    # Harga Coret
    font_old = load_font(int(W * 0.02))
    old_txt = f"Rp {price_old:,.0f}".replace(",", ".") + f"/{unit}"
    bbox_old = font_old.getbbox(old_txt)
    ow = bbox_old[2] - bbox_old[0]
    oh = bbox_old[3] - bbox_old[1]
    x_old = int(W * 0.30)
    y_old = y_title + int(H * 0.08)
    draw.text((x_old, y_old), old_txt, fill="red", font=font_old)
    draw.line((x_old, y_old + oh // 2, x_old + ow, y_old + oh // 2), fill="red", width=2)

    # Harga Promo
    font_new = load_font(int(W * 0.04), bold=True)
    new_txt = f"Rp {price_new:,.0f}".replace(",", ".") + f"/{unit}"
    draw.text((x_old, y_old + oh + int(H * 0.02)), new_txt, fill="red", font=font_new)

    # Output
    st.image(bg, width=400)  # ✅ FIXED: Preview kecil biar gak ngegas satu layar
    buf = io.BytesIO()
    bg.save(buf, format="PNG")
    st.download_button("⬇️ Download POP", buf.getvalue(), "POP_final.png", "image/png")

else:
    st.info("Upload background + minimal 1 logo dulu ya abangku!")
