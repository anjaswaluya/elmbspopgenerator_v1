import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="ELMBS POP Generator", layout="centered")

# ===== Sidebar =====
with st.sidebar:
    st.header("🛠️ Data Produk")
    nama_produk   = st.text_input("Nama Produk", "GRANIT POLISHED 80X160")
    harga_awal    = st.number_input("Harga Awal", min_value=0, value=269141)
    harga_promo   = st.number_input("Harga Promo", min_value=0, value=248013)
    satuan_harga  = st.text_input("Satuan (ex: m, pcs)", value="m")
    diskon_utama  = st.number_input("Diskon Utama (%)", min_value=0, value=5)
    diskon_member = st.number_input("Diskon Member (%)", min_value=0, value=3)
    st.markdown("---")
    st.header("⚙️ Pengaturan Real‑Time")
    circle_size   = st.slider("Ukuran Lingkaran", 50, 200, 120)
    font_size_num = st.slider("Ukuran Font Angka", 20, 120, 80)
    font_size_lbl = st.slider("Ukuran Font Label", 10, 60, 30)
    st.markdown("---")
    st.header("🖼️ Upload Gambar")
    bg_file     = st.file_uploader("Background (A4)", type=["jpg","jpeg","png"])
    logo_files  = st.file_uploader("Logo Produk (max 6)", type=["png","jpg","jpeg"], accept_multiple_files=True)

# ===== Helpers =====
def format_rp(x):
    return f"Rp{x:,.0f}".replace(",", ".")

def load_font(sz):
    try:
        return ImageFont.truetype("arial.ttf", sz)
    except:
        return ImageFont.load_default()

def center_text(draw, text, font, cx, y, fill="black"):
    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((cx - w//2, y), text, font=font, fill=fill)

# ===== Rendering Preview =====
if bg_file:
    # Load background
    bg = Image.open(bg_file).convert("RGBA")
    W,H = bg.size
    draw = ImageDraw.Draw(bg)
    cx = W//2

    # Logos
    if logo_files:
        logos = logo_files[:6]
        n = len(logos)
        lw, pad = 120, 40
        total_w = lw*n + pad*(n-1)
        start_x = (W - total_w)//2
        y0 = 40
        for i, f in enumerate(logos):
            im = Image.open(f).convert("RGBA")
            im.thumbnail((lw,lw))
            x0 = start_x + i*(lw+pad)
            if n==1: x0 = cx - lw//2
            bg.paste(im, (x0,y0), im)

    # Diskon circles
    f_num = load_font(font_size_num)
    f_lbl = load_font(font_size_lbl)
    cy = int(H*0.45)
    r  = circle_size
    for dx, color, txt, lbl in [(-r-20,"red",f"{diskon_utama}%", "DISKON"),
                                ( r+20,"blue",f"+{diskon_member}%","MEMBER")]:
        draw.ellipse([cx+dx-r, cy-r, cx+dx+r, cy+r], fill=color)
        center_text(draw, txt, f_num, cx+dx, cy-20, "white")
        bbox = draw.textbbox((0,0), lbl, font=f_lbl)
        h_lbl = bbox[3]-bbox[1]
        center_text(draw, lbl, f_lbl, cx+dx, cy+r-h_lbl-5, "white")

    # Harga awal (coret) & Harga promo
    f_strike = load_font(30)
    f_promo  = load_font(100)
    base_y   = cy + r + 40

    txt0 = format_rp(harga_awal) + f" /{satuan_harga}"
    bbox0 = draw.textbbox((0,0), txt0, font=f_strike)
    w0 = bbox0[2]-bbox0[0]
    x0 = cx - w0//2 - 100
    draw.text((x0, base_y), txt0, font=f_strike, fill="red")
    draw.line([(x0, base_y+20),(x0+w0, base_y+20)], fill="red", width=3)

    txt1 = format_rp(harga_promo) + f" /{satuan_harga}"
    center_text(draw, txt1, f_promo, cx, base_y+60, "black")

    # Nama produk di bawah
    f_prod = load_font(50)
    center_text(draw, nama_produk, f_prod, cx, H-150, "black")

    # Show & Download
    st.image(bg, use_column_width=True)
    buf = io.BytesIO(); bg.save(buf,"PNG")
    st.download_button("⬇️ Download POP", buf.getvalue(), "POP_final.png", "image/png")

else:
    st.info("Upload background di sidebar untuk preview real‑time")
