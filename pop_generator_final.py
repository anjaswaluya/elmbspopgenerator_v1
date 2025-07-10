import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# — Page config —
st.set_page_config(page_title="ELMBS POP Generator", layout="centered")

# — Sidebar: semua input & slider real‑time —
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
    circle_size    = st.slider("Ukuran Lingkaran Diskon", 50, 300, 150)
    font_size_num  = st.slider("Ukuran Font Angka Diskon", 20, 150, 100)
    font_size_lbl  = st.slider("Ukuran Font Label Diskon", 10, 80, 40)

    st.markdown("---")
    st.header("🖼️ Upload Gambar")
    bg_file    = st.file_uploader("Background (rasio A4)", type=["jpg","jpeg","png"])
    logo_files = st.file_uploader("Logo Produk (max 6)", type=["png","jpg","jpeg"], accept_multiple_files=True)

# — Helpers —
def format_rp(x):
    return f"Rp{x:,.0f}".replace(",", ".")

def load_font(sz):
    try:
        return ImageFont.truetype("arial.ttf", sz)
    except:
        return ImageFont.load_default()

def draw_centered(draw, text, font, cx, y, fill):
    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((cx - w//2, y), text, font=font, fill=fill)

# — Main preview: rerun setiap input berubah —
if bg_file:
    bg = Image.open(bg_file).convert("RGBA")
    W,H = bg.size
    draw = ImageDraw.Draw(bg)
    cx = W//2

    # 1) LETAKKAN LOGO di ATAS LINGKARAN
    top_logo_y = int(H*0.10)
    if logo_files:
        logos = logo_files[:6]
        n = len(logos)
        size_logo = int(circle_size * 0.6)
        total_w = size_logo*n + (n-1)*20
        start_x = (W-total_w)//2
        for i,f in enumerate(logos):
            im = Image.open(f).convert("RGBA")
            im.thumbnail((size_logo,size_logo))
            x = start_x + i*(size_logo+20)
            if n==1: x = cx - size_logo//2
            bg.paste(im, (x, top_logo_y), im)

    # 2) GAMBAR LINGKARAN & TEKS DISKON SAMBUNGAN
    f_num = load_font(font_size_num)
    f_lbl = load_font(font_size_lbl)
    cy = int(H*0.40)
    r  = circle_size

    # a) Diskon Utama
    left_center = cx - r - 20
    draw.ellipse([left_center-r, cy-r, left_center+r, cy+r], fill="red")
    draw_centered(draw, f"{diskon_utama}%", f_num, left_center, cy - font_size_num*0.1, "white")
    draw_centered(draw, "DISKON", f_lbl, left_center, cy + r*0.6 - font_size_lbl, "white")

    # b) Diskon Member
    right_center = cx + r + 20 - r*0 + 2*r
    # simpler: center at cx + r +20
    right_center = cx + r + 20
    draw.ellipse([right_center-r, cy-r, right_center+r, cy+r], fill="blue")
    draw_centered(draw, f"+{diskon_member}%", f_num, right_center, cy - font_size_num*0.1, "white")
    draw_centered(draw, "MEMBER", f_lbl, right_center, cy + r*0.6 - font_size_lbl, "white")

    # 3) HARGA AWAL (coret kecil merah, ke kiri)
    f_strike = load_font(int(font_size_num*0.4))
    txt0 = format_rp(harga_awal) + f" /{satuan_harga}"
    bbox0 = draw.textbbox((0,0), txt0, font=f_strike)
    w0 = bbox0[2]-bbox0[0]
    x0 = cx - w0//2 - r//2
    y0 = cy + r + 20
    draw.text((x0, y0), txt0, font=f_strike, fill="red")
    draw.line([(x0, y0+int(font_size_num*0.1)), (x0+w0, y0+int(font_size_num*0.1))], fill="red", width=3)

    # 4) HARGA PROMO (super besar)
    f_promo = load_font(int(font_size_num*1.2))
    txt1    = format_rp(harga_promo) + f" /{satuan_harga}"
    draw_centered(draw, txt1, f_promo, cx, y0 + font_size_num*0.8, "black")

    # 5) NAMA PRODUK di bawah lingkaran
    f_prod = load_font(50)
    draw_centered(draw, nama_produk, f_prod, cx, H - 120, "black")

    # — Show & Download —
    st.image(bg, use_column_width=True)
    buf = io.BytesIO(); bg.save(buf,"PNG")
    st.download_button("⬇️ Download POP", buf.getvalue(), "POP_final.png", "image/png")

else:
    st.info("Upload background untuk lihat preview real‑time.")
