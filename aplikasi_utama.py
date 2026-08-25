import streamlit as st
import pandas as pd

# 1. Impor Modul Pengaturan
from pengaturan.konfigurasi import inisialisasi_halaman
from pengaturan.gaya_tampilan import terapkan_gaya_css

# 2. Impor Modul Mesin Inti
from mesin_inti.pembaca_data import unggah_dan_baca_file
from mesin_inti.hitung_psikometri import proses_analisis_psikometri

# 3. Impor Modul UI & Grafik
from komponen_ui.kartu_informasi import tampilkan_kartu_ringkasan
from komponen_ui.grafik_visual import buat_scatter_plot, buat_bar_chart, buat_histogram_skor

# Inisialisasi awal aplikasi
inisialisasi_halaman()
terapkan_gaya_css()

# --- HEADER APLIKASI ---
st.markdown('<div class="main-header">📊 Dashboard Analisis Psikometri</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Evaluasi Kualitas Butir Soal & Reliabilitas Skala Menggunakan Modul Terpisah</div>', unsafe_allow_html=True)

# --- SIDEBAR (PANEL UNGGAH FILE) ---
st.sidebar.header("📁 Panel Kontrol & Input")
file_respon = st.sidebar.file_uploader("Upload File Respon Siswa (CSV/DBF/ZIP/XLSX)", type=['csv', 'dbf', 'zip', 'xlsx', 'xls'])
file_kunci = st.sidebar.file_uploader("Upload File Kunci Jawaban (CSV/DBF/ZIP/XLSX)", type=['csv', 'dbf', 'zip', 'xlsx', 'xls'])

# --- ALUR UTAMA APLIKASI ---
if file_respon and file_kunci:
    df_respon = unggah_dan_baca_file(file_respon, label_file="Respon")
    df_kunci = unggah_dan_baca_file(file_kunci, label_file="Kunci")

    if df_respon is not None and df_kunci is not None:
        # Pilihan Kode Mata Pelajaran dihilangkan (otomatis diproses tanpa filter mapel)
        kd_mapel_pilihan = None

        # Tombol Eksekusi Analisis
        if st.sidebar.button("🚀 Mulai Analisis Psikometri", type="primary"):
            df_rekap, df_hasil_item, alpha, df_deskriptif = proses_analisis_psikometri(
                df_respon, df_kunci, kd_mapel_pilihan
            )

            if df_rekap is not None:
                st.success("Analisis berhasil diperbarui!")

                # Kartu Ringkasan Metric
                mapel_label = "Semua Mapel"
                tampilkan_kartu_ringkasan(
                    mapel=mapel_label,
                    jenjang="Ujian",
                    jumlah_peserta=len(df_rekap),
                    nilai_alpha=alpha,
                    jumlah_soal=len(df_hasil_item)
                )

                st.divider()

                # Tab Visualisasi & Tabel Data
                tab1, tab2, tab3 = st.tabs(["📊 Visualisasi Grafik", "📝 Analisis Butir Soal", "📈 Statistik Deskriptif"])

                with tab1:
                    # Scatter Plot dipanggil penuh tanpa pembagian kolom
                    st.plotly_chart(buat_scatter_plot(df_hasil_item), use_container_width=True)

                    # Histogram skor (dinonaktifkan sementara)
                    # st.plotly_chart(buat_histogram_skor(df_rekap), use_container_width=True)

                    # Grafik batang tingkat kesukaran
                    st.plotly_chart(buat_bar_chart(df_hasil_item), use_container_width=True)

                with tab2:
                    st.markdown('<div class="section-title">📋 Tabel Detail Analisis Per Butir Soal</div>', unsafe_allow_html=True)
                    st.dataframe(df_hasil_item, use_container_width=True)

                with tab3:
                    st.markdown('<div class="section-title">📌 Ringkasan Statistik Deskriptif Skor</div>', unsafe_allow_html=True)
                    st.dataframe(df_deskriptif, use_container_width=True)

else:
    st.info("💡 Silakan unggah **File Respon** dan **File Kunci Jawaban** pada panel di sebelah kiri untuk memulai analisis.")  