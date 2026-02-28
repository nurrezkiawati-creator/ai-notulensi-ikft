import streamlit as st
from openai import OpenAI
import json

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

if "generated" not in st.session_state:
    st.session_state.generated = False

if "validated" not in st.session_state:
    st.session_state.validated = False

if "matrix_data" not in st.session_state:
    st.session_state.matrix_data = None

if "notulen_text" not in st.session_state:
    st.session_state.notulen_text = ""
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


    # Bersihkan markdown jika ada ```json
    if matrix_json.strip().startswith("```"):
        matrix_json = matrix_json.strip()
        matrix_json = matrix_json.replace("```json", "")
        matrix_json = matrix_json.replace("```", "")
        matrix_json = matrix_json.strip()

    matrix_data = json.loads(matrix_json)

    st.subheader("Matriks Aksi")
    st.table(matrix_data["data"])


    # =============================
    # PROMPT NOTULEN RESMI
    # =============================

    prompt_notulen = f"""

    ANDA ADALAH notulis resmi kementerian Republik Indonesia yang bertugas menyusun RISALAH RAPAT formal tingkat direktorat/deputi/eselon I.

    Tugas Anda adalah mengubah transkrip rapat menjadi dokumen RISALAH RAPAT resmi dengan gaya bahasa birokratis, formal, sistematis, naratif-analitis, dan siap diedarkan sebagai dokumen kementerian.

    FORMAT DOKUMEN

    NOTULA RAPAT  
    Tanggal : {tanggal}  
    Waktu : {waktu}  
    Tempat : {tempat}  
    Perihal : {perihal}  
    Pimpinan Rapat : {pimpinan}

    RISALAH RAPAT  

    I. Umum  
    II. Latar Belakang  
    III. Pembahasan  
    IV. Rekomendasi dan Tindak Lanjut  

    Gunakan penomoran bertingkat:

    Romawi (I, II, III, IV)

    Angka (1, 2, 3)

    Huruf (a, b, c) bila diperlukan

    Jangan gunakan bullet simbol (•)

    KETENTUAN PENULISAN PER BAGIAN

    I. UMUM

    Poin 1 WAJIB berupa narasi:

   “Rapat ini dipimpin oleh … selaku … dan dilaksanakan secara (luring/daring/hybrid) pada …”

    Poin 2 WAJIB berupa tujuan rapat dalam kalimat normatif panjang:

    “Rapat ini diselenggarakan dalam rangka … serta bertujuan untuk …”

    Poin 3 WAJIB memuat peserta secara naratif:

    “Adapun peserta rapat terdiri atas perwakilan dari …”

    Jangan menulis hanya berupa daftar singkat.

    II. LATAR BELAKANG

    Bagian ini HARUS:

    Menjelaskan konteks kebijakan

    Menjelaskan urgensi

    Menjelaskan dampak sektoral/nasional

    Menjelaskan risiko apabila tidak ditangani

    Ditulis minimal 2–4 paragraf analitis

    Gunakan frasa seperti:

    “Urgensi pembahasan dipicu oleh…”

    “Dalam rangka menjamin keberlanjutan…”

    “Kondisi tersebut berpotensi menimbulkan…”

    “Sehingga diperlukan langkah strategis…”

    “Dalam kerangka kebijakan nasional…”

    Hindari penjelasan yang terlalu singkat.

    III. PEMBAHASAN

    JANGAN menggunakan gaya percakapan seperti:
    “Direktur menyampaikan…”
    “ASAKI mengatakan…”

    Ganti dengan gaya impersonal dan normatif seperti:

    “Dijelaskan bahwa…”

    “Disampaikan bahwa…”

    “Ditegaskan bahwa…”

    “Diperkirakan bahwa…”

    “Dinyatakan bahwa…”

    “Diusulkan agar…”

    Pembahasan harus:

    Merumuskan substansi kebijakan

    Menjelaskan progres/indikator jika ada

    Menjelaskan kendala administratif/teknis

    Menjelaskan proyeksi atau estimasi dampak

    Tidak terlalu singkat

    Bersifat analitis, bukan hanya kronologis

    Jika terdapat data angka, uraikan secara formal.
    Jika ada target, jelaskan status capaiannya.
    Jika ada kendala, jelaskan implikasinya.

    IV. REKOMENDASI DAN TINDAK LANJUT

    Gunakan kalimat tegas dan normatif:

    “Disepakati bahwa…”

    “Ditetapkan bahwa…”

    “Sebagai tindak lanjut…”

    “Untuk menjamin keberlanjutan…”

    Jangan hanya berupa daftar tugas.
    Setiap poin harus berupa kalimat lengkap formal.

    KARAKTER BAHASA YANG WAJIB
    Formal birokratis
    Objektif
    Impersonal (hindari saya/kami/kita)
    Naratif panjang dan sistematis
    Menggunakan istilah regulatif dan administratif
    Tidak terlalu ringkas

    LARANGAN
    Jangan menggunakan gaya percakapan
    Jangan menggunakan bahasa informal
    Jangan terlalu singkat
    Jangan membuat ringkasan seperti minutes of meeting biasa
    Jangan menggunakan huruf kapital penuh untuk judul bab

    OUTPUT HARUS menyerupai dokumen risalah rapat kementerian yang siap dicetak dan diedarkan.
"""
    response_notulen = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_notulen}],
            temperature=0.2
        )
    st.subheader("Notulen Resmi")
    st.text_area("Output Notulen", response_notulen.choices[0].message.content, height=400)
