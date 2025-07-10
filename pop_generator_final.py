import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(layout="wide")
st.title("POP Generator Optimal")

# === Sidebar ===
st.sidebar.header("Data Produk")
nama_produk = st.sidebar.text_input("Nama Produk", "GRANIT POLISHED 80X160")
harga_awal = st.sidebar.number_input("Harga Awal", 0, step=1000, value=269141)
harga_promo = st.sidebar.number_input("Harga Promo", 0, step=1000, value=248013)
satuan = st.sidebar.text_input("Satuan (ex: m, pcs)", "m")
diskon_utama = st.sidebar.number_input("Diskon Utama (%)", 0, 100, 5)
diskon_member = st.sidebar.number_input("Diskon Member (%)", 0, 100, 3)

# === Upload ===
st.sidebar.header("Upload Gambar")
background_file = st.sidebar.file_uploader("Background (rasio A4)", type=["jpg", "jpeg", "png"])
logo_files = st.sidebar.file_uploader("Upload Logo Produk (max 6)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# === Slider Pengaturan ===
st.sidebar.header("Pengaturan Real-Time")
uk_lingkaran = st.sidebar.slider("Ukuran Lingkaran Diskon", 50, 300, 120)
uk_font_diskon = st.sidebar.slider("Ukuran Font Angka Diskon", 20, 150, 80)
uk_font_label = st.sidebar.slider("Ukuran Font Label Diskon", 10, 80, 30)
uk_font_judul = st.sidebar.slider("Ukuran Font Judul", 10, 200, 60)

# === Fungsi Center Text ===
def center_text(draw, text, font, x, y):
    w, h = draw.textsize(text, font=font)
    draw.text((x - w/2, y - h/2), text, font=font, fill="white")

# === Proses Gambar ===
if background_file is not None:
    bg = Image.open(background_file).convert("RGBA")
    bg_w, bg_h = bg.size

    draw = ImageDraw.Draw(bg)

    # === Logo Mitra (static di atas) ===
    mitra_logo = Image.open("mitra_logo.png").convert("RGBA").resize((int(bg_w*0.25), int(bg_h*0.07)))
    bg.paste(mitra_logo, (int(bg_w/2 - mitra_logo.width/2), int(bg_h*0.03)), mitra_logo)

    # === Judul Produk ===
    font_judul = ImageFont.truetype("arialbd.ttf", uk_font_judul)
    draw.text((bg_w/2, int(bg_h*0.15)), nama_produk, font=font_judul, fill="black", anchor="mm")

    # === Logo Produk ===
    if logo_files:
        logo_area_y = int(bg_h * 0.2)
        logo_max_h = int(bg_h * 0.08)
        total_logos = len(logo_files)
        space_between = int(bg_w * 0.02)
        logo_width = int((bg_w * 0.5 - (space_between * (total_logos - 1))) / total_logos)

        start_x = int(bg_w / 2 - (logo_width * total_logos + space_between * (total_logos - 1)) / 2)

        for i, logo_file in enumerate(logo_files[:6]):
            logo = Image.open(logo_file).convert("RGBA")
            ratio = logo.height / logo.width
            new_h = logo_max_h
            new_w = int(new_h / ratio)
            logo_resized = logo.resize((new_w, new_h), resample=Image.Resampling.LANCZOS)
            pos_x = start_x + i * (new_w + space_between)
            bg.paste(logo_resized, (pos_x, logo_area_y), logo_resized)

    # === Lingkaran Diskon ===
    lingkaran_x = int(bg_w * 0.35)
    lingkaran_y = int(bg_h * 0.4)
    draw.ellipse([
        (lingkaran_x - uk_lingkaran, lingkaran_y - uk_lingkaran),
        (lingkaran_x + uk_lingkaran, lingkaran_y + uk_lingkaran)
    ], fill="red")

    font_diskon = ImageFont.truetype("arialbd.ttf", uk_font_diskon)
    font_label = ImageFont.truetype("arial.ttf", uk_font_label)

    center_text(draw, f"{diskon_utama}%", font_diskon, lingkaran_x, lingkaran_y)
    center_text(draw, "DISKON", font_label, lingkaran_x, lingkaran_y - uk_font_diskon)

    # === Harga Coret + Promo ===
    font_harga_kecil = ImageFont.truetype("arial.ttf", 28)
    font_harga_besar = ImageFont.truetype("arialbd.ttf", 48)

    harga_area_y = int(bg_h * 0.75)

    draw.text((bg_w/2 - 80, harga_area_y), f"Rp {harga_awal:,}/{satuan}", font=font_harga_kecil, fill="red")
    draw.line([
        (bg_w/2 - 85, harga_area_y + 10),
        (bg_w/2 + 55, harga_area_y + 10)
    ], fill="red", width=2)

    draw.text((bg_w/2 - 60, harga_area_y + 40), f"Rp. {harga_promo:,}/{satuan}", font=font_harga_besar, fill="red")

    # === Output ===
    st.image(bg, use_column_width=True)
    buf = io.BytesIO()
    bg.save(buf, format="PNG")
    st.download_button("Download POP", data=buf.getvalue(), file_name="pop_final.png", mime="image/png")
