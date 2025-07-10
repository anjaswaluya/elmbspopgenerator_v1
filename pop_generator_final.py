import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Page setup
st.set_page_config(page_title="POP Generator by ElMBS", layout="wide")
st.title("🎯 POP Generator Final Fix")

# Sidebar: Uploads and Inputs
with st.sidebar:
    st.header("🎨 Settings")
    st.markdown("🖼️ **Gaskeun bg-nya!**")
    bg_file = st.file_uploader("Upload Background (rasio A4)", type=["jpg", "jpeg", "png"])

    st.markdown("📌 **Cusss upload logonyaaa! Maksimal 6 ya, jangan barbar 😆**")
    logos = st.file_uploader("Upload Logo Produk", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    st.markdown("---")
    st.markdown("✍️ **Tulis nama produknya... yang jualan kamu, yang laku kita 🤝**")
    title = st.text_input("Judul Produk", "TRISENSA CERAMICS 80X80")
    title_size = st.slider("🔠 Ukuran Font Judul", 10, 120, 50)

    st.markdown("---")
    st.markdown("💰 **Masukin harga asli... tenang, nanti kita coret 😎**")
    price_old = st.number_input("Harga Normal", value=269141)

    st.markdown("🔥 **Harga promo paling nendang? Masukin sini brooo 💸**")
    price_new = st.number_input("Harga Promo", value=248013)

    st.markdown("📏 **/m, /pcs, /dus, bebas bang... asal jangan /mantan 😅**")
    unit = st.text_input("Satuan (ex: m, pcs)", "m")

# Helper: load font
def load_font(sz, bold=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", sz)
    except:
        return ImageFont.load_default()

# Main execution
if bg_file and logos:
    bg = Image.open(bg_file).convert("RGBA")
    W, H = bg.size
    draw = ImageDraw.Draw(bg)

    # Logo Produk Area
    logo_h = int(H * 0.15)
    n = min(len(logos), 6)
    gap = int((W - n * logo_h) / (n + 1))
    y0 = int(H * 0.1)

    for i, f in enumerate(logos[:6]):
        im = Image.open(f).convert("RGBA")
        ar = im.width / im.height
        w0 = int(logo_h * ar)
        im = im.resize((w0, logo_h), resample=Image.Resampling.LANCZOS)
        x0 = gap * (i + 1) + sum(int(logo_h * (logos[j].width / logos[j].height)) for j in range(i))
        bg.paste(im, (x0, y0), im)

    # Judul Produk
    font_title = load_font(title_size, bold=True)
    tw, th = draw.textsize(title, font=font_title)
    x_t = (W - tw) // 2
    y_t = y0 + logo_h + int(H * 0.02)
    draw.text((x_t, y_t), title, fill="black", font=font_title)

    # Harga Coret
    font_old = load_font(int(W * 0.02))
    old_txt = f"Rp {price_old:,.0f}".replace(",", ".") + f"/{unit}"
    ow, oh = draw.textsize(old_txt, font=font_old)
    x_o = int(W * 0.30)
    y_o = y_t + th + int(H * 0.04)
    draw.text((x_o, y_o), old_txt, fill="red", font=font_old)
    draw.line((x_o, y_o + oh // 2, x_o + ow, y_o + oh // 2), fill="red", width=2)

    # Harga Promo
    font_new = load_font(int(W * 0.04), bold=True)
    new_txt = f"Rp {price_new:,.0f}".replace(",", ".") + f"/{unit}"
    nw, nh = draw.textsize(new_txt, font=font_new)
    x_n = x_o
    y_n = y_o + oh + int(H * 0.02)
    draw.text((x_n, y_n), new_txt, fill="red", font=font_new)

    # Display & Download
    st.image(bg, use_column_width=True)
    buf = io.BytesIO()
    bg.save(buf, format="PNG")
    st.download_button("⬇️ Download POP", buf.getvalue(), "POP_final.png", "image/png")
else:
    st.info("Upload background + minimal 1 logo dulu ya abangku!")
