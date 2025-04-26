 Cara Menjalankan Aplikasi
Pastikan Python dan Streamlit sudah terinstal
Jika belum, instal dengan perintah berikut:


pip install streamlit nbformat
Simpan kode berikut sebagai app.py

import streamlit as st
import json
import nbformat

# Fungsi untuk membaca file .ipynb dan mengembalikan kontennya dalam bentuk teks
def read_ipynb(file):
    try:
        notebook = nbformat.read(file, as_version=4)
        return json.dumps(notebook, indent=2)
    except Exception as e:
        return f"Error: {e}"

st.title("Jupyter Notebook Viewer")

# Upload file .ipynb
uploaded_file = st.file_uploader("Upload a Jupyter Notebook (.ipynb)", type=["ipynb"])

if uploaded_file is not None:
    content = read_ipynb(uploaded_file)
    st.text_area("Notebook Content", content, height=400)

    # Tombol untuk mengunduh kembali file
    st.download_button(
        label="Download File",
        data=uploaded_file.getvalue(),
        file_name=uploaded_file.name,
        mime="application/json"
    )

# Menjalankan aplikasi secara lokal
if __name__ == "__main__":
    st.write("Jalankan perintah berikut di terminal untuk membuka aplikasi:")
    st.code("streamlit run.py")
Jalankan aplikasi dengan perintah berikut di terminal

streamlit run Python.py
Buka browser dan akses aplikasi
Aplikasi akan berjalan di http://localhost:8501/, dan Anda dapat mulai mengunggah serta mengunduh file .ipynb.