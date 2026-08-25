import streamlit as st

def inisialisasi_halaman():
    """Mengatur konfigurasi awal tab browser Streamlit."""
    st.set_page_config(
        page_title="Dashboard Analisis Psikometri",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# Batas Kriteria Psikometri Global
BATAS_RELIABILITAS_TINGGI = 0.70
BATAS_RELIABILITAS_SEDANG = 0.50

BATAS_KESUKARAN_SUKAR = 0.30
BATAS_KESUKARAN_MUDAH = 0.70

BATAS_DAYA_BEDA_SANGAT_BAIK = 0.40
BATAS_DAYA_BEDA_BAIK = 0.30
BATAS_DAYA_BEDA_CUKUP = 0.20