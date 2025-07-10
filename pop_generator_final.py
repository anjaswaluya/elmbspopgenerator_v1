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
    st.header("🖼️ Upload Gambar")
    bg_file    = st.file_uploader("Background (rasio apa pun)", type=["jpg","png","jpeg"])
    logo_files = st.file_uploader("Logo Produk (max 6)", type=["png","jpg","jpeg"], accept_multiple_files=True)

# ===== Helpers =====
def format_rp(x):
    return f"Rp{x:,.0f}".replace(",", ".")

def load_font(sz):
    try:
        return ImageFont.truetype("arial.ttf", sz)
    except:
        return ImageFont.load_default()

def center_text(draw, text, font, cx, cy, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - w//2, cy - h//2), text, font=font, fill=fill)

# ===== Main Logic =====
if bg_file:
    bg = Image.open(bg_file).convert("RGBA")
    W, H = bg.size
    draw = ImageDraw.Draw(bg)
    cx, cy = W//2, int(H * 0.45)

    # Sizing
    r        = int(W * 0.15)  # lingkaran radius
    spacing  = int(W * 0.05)
    logo_h   = int(H * 0.13)
    strike_sz= max(16, int(W * 0.02))
    promo_sz = max(32, int(W * 0.045))
    f_strike = load_font(strike_sz)
    f_promo  = load_font(promo_sz)

    y_text_produk = H - int(H * 0.08)  # default jika tak ada logo

    # ==== Render LOGO ====
    if logo_files:
        logos = logo_files[:6]
        n = len(logos)
        total_w = n * logo_h
        spacing = (W - total_w) // (n + 1)
        y0 = cy - r - logo_h - int(H * 0.025)
        for i, f in enumerate(logos):
            im = Image.open(f).convert("RGBA")
            im.thumbnail((logo_h, logo_h))
            x = spacing * (i+1) + logo_h * i
            bg.paste(im, (x, y0), im)
        y_text_produk = y0 + logo_h + int(H * 0.02)

    # ==== Render DISKON ====
    diskons = [
        {"val": f"{diskon_utama}%", "label": "DISKON", "color": "red"},
        {"val": f"+{diskon_member}%", "label": "MEMBER", "color": "blue"}
    ]
    d_spacing = r * 2 + int(W * 0.05)
    d_start_x = cx - d_spacing // 2
    for i, d in enumerate(diskons):
        dx = d_start_x + i * d_spacing
        draw.ellipse([dx - r, cy - r, dx + r, cy + r], fill=d["color"])
        f_val = load_font(int(r * 0.6))
        f_lbl = load_font(int(r * 0.25))
        center_text(draw, d["val"], f_val, dx, cy - int(r * 0.2), "white")
        center_text(draw, d["label"], f_lbl, dx, cy + int(r * 0.35), "white")

    # ==== Harga Coret ====
    base_y = cy + r + int(H * 0.03)
    t0 = format_rp(harga_awal) + f" /{satuan_harga}"
    bbox0 = draw.textbbox((0, 0), t0, font=f_strike)
    w0 = bbox0[2] - bbox0[0]
    x0 = cx - w0//2 - int(W * 0.03)
    draw.text((x0, base_y), t0, font=f_strike, fill="red")
    draw.line([(x0, base_y + strike_sz//2), (x0 + w0, base_y + strike_sz//2)], fill="red", width=2)

    # ==== Harga Promo ====
    t1 = format_rp(harga_promo) + f" /{satuan_harga}"
    center_text(draw, t1, f_promo, cx, base_y + int(promo_sz * 0.8), "black")

    # ==== Nama Produk (di bawah logo atau fallback bawah) ====
    max_width_ratio = 0.85
    max_font_size = int(W * 0.06)
    min_font_size = 12
    text = nama_produk.upper()
    for sz in range(max_font_size, min_font_size, -1):
        f = load_font(sz)
        bbox = draw.textbbox((0, 0), text, font=f)
        if bbox[2] - bbox[0] <= W * max_width_ratio:
            center_text(draw, text, f, cx, y_text_produk, "black")
            break

    # ==== Output ====
    st.image(bg, use_container_width=True)
    buf = io.BytesIO()
    bg.save(buf, format="PNG")
    st.download_button("⬇️ Download POP", buf.getvalue(), "POP_final.png", "image/png")

else:
    st.info("Upload background terlebih dahulu.")
