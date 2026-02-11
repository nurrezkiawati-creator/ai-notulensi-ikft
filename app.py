import streamlit as st
import requests
st.image("https://upload.wikimedia.org/wikipedia/commons/3/3f/Logo_Kementerian_Perindustrian_Indonesia.png", width=120)

st.markdown("""
### DIREKTORAT JENDERAL INDUSTRI KIMIA, FARMASI DAN TEKSTIL  
Jl. Jenderal Gatot Subroto Kav. 52-53 Jakarta 12950  
""")
st.divider()



st.title("AI Notulensi Rapat IKFT")

st.header("Input Data Rapat")

tanggal = st.date_input("Tanggal Rapat")
judul = st.text_input("Judul Rapat")
peserta = st.text_area("Peserta Rapat")
catatan = st.text_area("Catatan / Transkrip Rapat")

if st.button("Generate Notulensi"):

    prompt = f"""
Susun notulensi rapat resmi Direktorat Jenderal IKFT
dengan bahasa Indonesia formal.

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

    # sementara output dummy (nanti kita sambungkan ke AI)
    hasil = "Notulensi akan muncul di sini setelah terhubung ke AI."

    st.subheader("Hasil Notulensi")
    st.text_area("Output", hasil, height=300)
