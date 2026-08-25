import gc
import time
import numpy as np
import pandas as pd
import streamlit as st

from pengaturan.konfigurasi import (
    BATAS_KESUKARAN_SUKAR,
    BATAS_KESUKARAN_MUDAH,
    BATAS_DAYA_BEDA_SANGAT_BAIK,
    BATAS_DAYA_BEDA_BAIK,
    BATAS_DAYA_BEDA_CUKUP
)

def _hitung_analisis_butir_soal(matriks_biner, total_skor, jumlah_soal, str_kunci):
    """Menhitung tingkat kesukaran (p) dan daya beda (r_pbi) per butir soal."""
    hasil_item = []
    std_total = np.std(total_skor, ddof=1)

    for idx in range(jumlah_soal):
        kolom_item = matriks_biner[:, idx]
        p_val = float(np.mean(kolom_item))
        
        # Kategori Kesukaran
        if p_val < BATAS_KESUKARAN_SUKAR:
            kat_sukar = "Sukar"
        elif p_val <= BATAS_KESUKARAN_MUDAH:
            kat_sukar = "Sedang"
        else:
            kat_sukar = "Mudah"

        # Daya Beda (Korelasi Point-Biserial)
        std_item = np.std(kolom_item, ddof=1)
        if std_item > 0 and std_total > 0:
            rpbi = float(np.corrcoef(kolom_item, total_skor)[0, 1])
        else:
            rpbi = 0.0

        # Kategori Daya Beda
        if rpbi >= BATAS_DAYA_BEDA_SANGAT_BAIK:
            kat_db = "Sangat Baik"
        elif rpbi >= BATAS_DAYA_BEDA_BAIK:
            kat_db = "Baik"
        elif rpbi >= BATAS_DAYA_BEDA_CUKUP:
            kat_db = "Cukup (Perlu Revisi)"
        else:
            kat_db = "Buruk (Dibuang/Revisi Total)"

        hasil_item.append({
            "No Soal": f"Soal {idx+1}",
            "Kunci": str_kunci[idx],
            "Tingkat Kesukaran (p)": round(p_val, 3),
            "Kategori Kesukaran": kat_sukar,
            "Daya Beda (r_pbi)": round(rpbi, 3),
            "Kategori Daya Beda": kat_db
        })
    return hasil_item

def _hitung_statistik_deskriptif(total_skor, total_data):
    """Menghitung ringkasan statistik deskriptif distribusi skor."""
    s_series = pd.Series(total_skor)
    modus_val = s_series.mode()
    modus_str = str(round(modus_val[0], 2)) if not modus_val.empty else "-"

    return pd.DataFrame({
        "Parameter Statistik": [
            "Jumlah Peserta (N)", "Rata-rata (Mean)", "Median", "Modus",
            "Standar Deviasi (SD)", "Varians", "Skor Minimum", "Skor Maksimum",
            "Rentang Skor (Range)", "Kemiringan (Skewness)", "Keruncingan (Kurtosis)"
        ],
        "Nilai": [
            f"{total_data:,}", f"{s_series.mean():.2f}", f"{s_series.median():.2f}", modus_str,
            f"{s_series.std():.2f}", f"{s_series.var():.2f}", f"{s_series.min()}", f"{s_series.max()}",
            f"{s_series.max() - s_series.min()}", f"{s_series.skew():.3f}", f"{s_series.kurtosis():.3f}"
        ]
    })

@st.cache_data(show_spinner=False)
def proses_analisis_psikometri(df_respon, df_kunci, kd_mapel_pilihan=None):
    """Engine utama pengolahan skor psikometri berskala besar."""
    if 'jawaban' not in df_respon.columns or 'nomor' not in df_respon.columns:
        st.error("File Respon harus memiliki kolom 'nomor' dan 'jawaban'!")
        return None, None, None, None

    if 'kunci' not in df_kunci.columns:
        st.error("File Kunci Jawaban harus memiliki kolom 'kunci'!")
        return None, None, None, None

    if 'kd_mapel' in df_respon.columns and kd_mapel_pilihan:
        df_respon = df_respon[df_respon['kd_mapel'].astype(str).str.strip() == str(kd_mapel_pilihan)]

    if 'kd_mapel' in df_kunci.columns and kd_mapel_pilihan:
        df_kunci = df_kunci[df_kunci['kd_mapel'].astype(str).str.strip() == str(kd_mapel_pilihan)]

    str_kunci = str(df_kunci['kunci'].iloc[0]).strip().upper()
    jumlah_soal = len(str_kunci)
    total_data = len(df_respon)

    progress_text = f"Memproses {total_data:,} data (batch per 100.000 data)..."
    progress_bar = st.progress(0, text=progress_text)

    arr_kunci = np.array(list(str_kunci))
    batch_size = 100_000
    matriks_biner_list = []
    
    jawaban_series = df_respon['jawaban'].astype(str).str.strip().str.upper().str.ljust(jumlah_soal)
    total_batches = (total_data + batch_size - 1) // batch_size
    
    for b_idx, i in enumerate(range(0, total_data, batch_size)):
        batch_jwb = jawaban_series.iloc[i:i+batch_size].to_numpy()
        batch_matriks = np.array([list(jwb[:jumlah_soal]) for jwb in batch_jwb])
        batch_biner = (batch_matriks == arr_kunci).astype(np.uint8)
        matriks_biner_list.append(batch_biner)

        persen = int(((b_idx + 1) / total_batches) * 100)
        progress_bar.progress(persen, text=f"{progress_text} ({persen}%)")

    time.sleep(0.2)
    progress_bar.empty()

    matriks_biner = np.vstack(matriks_biner_list)
    del matriks_biner_list
    gc.collect()

    total_skor = matriks_biner.sum(axis=1, dtype=np.uint16)

    hasil_item = _hitung_analisis_butir_soal(matriks_biner, total_skor, jumlah_soal, str_kunci)
    df_hasil_item = pd.DataFrame(hasil_item)

    # Menghitung Cronbach's Alpha (Reliabilitas)
    k = jumlah_soal
    varians_item = np.var(matriks_biner, axis=0, ddof=1).sum()
    varians_total = np.var(total_skor, ddof=1)
    cronbach_alpha = (k / (k - 1)) * (1 - (varians_item / varians_total)) if varians_total > 0 and k > 1 else 0.0

    df_deskriptif = _hitung_statistik_deskriptif(total_skor, total_data)

    df_rekap_skor = pd.DataFrame({
        'Kode_Peserta': df_respon['nomor'].values,
        'Total_Skor': total_skor
    })

    del matriks_biner
    gc.collect()

    return df_rekap_skor, df_hasil_item, round(cronbach_alpha, 3), df_deskriptif