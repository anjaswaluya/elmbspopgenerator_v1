import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Page config
st.set_page_config(page_title="POP Generator by ElMBS", layout="wide")
st.title("🎯 POP Generator Final Fix")

# Sidebar: upload + input
with st.sidebar:
    st.header("🎨 Settings")
    st.markdown("🖼️ **Gaskeun bg-nya!**")
    bg_file = st.file_uploader("Upload Background (rasio A4)", type=["jpg","jpeg","png"])
    st.markdown("📌 **Logo Produk (max 6)**")
    logos = st.file_uploader("Upload Logo", type=["jpg","jpeg","png"], accept_multiple_files=True)
    st.markdown("---")
    st.markdown("✍️ **Isi Judul POP**")
    title = st.text_input("Judul Produk", "TRISENSA CERAMICS 80X80")
    title_size = st.slider("Ukuran Font Judul", 10, 120, 50)
    st.markdown("---")
    st.markdown("💰 **Harga Coret**")
    price_old = st.number_input("Harga Normal", value=269141)
    st.markdown("🔥 **Harga Fix**")
    price_new = st.number_input("Harga Promo", value=248013)
    unit = st.text_input("Satuan (ex: m, pcs)", "m")

# load fonts
def load_font(sz, bold=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", sz)
    except:
        return ImageFont.load_default()

# draw if both bg and at least one logo
if bg_file and logos:
    bg = Image.open(bg_file).convert("RGBA")
    W, H = bg.size
    draw = ImageDraw.Draw(bg)

    # --- Logo Produk (diperkecil ke 40% width total) ---
    max_n = min(6, len(logos))
    total_w = int(W * 0.4)
    gap = int(W * 0.02)
    single = (total_w - gap*(max_n-1)) // max_n
    start = (W - total_w)//2
    y0 = int(H * 0.08)

    for i, f in enumerate(logos[:6]):
        im = Image.open(f).convert("RGBA")
        h0 = single
        w0 = int(im.width/im.height * h0)
        im = im.resize((w0, h0), resample=Image.Resampling.LANCZOS)
        x0 = start + i*(single+gap)
        bg.paste(im, (x0, y0), im)

    # --- Judul di bawah logo ---
    font_title = load_font(title_size, bold=True)
    if hasattr(draw, "textbbox"):
        b = draw.textbbox((0,0), title, font=font_title)
        tw, th = b[2]-b[0], b[3]-b[1]
    else:
        tw, th = draw.textsize(title, font=font_title)
    x_t = (W-tw)//2
    y_t = y0 + single + int(H*0.02)
    draw.text((x_t, y_t), title, fill="black", font=font_title)

    # --- Harga Coret (kecil & merah) ---
    font_old = load_font(int(W*0.02))
    old_txt = f"Rp {price_old:,.0f}".replace(",",".") + f"/{unit}"
    if hasattr(draw, "textbbox"):
        b2 = draw.textbbox((0,0), old_txt, font=font_old)
        ow, oh = b2[2]-b2[0], b2[3]-b2[1]
    else:
        ow, oh = draw.textsize(old_txt, font=font_old)
    x_o = int(W*0.25)
    y_o = y_t + th + int(H*0.03)
    draw.text((x_o, y_o), old_txt, fill="red", font=font_old)
    draw.line((x_o, y_o+oh//2, x_o+ow, y_o+oh//2), fill="red", width=2)

    # --- Harga Fix (besar & bold) ---
    font_new = load_font(int(W*0.04), bold=True)
    new_txt = f"Rp {price_new:,.0f}".replace(",",".") + f"/{unit}"
    if hasattr(draw, "textbbox"):
        b3 = draw.textbbox((0,0), new_txt, font=font_new)
        nw, nh = b3[2]-b3[0], b3[3]-b3[1]
    else:
        nw, nh = draw.textsize(new_txt, font=font_new)
    x_n = x_o
    y_n = y_o + oh + int(H*0.02)
    draw.text((x_n, y_n), new_txt, fill="red", font=font_new)

    # --- Preview & Download ---
    st.image(bg, use_column_width=True)
    buf = io.BytesIO(); bg.save(buf, format="PNG")
    st.download_button("⬇️ Download POP", buf.getvalue(), "POP_final.png", "image/png")

else:
    st.info("Upload background + minimal 1 logo dulu, baru kita gaskeun!")
