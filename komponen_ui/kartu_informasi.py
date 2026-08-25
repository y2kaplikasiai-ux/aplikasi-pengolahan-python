import streamlit as st
from pembantu.penunjang import dapatkan_status_reliabilitas

def tampilkan_kartu_ringkasan(mapel, jenjang, jumlah_peserta, nilai_alpha, jumlah_soal):
    """Menampilkan 4 kartu statistik utama di bagian atas dashboard."""
    badge_class, badge_label = dapatkan_status_reliabilitas(nilai_alpha)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">Mata Pelajaran</div>
                <div class="metric-value">{mapel}</div>
                <span class="metric-badge badge-good">{jenjang}</span>
            </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">Jumlah Peserta (N)</div>
                <div class="metric-value">{jumlah_peserta:,}</div>
                <span class="metric-badge badge-good">Siswa Sampel</span>
            </div>
        ''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">Reliabilitas (Alpha)</div>
                <div class="metric-value">{nilai_alpha}</div>
                <span class="metric-badge {badge_class}">{badge_label}</span>
            </div>
        ''', unsafe_allow_html=True)
    with c4:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">Jumlah Butir Soal</div>
                <div class="metric-value">{jumlah_soal}</div>
                <span class="metric-badge badge-good">Butir Evaluasi</span>
            </div>
        ''', unsafe_allow_html=True)