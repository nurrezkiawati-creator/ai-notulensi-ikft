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

Anda adalah penyusun RISALAH RAPAT resmi tingkat kementerian.
Gunakan bahasa Indonesia baku, formal, administratif, objektif, dan teknokratis.
Hasil harus layak menjadi dokumen arsip resmi dan bahan laporan pimpinan.

Ketentuan umum:
- Tidak menambahkan isu baru yang tidak dibahas dalam catatan rapat.
- Tidak menuliskan dialog atau transkrip percakapan.
- Tidak menggunakan kata ganti orang pertama.
- Tidak bersifat opini.
- Gunakan penomoran Romawi dan Arab.
- Tidak menggunakan bullet simbol.
- Ringkas namun tetap substantif.

RISALAH RAPAT

Tanggal: {tanggal}
Waktu: {waktu}
Tempat: {tempat}
Perihal: {judul}
Pimpinan Rapat: {pimpinan}

I. UMUM
Uraikan secara formal dan netral mengenai:
1. Pimpinan rapat
2. Waktu dan tempat pelaksanaan
3. Unit kerja/instansi yang hadir
Gunakan redaksi administratif tanpa opini.

II. LATAR BELAKANG
Meskipun dalam rapat latar belakang dapat disampaikan secara singkat, kembangkan bagian ini secara lebih detail namun tetap padat dan substantif dengan ketentuan:

1. Gunakan informasi dalam catatan rapat sebagai dasar utama.
2. Apabila terdapat penyebutan regulasi, kebijakan, atau program nasional, jelaskan secara ringkas namun substantif mengenai:
   a. Konteks pembentukannya
   b. Tujuan pengaturannya
   c. Relevansinya terhadap materi yang dibahas
3. Diperbolehkan memperkaya penjelasan menggunakan informasi regulasi atau kebijakan resmi yang relevan dan kredibel untuk memperjelas konteks, tanpa menambahkan isu baru.
4. Susun secara runtut:
   a. Kondisi atau kebijakan nasional yang melatarbelakangi
   b. Permasalahan atau kebutuhan penyesuaian
   c. Alasan strategis dilaksanakannya rapat
Gunakan bahasa formal dan teknokratis tanpa opini atau asumsi.

III. POKOK PEMBAHASAN
Sajikan inti pembahasan secara sistematis dalam poin bernomor, meliputi:
1. Penjelasan atau pandangan unit kerja terkait
2. Isu strategis dan pertimbangan kebijakan
3. Arah atau kesepahaman yang mengemuka dalam rapat
Tidak mencantumkan transkrip dialog dan tidak melakukan interpretasi tambahan.

IV. REKOMENDASI DAN TINDAK LANJUT
Gabungkan rekomendasi dan tindak lanjut dalam satu bagian dengan ketentuan:
1. Hanya mencantumkan hal yang benar-benar dibahas dan disepakati dalam rapat.
2. Setiap poin mencerminkan:
   a. Arah kebijakan atau kesimpulan rapat
   b. Unit kerja/pihak yang terkait (jika disebut)
   c. Bentuk tindak lanjut yang jelas dan operasional
Gunakan kalimat formal, tegas, dan administratif.

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
