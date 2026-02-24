import streamlit as st
from openai import OpenAI
import json
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)
# =============================
# HEADER RESMI
# =============================

col1, col2 = st.columns([1, 4])

with col1:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/3/3f/Logo_Kementerian_Perindustrian_Indonesia.png",
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

st.title("AI NOTULENSI RAPAT IKFT – V2 Professional")

# =============================
# INPUT
# =============================

tanggal = st.date_input("Tanggal Rapat")
judul = st.text_input("Judul / Agenda Rapat")
waktu = st.text_input("Waktu")
tempat = st.text_input("Tempat")
pimpinan = st.text_input("Pimpinan Rapat")
mode = st.selectbox("Mode Rapat", ["Luring", "Daring"])
peserta = st.text_area("Peserta Rapat")
catatan = st.text_area("Catatan / Transkrip Kasar")



# =============================
# GENERATE
# =============================

if st.button("Generate Notulensi V2"):

    # =============================
    # PROMPT MATRKS AKSI
    # =============================

    prompt_matrix = f"""
    Anda adalah analis notulensi resmi instansi pemerintahan.

    Buat Matriks Aksi dari catatan rapat berikut.

    Agenda Rapat: {judul}

    Identifikasi:
    - Keputusan
    - Tindak lanjut
    - Penanggung jawab
    - Deadline

    Jika tidak ada penanggung jawab tulis: Belum ditentukan
    Jika tidak ada deadline tulis: Tidak disebutkan

    WAJIB:
    - Keluarkan HANYA JSON valid.
    - Jangan tambahkan teks apapun di luar JSON.

    Format JSON:
    {{
      "data": [
        {{
          "agenda_rapat": "",
          "keputusan": "",
          "tindak_lanjut": "",
          "penanggung_jawab": "",
          "deadline": "",
          "status": "Belum Ditindaklanjuti"
        }}
      ]
    }}

    Catatan:
    {catatan}
    """

    response_matrix = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt_matrix}],
        temperature=0
    )
    matrix_json = response_matrix.choices[0].message.content

try:
    # Bersihkan markdown jika ada ```json
    if matrix_json.strip().startswith("```"):
        matrix_json = matrix_json.strip()
        matrix_json = matrix_json.replace("```json", "")
        matrix_json = matrix_json.replace("```", "")
        matrix_json = matrix_json.strip()

    matrix_data = json.loads(matrix_json)

    st.subheader("Matriks Aksi")
    st.table(matrix_data["data"])

except Exception as e:
    st.error("Format Matriks tidak terbaca.")
    st.write("Output mentah dari AI:")
    st.code(response_matrix.choices[0].message.content)
    # =============================
    # PROMPT NOTULEN RESMI
    # =============================

    prompt_notulen = f"""
    Anda adalah notulis profesional instansi pemerintahan.

    Susun notulen resmi dengan struktur berikut:

    NOTULEN RAPAT

    Tanggal: {tanggal}
    Waktu: {waktu}
    Tempat: {tempat}
    Perihal: {judul}
    Pimpinan Rapat: {pimpinan}

    A. UMUM
    1. Pelaksanaan Rapat
    2. Tujuan Rapat

    B. LATAR BELAKANG
    (poin 1,2,3)

    C. PEMBAHASAN
    (dikelompokkan berdasarkan tema)

    D. REKOMENDASI DAN TINDAK LANJUT
    (bernomor dan formal)

    Gunakan bahasa birokrasi formal.
    Jangan menambahkan informasi yang tidak ada dalam catatan.

    Catatan Rapat:
    {catatan}
    """
    response_notulen = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_notulen}],
            temperature=0.2
        )
    st.subheader("Notulen Resmi")
    st.text_area("Output Notulen", response_notulen.choices[0].message.content, height=400)
