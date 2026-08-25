import os
import zipfile
import tempfile
import io
import pandas as pd
from dbfread import DBF
import streamlit as st

def optimalkan_memori_dataframe(df):
    """
    Mengoptimalkan konsumsi RAM dengan mengubah nama kolom 
    dan tipe data teks menjadi kategori jika memungkinkan.
    """
    df.columns = [str(col).lower().strip() for col in df.columns]
    for col in df.columns:
        if df[col].dtype == 'object':
            if col in ['nomor', 'kd_mapel']:
                df[col] = df[col].astype('category')
            else:
                df[col] = df[col].astype(str)
    return df

def _baca_file_dbf(jalur_file):
    """Fungsi pembantu internal untuk membaca file DBF."""
    tabel = DBF(jalur_file, encoding='latin-1', char_decode_errors='ignore')
    return pd.DataFrame(iter(tabel))

@st.cache_data(show_spinner=False)
def baca_file_tersimpan(file_bytes, nama_file):
    """
    Membaca file dari memori buffer (CSV, Excel, DBF, ZIP) 
    dan mengembalikan DataFrame yang sudah teroptimasi.
    """
    nama_file_lower = nama_file.lower()
    df = None
    
    if nama_file_lower.endswith('.zip'):
        with tempfile.TemporaryDirectory() as direktori_sementara:
            jalur_zip = os.path.join(direktori_sementara, "temp.zip")
            with open(jalur_zip, "wb") as f:
                f.write(file_bytes)
                
            with zipfile.ZipFile(jalur_zip, 'r') as zip_ref:
                zip_ref.extractall(direktori_sementara)
                for nama_di_zip in zip_ref.namelist():
                    jalur_ekstraksi = os.path.join(direktori_sementara, nama_di_zip)
                    f_lower = nama_di_zip.lower()
                    
                    if f_lower.endswith('.csv'):
                        df = pd.read_csv(jalur_ekstraksi, engine='c')
                        break
                    elif f_lower.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(jalur_ekstraksi)
                        break
                    elif f_lower.endswith('.dbf'):
                        df = _baca_file_dbf(jalur_ekstraksi)
                        break

    elif nama_file_lower.endswith('.csv'):
        df = pd.read_csv(io.BytesIO(file_bytes), engine='c')
        
    elif nama_file_lower.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(io.BytesIO(file_bytes))
        
    elif nama_file_lower.endswith('.dbf'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".dbf") as file_temp:
            file_temp.write(file_bytes)
            jalur_temp = file_temp.name
        df = _baca_file_dbf(jalur_temp)
        os.remove(jalur_temp)
        
    if df is not None:
        df = optimalkan_memori_dataframe(df)
        
    return df

def unggah_dan_baca_file(file_unggahan, label_file="File"):
    """Fungsi utama yang dipanggil oleh antarmuka Streamlit."""
    with st.spinner(f"Membaca & Mengoptimalkan Memori {label_file} ('{file_unggahan.name}')..."):
        file_bytes = file_unggahan.getvalue()
        return baca_file_tersimpan(file_bytes, file_unggahan.name)