import streamlit as st
# ===== HEADER RESMI KEMENPERIN =====

col1, col2 = st.columns([1, 4])

with col1:
    st.image(
    "https://kemenperin.go.id/images/logo-kemenperin.png",
    width=100
)


with col2:
    st.markdown("""
    <div style="line-height:1.4">
        <b>KEMENTERIAN PERINDUSTRIAN REPUBLIK INDONESIA</b><br>
        <b>DIREKTORAT JENDERAL INDUSTRI KIMIA, FARMASI DAN TEKSTIL</b><br>
        Jl. Jenderal Gatot Subroto Kav. 52-53 Jakarta 12950
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border:2px solid black;'>", unsafe_allow_html=True)

# =========================
# HEADER KEMENPERIN
# =========================



st.title("AI Notulensi Rapat IKFT (Hybrid Mode)")

# =========================
# INPUT
# =========================

tanggal = st.date_input("Tanggal Rapat")
judul = st.text_input("Judul Rapat")
peserta = st.text_area("Peserta Rapat")
catatan = st.text_area("Catatan / Transkrip Rapat")

# Optional API key (boleh dikosongkan)
api_key = st.text_input("API Key OpenAI (Opsional)", type="password")

# =========================
# BUTTON
# =========================

if st.button("Generate Notulensi"):

    # =========================
    # MODE GRATIS (Template)
    # =========================
    if api_key == "":
        hasil = f"""
NOTULENSI RAPAT  
Direktorat Jenderal IKFT  

Tanggal: {tanggal}  
Judul: {judul}  

I. Pendahuluan  
Rapat dilaksanakan dalam rangka membahas agenda terkait {judul}.

II. Peserta Rapat  
{peserta}

III. Pokok Pembahasan  
{catatan}

IV. Kesimpulan  
Berdasarkan hasil pembahasan, diperlukan tindak lanjut sesuai hasil rapat.

V. Tindak Lanjut  
1. Koordinasi lanjutan antar unit terkait.  
2. Penyusunan laporan perkembangan.  
"""

    # =========================
    # MODE AI (Jika API Ada)
    # =========================
    else:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        prompt = f"""
Susun notulensi rapat resmi Direktorat Jenderal IKFT
dengan bahasa Indonesia formal dan sistematis.

Data:
Tanggal: {tanggal}
Judul: {judul}
Peserta: {peserta}

Catatan Rapat:
{catatan}

Struktur:
1. Identitas Rapat
2. Pendahuluan
3. Pokok Pembahasan
4. Kesimpulan
5. Tindak Lanjut
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        hasil = response.choices[0].message.content

    st.subheader("Hasil Notulensi")
    st.text_area("Output", hasil, height=400)
