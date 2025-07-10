import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# ------------------- Konfigurasi Streamlit -------------------
st.set_page_config(page_title="POP Generator Optimal", layout="centered")
st.title("POP Generator Optimal")

# Slider pada sidebar untuk mengatur ukuran font judul produk
font_size = st.sidebar.slider(
    "Ukuran Font Judul", min_value=10, max_value=200, value=50, step=1
)

# Input: Unggah hingga 6 logo produk (JPG/PNG)
uploaded_files = st.file_uploader(
    "Upload Logo Produk (JPG/PNG, maksimal 6 file)", 
    type=["jpg", "jpeg", "png"], accept_multiple_files=True
)

# Input: Judul produk (teks)
product_title = st.text_input("Judul Produk:")

# Proses hanya jika ada minimal satu file logo yang diunggah
if uploaded_files and product_title:
    # Batasi maksimal 6 logo
    if len(uploaded_files) > 6:
        st.warning("Hanya diperbolehkan maksimal 6 logo. Menggunakan 6 logo pertama saja.")
        uploaded_files = uploaded_files[:6]
    
    # Baca logo menggunakan PIL
    logos = [Image.open(file) for file in uploaded_files]

    # Tentukan ukuran kanvas dengan rasio A4 (lebar x tinggi)
    canvas_width = 1000  # lebar kanvas (px)
    canvas_height = int(canvas_width * 1.4142)  # tinggi = lebar * sqrt(2) untuk rasio A4
    image = Image.new("RGB", (canvas_width, canvas_height), color="white")
    draw = ImageDraw.Draw(image)

    # Atur dimensi logo (seragam tinggi) dan hitung total lebar semua logo
    if logos:
        # Tinggi maksimal untuk semua logo (misal 20% tinggi kanvas)
        logo_height = int(canvas_height * 0.2)
        resized_logos = []
        total_logos_width = 0

        for logo in logos:
            # Rasio skala untuk logo
            ratio = logo_height / logo.height
            new_width = int(logo.width * ratio)
            # Ubah ukuran logo agar memiliki tinggi yang sama
            logo_resized = logo.resize((new_width, logo_height), resample=Image.ANTIALIAS)
            resized_logos.append(logo_resized)
            total_logos_width += new_width

        # Hitung jarak/gap horizontal antara logo
        n = len(resized_logos)
        gap = (canvas_width - total_logos_width) // (n + 1) if n > 0 else 0
        current_x = gap
        logo_y = int(canvas_height * 0.05)  # margin atas (5% dari tinggi kanvas)

        # Tempelkan logo ke kanvas secara horizontal berurutan
        for logo_resized in resized_logos:
            image.paste(logo_resized, (current_x, logo_y))
            current_x += logo_resized.width + gap

    # Siapkan font untuk teks judul produk (Arial atau default)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Ukur dimensi teks untuk penempatan di tengah horizontal
    text = product_title
    text_width, text_height = draw.textsize(text, font=font)

    # Jika teks terlalu lebar, skala ukuran font agar tidak melebihi kanvas (opsional)
    if text_width > canvas_width * 0.9:
        scale = (canvas_width * 0.9) / text_width
        new_size = max(int(font_size * scale), 1)
        try:
            font = ImageFont.truetype("arial.ttf", new_size)
        except IOError:
            font = ImageFont.load_default()
        text_width, text_height = draw.textsize(text, font=font)

    # Posisi teks: horizontal center, vertical di bawah logo
    text_x = (canvas_width - text_width) // 2
    # Jika ada logo, letakkan teks tepat di bawah logo; jika tidak ada logo, bisa di tengah kanvas
    if logos:
        # Jarak teks di bawah logo (misal 5% dari tinggi logo area)
        vertical_gap = int(canvas_height * 0.05)
        text_y = logo_y + logo_height + vertical_gap
    else:
        # Jika tidak ada logo, tempatkan di tengah gambar
        text_y = (canvas_height - text_height) // 2

    # Gambar teks judul produk di kanvas
    draw.text((text_x, text_y), text, font=font, fill="black")

    # Tampilkan hasil di aplikasi Streamlit
    st.image(image, caption="Hasil Desain POP", use_column_width=True)
else:
    st.info("Silakan unggah minimal satu logo dan masukkan judul produk untuk membuat desain.")

