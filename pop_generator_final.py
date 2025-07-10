import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Page config
st.set_page_config(page_title="ELMBS POP Generator", layout="centered")

# ===== Sidebar Inputs =====
with st.sidebar:
    st.header("🛠️ Data Produk")
    nama_produk    = st.text_input("Nama Produk", "GRANIT POLISHED 80X160")
    harga_awal     = st.number_input("Harga Awal", min_value=0, value=269141)
    harga_promo    = st.number_input("Harga Promo", min_value=0, value=248013)
    satuan_harga   = st.text_input("Satuan (ex: m, pcs)", value="m")
    diskon_utama   = st.number_input("Diskon Utama (%)", min_value=0, value=5)
    diskon_member  = st.number_input("Diskon Member (%)", min_value=0, value=3)
    st.markdown("---")
    st.header("⚙️ Pengaturan Tampilan")
    circle_size    = st.slider("Ukuran Lingkaran Diskon", 50, 200, 120)
    font_size_num  = st.slider("Ukuran Font Angka Diskon", 20, 120, 80)
    font_size_lbl  = st.slider("Ukuran Font Label Diskon", 10, 60, 30)
    st.markdown("---")
    st.header("🖼️ Upload Gambar")
    bg_file        = st.file_uploader("Upload Background (rasio A4)", type=["jpg","jpeg","png"])
    logo_files     = st.file_uploader("Upload Logo Produk (max 6)", type=["png","jpg","jpeg"], accept_multiple_files=True)
    generate       = st.button("🎯 Generate POP")

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
    x = cx - w // 2
    draw.text((x, y), text, font=font, fill=fill)

# ===== Main Rendering =====
if generate and bg_file:
    # Load background
    bg = Image.open(bg_file).convert("RGBA")
    W, H = bg.size
    draw = ImageDraw.Draw(bg)
    cx = W // 2

    # -- Logos --
    if logo_files:
        logos = logo_files[:6]
        n = len(logos)
        logo_w = 120
        padding = 40
        total_width = logo_w * n + padding * (n - 1)
        start_x = (W - total_width) // 2
        y0 = 40
        for i, f in enumerate(logos):
            img = Image.open(f).convert("RGBA")
            img.thumbnail((logo_w, logo_w))
            x0 = start_x + i * (logo_w + padding)
            if n == 1:
                x0 = cx - logo_w // 2
            bg.paste(img, (x0, y0), img)

    # -- Discount Circles --
    f_num = load_font(font_size_num)
    f_lbl = load_font(font_size_lbl)
    cy = int(H * 0.45)
    r  = circle_size
    dx = -r - 20
    dx2= r + 20

    # Diskon Utama
    draw.ellipse([cx+dx-r, cy-r, cx+dx+r, cy+r], fill="red")
    center_text(draw, f"{diskon_utama}%", f_num, cx+dx, cy-20, "white")
    center_text(draw, "DISKON", f_lbl, cx+dx, cy+r - f_lbl.getsize("DISKON")[1] - 5, "white")

    # Diskon Member
    draw.ellipse([cx+dx2-r, cy-r, cx+dx2+r, cy+r], fill="blue")
    center_text(draw, f"+{diskon_member}%", f_num, cx+dx2, cy-20, "white")
    center_text(draw, "MEMBER", f_lbl, cx+dx2, cy+r - f_lbl.getsize("MEMBER")[1] - 5, "white")

    # -- Prices --
    f_strike = load_font(30)
    f_promo  = load_font(100)
    ypos = cy + r + 40

    # Harga Awal tercoret
    txt0 = format_rp(harga_awal) + f" /{satuan_harga}"
    bbox0 = draw.textbbox((0,0), txt0, font=f_strike)
    w0 = bbox0[2] - bbox0[0]
    x0 = cx - w0 // 2 - 100
    draw.text((x0, ypos), txt0, font=f_strike, fill="red")
    draw.line([(x0, ypos + 20), (x0 + w0, ypos + 20)], fill="red", width=3)

    # Harga Promo besar
    txt1 = format_rp(harga_promo) + f" /{satuan_harga}"
    center_text(draw, txt1, f_promo, cx, ypos + 60, "black")

    # -- Product Name --
    f_prod = load_font(50)
    center_text(draw, nama_produk, f_prod, cx, H - 150, "black")

    # -- Preview & Download --
    st.image(bg, use_column_width=True)
    buf = io.BytesIO()
    bg.save(buf, "PNG")
    st.download_button("⬇️ Download POP", buf.getvalue(), "POP_final.png", "image/png")

else:
    st.info("Upload background, masukkan data, lalu klik Generate POP")
