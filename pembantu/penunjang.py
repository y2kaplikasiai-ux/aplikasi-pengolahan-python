from pengaturan.konfigurasi import (
    BATAS_RELIABILITAS_TINGGI,
    BATAS_RELIABILITAS_SEDANG
)

def format_angka(nilai, jumlah_desimal=2):
    """Format angka float menjadi string dengan desimal terformat."""
    try:
        return f"{float(nilai):.{jumlah_desimal}f}"
    except (ValueError, TypeError):
        return str(nilai)

def dapatkan_status_reliabilitas(nilai_alpha):
    """Mengembalikan kelas CSS badge dan label status berdasarkan nilai Cronbach Alpha."""
    if nilai_alpha >= BATAS_RELIABILITAS_TINGGI:
        return "badge-good", "Sangat Baik"
    elif nilai_alpha >= BATAS_RELIABILITAS_SEDANG:
        return "badge-warning", "Cukup"
    else:
        return "badge-danger", "Perlu Revisi"