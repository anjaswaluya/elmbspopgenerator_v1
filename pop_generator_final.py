import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="ELMBS POP Generator", layout="centered")

# ========= SIDEBAR ==========
with st.sidebar:
    st.header("📦 Data Produk")

    nama_produk = st.text_input("Nama Produk", "Contoh: GRANIT 60x60 TRISENSA")

    harga_awal = st.number_input("Harga Awal", min_value=0, value=250000)
    harga_promo = st.number_input("Harga Promo", min_value=0, value=225000)

    satuan_custom = st.text_input("Satuan Harga", value="m")
    
    diskon_utama = st.number_input("Diskon Utama (%)", min_value=0, value=5)
    diskon_member = st.number_input("Diskon Member (%)", min_value=0, value=3)

    st.markdown("---")
    st.header("🖼️ Upload Gambar")

    bg_file = st.file_uploader("Upload Background (rasio A4)", type=["jpg", "jpeg", "png"])
    logo_files = st.file_uploader("Upload Logo Produk (max 6)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    generate = st.button("🎯 Generate POP")

# ========= FUNGSI ==========
def format_rupiah(x):
    return f"Rp{x:,.0f}".replace(",", ".")

def get_font(sz):
    try: return ImageFont.truetype("arial.ttf", sz)
    except: return ImageFont.load_default()

def draw_centered(draw, text, font, cx, y, fill="black"):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = cx - w // 2
    draw.text((x, y), text, font=font, fill=fill)

# ========= OUTPUT ==========
if generate and bg_file:
    bg = Image.open(bg_file).convert("RGBA")
    W, H = bg.size
    draw = ImageDraw.Draw(bg)
    cx = W // 2

    # ---------- LOGO ----------
    logo_y = 80
    if logo_files:
        max_logos = min(len(logo_files), 6)
        logo_imgs = [Image.open(f).convert("RGBA") for f in logo_files[:max_logos]]
        logo_w = 180
        gap = 40
        total_width = logo_w * max_logos + gap * (max_logos - 1)
        start_x = (W - total_width) // 2

        for i, logo in enumerate(logo_imgs):
            logo.thumbnail((logo_w, logo_w))
            lx = start_x + i * (logo_w + gap)
            bg.paste(logo, (lx, logo_y), logo)

    # ---------- DISKON CIRCLES ----------
    f_disc = get_font(80)
    f_label = get_font(30)
    cy = 400

    # Diskon utama (merah)
    r = 130
    draw.ellipse([cx - r - 100, cy - r, cx - 100 + r, cy + r], fill="red")
    draw_centered(draw, f"{diskon_utama}%", f_disc, cx - 100, cy - 30, "white")
    draw_centered(draw, "DISKON", f_label, cx - 100, cy + 60, "white")

    # Diskon member (biru)
    draw.ellipse([cx + 100 - r, cy - r, cx + 100 + r, cy + r], fill="blue")
    draw_centered(draw, f"+{diskon_member}%", f_disc, cx + 100, cy - 30, "white")
    draw_centered(draw, "MEMBER", f_label, cx + 100, cy + 60, "white")

    # ---------- PRODUK NAME ----------
    f_prod = get_font(60)
    draw_centered(draw, nama_produk, f_prod, cx, cy + 150, "black")

    # ---------- HARGA ----------
    f_awal = get_font(40)
    f_promo = get_font(100)

    harga_y = cy + 250

    h_awal = f"{format_rupiah(harga_awal)} /{satuan_custom}"
    bbox = draw.textbbox((0, 0), h_awal, font=f_awal)
    w_awal = bbox[2] - bbox[0]
    x_awal = cx - w_awal // 2
    draw.text((x_awal, harga_y), h_awal, font=f_awal, fill="red")
    draw.line([(x_awal, harga_y + 25), (x_awal + w_awal, harga_y + 25)], fill="red", width=3)

    harga_promo_text = f"{format_rupiah(harga_promo)} /{satuan_custom}"
    draw_centered(draw, harga_promo_text, f_promo, cx, harga_y + 80, "black")

    # ---------- PREVIEW & DOWNLOAD ----------
    st.image(bg, use_column_width=True)
    buf = io.BytesIO()
    bg.save(buf, format="PNG")
    st.download_button("⬇️ Download POP", buf.getvalue(), "POP_final.png", "image/png")

else:
    st.info("Upload background dan isi semua data, lalu klik tombol Generate.")
