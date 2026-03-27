import streamlit as st
from openai import OpenAI
import json

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import io

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
    st.image("logo.png", width=140)

with col2:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:20px; line-height:1.4;">
        <div>
            <b>KEMENTERIAN PERINDUSTRIAN REPUBLIK INDONESIA</b><br>
            <b>DIREKTORAT JENDERAL INDUSTRI KIMIA, FARMASI DAN TEKSTIL</b><br>
            Jl. Jenderal Gatot Subroto Kav. 52-53 Jakarta 12950
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border:2px solid black;'>", unsafe_allow_html=True)

st.title("IKFT Smart Meeting Minutes System (AI-Powered Professional)")

# =============================
# INPUT
# =============================

tanggal = st.date_input("Tanggal Rapat")
perihal = st.text_input("Perihal")
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

    Agenda Rapat: {perihal}

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
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt_matrix}],
        temperature=0.2,
        max_tokens=4000
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

    Tugas Anda adalah mengubah catatan kasar atau transkrip rapat menjadi dokumen RISALAH RAPAT resmi dengan bahasa birokratis formal, sistematis, analitis, dan lengkap.
  
    PRINSIP UTAMA (WAJIB)
    Jangan merangkum secara berlebihan.
    Jangan menghilangkan informasi penting dari catatan.
    Semua isu yang penting dibahas, wajib muncul dalam dokumen akhir.
    Jika catatan panjang dan kompleks, hasil risalah juga harus panjang dan detail.
    Reformulasikan secara resmi tanpa mengurangi substansi.
    PROSES INTERNAL WAJIB (JANGAN DITAMPILKAN)

    Sebelum menulis RISALAH RAPAT, lakukan secara internal:
    Langkah 1 Inventarisasi Substansi
    Identifikasi seluruh:
    Isu yang dibahas
    Data dan angka
    Wilayah/lokasi yang disebut
    Regulasi/perizinan/ketentuan
    Kendala teknis dan administratif
    Usulan solusi
    Target dan indikator
    Estimasi dampak
    Tenggat waktu
    
    Langkah 2  Pengelompokan Isu
    Kelompokkan seluruh substansi ke dalam kategori yang logis agar tidak ada yang terlewat.
    Langkah 3 Formulasi Lengkap
    Tulis seluruh hasil inventarisasi tersebut ke dalam bagian Pembahasan secara sistematis dan lengkap
    Jangan tampilkan langkah ini dalam output.

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

    KETENTUAN PENULISAN PER BAGIAN

    I. UMUM
    Poin 1 WAJIB berupa narasi:
    Rapat ini dipimpin oleh selaku dan dilaksanakan secara (luring/daring/hybrid) pada, Adapun peserta rapat terdiri atas perwakilan dari
    Poin 2 WAJIB berupa tujuan rapat dalam kalimat normatif:
    Rapat ini diselenggarakan dalam rangka, serta bertujuan untuk,
    Jangan menulis hanya berupa daftar singkat.

    II. LATAR BELAKANG
    Bagian ini HARUS:
    Menjelaskan konteks kebijakan
    Menjelaskan pembahasan sebelumnya jika ada
    Menjelaskan urgensi
    Menjelaskan dampak sektoral/nasional
    Menjelaskan risiko apabila tidak ditangani
  
    Ditulis minimal 2 sampai 4 paragraf analitis


    III. PEMBAHASAN

    JANGAN menggunakan gaya percakapan seperti:
    Direktur menyampaikan
    ASAKI mengatakan
    Gunakan variasi kalimat formal seperti:
    Terdapat
    Kondisi menunjukkan
    Dalam konteks tersebut
    Hal ini berdampak pada
    Apabila tidak ditindaklanjuti
    Sehingga diperlukan langkah
    Dengan demikian
    
    Hindari penggunaan repetitif frasa seperti Dijelaskan bahwa di setiap poin.

    Pembahasan harus:
    Merumuskan substansi kebijakan
    Menjelaskan progres/indikator jika ada
    Menjelaskan kendala administratif/teknis
    Menjelaskan proyeksi atau estimasi dampak
    Memuat seluruh substansi rapat tanpa pengecualian.
    Tidak menyederhanakan detail penting menjadi kalimat umum.
    Menguraikan konteks, sebab, dampak, dan implikasi
    Menjelaskan seluruh informasi teknis jika ada.
    Memuat seluruh data, angka, istilah teknis, atau referensi regulasi yang disebut.
    Menjelaskan kendala dan solusi secara lengkap.
    Jika terdapat banyak isu, gunakan sub-poin agar sistematis.
    Bersifat analitis, bukan hanya kronologis
    Jika terdapat data angka, uraikan secara formal.
    Jika ada target, jelaskan status capaiannya.
    Jika ada kendala, jelaskan implikasinya.

    IV. REKOMENDASI DAN TINDAK LANJUT
    Rekomendasi harus:
    Berdasarkan seluruh pembahasan.
    Tidak menghilangkan usulan yang muncul.
    Menggunakan kalimat normatif seperti
    Disepakati bahwa
    Ditetapkan bahwa
    sebagai tindak lanjut
    Untuk menjamin keberlanjutan

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
    Jangan menggunakan huruf kapital penuh untuk perihal bab

    HECKLIST WAJIB SEBELUM OUTPUT
    Pastikan:
    Tidak ada isu dalam catatan yang hilang
    Tidak ada data yang dihapus
    Tidak ada wilayah atau detail teknis yang terlewat
    Tidak ada penyederhanaan berlebihan
    Semua informasi telah diformulasikan ulang secara lengkap

    OUTPUT HARUS menyerupai dokumen risalah rapat kementerian yang siap dicetak dan diedarkan.
"""
    response_notulen = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt_notulen},
            {"role": "user", "content": catatan}],
            temperature=0.2,
            max_tokens=4000
        )
    st.subheader("Notulen Resmi")
    st.text_area("Output Notulen", response_notulen.choices[0].message.content, height=400)
    # ================= EXPORT PDF =================
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import io

if st.button("Export PDF"):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    isi_notulen = response_notulen.choices[0].message.content

    elements.append(Paragraph("<b>NOTULA RAPAT</b>", styles["Title"]))
    elements.append(Spacer(1, 10))
    for line in isi_notulen.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 6))

    doc.build(elements)

    st.download_button(
        "Download PDF",
        buffer.getvalue(),
        file_name="notula_rapat.pdf",
        mime="application/pdf"
    )
