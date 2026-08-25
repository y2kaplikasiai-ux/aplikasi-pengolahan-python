import plotly.express as px

def buat_scatter_plot(df_hasil_item):
    """Membuat grafik scatter plot untuk melihat kuadran kesukaran vs daya beda (Full Width)."""
    fig = px.scatter(
        df_hasil_item,
        x="Tingkat Kesukaran (p)",
        y="Daya Beda (r_pbi)",
        color="Kategori Daya Beda",
        hover_name="No Soal",
        hover_data=["Kunci", "Kategori Kesukaran"],
        color_discrete_map={
            "Sangat Baik": "#10B981",
            "Baik": "#3B82F6",
            "Cukup (Perlu Revisi)": "#F59E0B",
            "Buruk (Dibuang/Revisi Total)": "#EF4444"
        },
        title="Scatter Plot: Tingkat Kesukaran vs Daya Beda Soal"
    )
    fig.add_hline(y=0.30, line_dash="dash", line_color="gray", annotation_text="Batas Daya Beda Baik (0.30)")
    fig.add_vline(x=0.30, line_dash="dot", line_color="red", annotation_text="Sukar")
    fig.add_vline(x=0.70, line_dash="dot", line_color="green", annotation_text="Mudah")
    
    # Menghilangkan area kosong kanan & melebarkan grafik penuh
    fig.update_layout(
        template="plotly_white",
        height=500,
        autosize=True,
        margin=dict(l=30, r=30, t=60, b=40),
        xaxis=dict(range=[-0.05, 1.05], dtick=0.1),  # Memaksa sumbu X membentang penuh 0-1
        legend=dict(
            orientation="h",       # Legend dipindahkan ke atas secara horizontal
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

def buat_bar_chart(df_hasil_item):
    """Membuat grafik batang tingkat kesukaran per butir soal."""
    fig = px.bar(
        df_hasil_item,
        x="No Soal",
        y="Tingkat Kesukaran (p)",
        color="Kategori Kesukaran",
        color_discrete_map={"Mudah": "#6EE7B7", "Sedang": "#60A5FA", "Sukar": "#F87171"},
        title="Tingkat Kesukaran (p) Per Butir Soal"
    )
    fig.update_layout(
        template="plotly_white",
        height=400,
        autosize=True,
        margin=dict(l=30, r=30, t=50, b=40),
        xaxis_tickangle=-45
    )
    return fig

def buat_histogram_skor(df_biner):
    """Membuat histogram distribusi skor peserta dengan presisi bin 1 poin."""
    max_skor = int(df_biner['Total_Skor'].max()) if len(df_biner) > 0 else 30

    fig = px.histogram(
        df_biner,
        x="Total_Skor",
        title="Histogram Distribusi Skor Peserta (Presisi 1 Poin)",
        color_discrete_sequence=["#6366F1"]
    )
    fig.update_traces(xbins=dict(start=-0.5, end=max_skor + 0.5, size=1))
    fig.update_layout(
        template="plotly_white",
        height=450,
        autosize=True,
        margin=dict(l=30, r=30, t=50, b=40),
        xaxis=dict(
            title="Total Skor Siswa",
            tick0=0,
            dtick=1,
            range=[-0.5, max_skor + 0.5]
        ),
        yaxis_title="Frekuensi (Jumlah Siswa)",
        bargap=0.15
    )
    return fig