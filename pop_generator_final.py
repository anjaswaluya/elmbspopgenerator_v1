import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Page config
st.set_page_config(page_title="ELMBS POP Generator", layout="centered")

# ===== Sidebar Inputs =====
with st.sidebar:
    st.header("🛠️ Data Produk")
    nama_produk   = st.text_input("Nama Produk", "GRANIT POLISHED 80X160")
    harga_awal    = st.number_input("Harga Awal", min_value=0, value=269141)
    harga_promo   = st.number_input("Harga Promo", min_value=0, value=248013)
    satuan_harga  = st.text_input("Satuan (ex: m, pcs)", value="m")
    diskon_utama  = st.number_input("Diskon Utama (%)", min_value=0, value=5)
    diskon_member = st.number_input("Diskon Member (%)", min_value=0, value=3)

    st.markdown("---")
    st.header("🖼️ Upload Gambar")
    bg_file    = st.file_uploader("Background (rasio apa pun)", type=["jpg","jpeg","png"])
    logo_files = st.file_uploader("Logo Produk (max 6)", type=["png","jpg","jpeg"], accept_multiple_files=True)

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

# ===== Main Preview =====
if bg_file:
    # 1) Load background & canvas
    bg = Image.open(bg_file).convert("RGBA")
    W, H = bg.size
    draw = ImageDraw.Draw(bg)
    cx, cy = W//2, int(H * 0.45)

    # 2) Dynamic sizing based on W
    # Radius = 20% of width
    r = int(W * 0.20)
    # Font sizes proportional to radius
    num_sz = max(20, int(r * 0.6))
    lbl_sz = max(10, int(r * 0.2))
    strike_sz = max(12, int(num_sz * 0.3))
    promo_sz = max(num_sz, int(r * 0.8))
    prod_sz  = max(30, int(r * 0.4))

    f_num    = load_font(num_sz)
    f_lbl    = load_font(lbl_sz)
    f_strike = load_font(strike_sz)
    f_promo  = load_font(promo_sz)
    f_prod   = load_font(prod_sz)

    # 3) Logos: auto arrange at top of circle
    if logo_files:
        logos = logo_files[:6]
        n = len(logos)
        # Logo height = 15% of H
        logo_h = int(H * 0.15)
        gap = int((W - 2*logo_h) / max(n,1) * 0.2)
        total_w = logo_h * n + gap * (n - 1)
        start_x = (W - total_w) // 2
        y0 = cy - r - logo_h - int(H*0.02)
        for i, f in enumerate(logos):
            im = Image.open(f).convert("RGBA")
            im.thumbnail((logo_h, logo_h))
            x0 = start_x + i * (logo_h + gap)
            if n == 1:
                x0 = cx - im.width//2
            bg.paste(im, (x0, y0), im)

    # 4) Draw discount circles + texts
    for dx, color, val, lbl in [
        (-r - int(W*0.02), "red",    f"{diskon_utama}%", "DISKON"),
        ( r + int(W*0.02), "blue", f"+{diskon_member}%", "MEMBER")
    ]:
        x0 = cx + dx
        draw.ellipse([x0 - r, cy - r, x0 + r, cy + r], fill=color)
        center_text(draw, val, f_num, x0, cy - int(num_sz*0.3), "white")
        center_text(draw, lbl, f_lbl, x0, cy + int(r*0.6), "white")

    # 5) Harga awal tercoret (kecil, merah, agak ke kiri)
    base_y = cy + r + int(H*0.02)
    t0 = format_rp(harga_awal) + f" /{satuan_harga}"
    bbox0 = draw.textbbox((0,0), t0, font=f_strike)
    w0 = bbox0[2] - bbox0[0]
    x0 = cx - w0//2 - int(r*0.3)
    draw.text((x0, base_y), t0, font=f_strike, fill="red")
    draw.line([(x0, base_y + int(strike_sz*0.3)), (x0 + w0, base_y + int(strike_sz*0.3))],
              fill="red", width=max(2, strike_sz//10))

    # 6) Harga promo besar di bawah
    t1 = format_rp(harga_promo) + f" /{satuan_harga}"
    center_text(draw, t1, f_promo, cx, base_y + int(promo_sz*0.6), "black")

    # 7) Nama produk di bawah lingkaran
    center_text(draw, nama_produk, f_prod, cx, H - int(H*0.1), "black")

    # 8) Preview & Download
    st.image(bg, use_container_width=True)  # langsung full lebar kolom
    buf = io.BytesIO(); bg.save(buf, "PNG")
    st.download_button("⬇️ Download POP", buf.getvalue(), "POP_final.png", "image/png")

else:
    st.info("Upload background apa pun di sidebar untuk preview real‑time.")
