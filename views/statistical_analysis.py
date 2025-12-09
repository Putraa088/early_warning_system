import streamlit as st
from gumbel_distribution import predict_flood_gumbel
import math

# Tambahkan di bagian atas fungsi show_ai_analysis() dan show_statistical_analysis()
st.markdown("""
<style>
.analysis-card {
    background: linear-gradient(145deg, #1a1a1a, #222222);
    padding: 20px;
    border-radius: 10px;
    margin: 15px 0;
    border: 1px solid #333333;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    color: #dddddd;
}
.tech-details {
    background: #2a2a2a;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #00a8ff;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

def show_statistical_analysis():
    """Tampilkan analisis Distribusi Gumbel"""
    
    st.title("📈 ANALISIS GUMBEL - DISTRIBUSI EKSTREM")
    
    # 1. ANALOGI PERIODE ULANG
    st.header("📅 Memahami Konsep Periode Ulang")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; margin: 15px 0;">
    <h3 style="color: white; margin-top: 0;">"Seperti memperkirakan kapan banjir besar akan terulang berdasarkan pola sejarah"</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 BANJIR 5-TAHUNAN**
        - Terjadi setiap 5 tahun sekali
        - **Risiko**: SEDANG
        - **Artinya**: Dalam 5 tahun mendatang, 
          kemungkinan terjadi 63.2%
        """)
    
    with col2:
        st.markdown("""
        **🎯 BANJIR 10-TAHUNAN**  
        - Lebih besar, lebih jarang
        - **Risiko**: TINGGI saat mendekati periode
        - **Artinya**: Dalam 10 tahun mendatang,
          kemungkinan terjadi 86.5%
        """)
    
    with col3:
        st.markdown("""
        **🎯 BANJIR 50-TAHUNAN**
        - Sangat besar, sangat jarang  
        - **Risiko**: SANGAT TINGGI
        - **Artinya**: Butuh persiapan ekstra
          dan infrastruktur khusus
        """)
    
    st.info("""
    **💡 BAGAIMANA MEMAHAMINYA?**
    "Seperti mengetahui bahwa setiap 5 tahun biasanya ada badai besar di daerah kita. 
    Distribusi Gumbel membantu memperkirakan kemungkinan dan waktu kejadian ekstrem tersebut."
    """)
    
    # 2. DETAIL DISTRIBUSI GUMBEL
    st.markdown("---")
    if st.checkbox("📊 Tampilkan Detail Distribusi Gumbel"):
        show_gumbel_technical()
    
    # 3. DEMO INTERAKTIF
    st.markdown("---")
    show_gumbel_demo()
    
    # 4. PERBANDINGAN METODE
    st.markdown("---")
    show_method_comparison()

def show_gumbel_technical():
    """Tampilkan detail teknis Distribusi Gumbel"""
    
    st.header("🔧 Detail Teknis Distribusi Gumbel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📐 Konsep Matematis")
        st.markdown("""
        **Distribusi Gumbel Type I**
        - **Digunakan untuk**: Analisis nilai ekstrem
        - **Aplikasi**: Banjir maksimum, gempa, angin topan
        - **Rumus CDF**: 
          ```
          F(x) = exp(-exp(-(x-μ)/β))
          ```
        - **Return Period**:
          ```
          T = 1 / (1 - F(x))
          ```
        """)
    
    with col2:
        st.subheader("⚙️ Parameter Model")
        st.markdown("""
        **Berdasarkan Data Historis:**
        - **μ (location)**: 85.0
        - **β (scale)**: 22.5
        - **Data Source**: BMKG 10 tahun
        - **Return Period**: 10 tahun
        - **Probability**: 0.6347
        
        **Interpretasi**:
        - μ: Nilai rata-rata kejadian ekstrem
        - β: Variabilitas kejadian ekstrem
        """)
    
    st.subheader("🎯 Aplikasi untuk Prediksi Banjir")
    st.markdown("""
    Distribusi Gumbel sangat efektif untuk:
    - **Memperkirakan** banjir maksimum yang mungkin terjadi
    - **Mendesain** infrastruktur (jalan, jembatan, bendungan)
    - **Menyusun** rencana tanggap darurat
    - **Menentukan** zona rawan banjir
    """)

def show_gumbel_demo():
    """Demo interaktif Distribusi Gumbel"""
    
    st.header("🎮 Coba Analisis Gumbel Sendiri!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # PERUBAHAN: Input manual dengan desimal untuk curah hujan
        rainfall = st.number_input(
            "🌧️ Curah Hujan untuk Analisis (mm)", 
            min_value=0.0, 
            max_value=300.0, 
            value=100.0,
            step=0.01,
            format="%.2f",
            help="Masukkan curah hujan dalam milimeter (0.00-300.00 mm)"
        )
        
        # PERUBAHAN: Periode ulang dengan pilihan terbatas
        return_period = st.selectbox(
            "📅 Periode Ulang (Return Period)",
            [5, 10, 15, 25, 50],
            index=1,
            help="Pilih periode ulang untuk analisis"
        )
    
    with col2:
        st.markdown("**📊 Parameter Gumbel:**")
        st.write(f"- **μ (location)**: 85.0")
        st.write(f"- **β (scale)**: 22.5")
        st.write(f"- **Data Source**: BMKG Historical")
        
        st.markdown("**💡 Info:**")
        st.write("Parameter diatas berdasarkan analisis data historis 10 tahun dari BMKG")
    
    if st.button("📈 ANALISIS DENGAN GUMBEL", type="primary", use_container_width=True):
        with st.spinner("Menganalisis dengan Distribusi Gumbel..."):
            result = predict_flood_gumbel(rainfall, return_period)
            
            # Tampilkan hasil
            st.markdown("---")
            st.subheader("📊 HASIL ANALISIS GUMBEL")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                risk_level = result['risk_level']
                if result['status'] == "RENDAH":
                    st.success(f"🟢 {result['status']}")
                elif result['status'] == "MENENGAH":
                    st.warning(f"🟡 {result['status']}")
                else:
                    st.error(f"🔴 {result['status']}")
                
                st.metric("Risk Level", f"{risk_level:.3f}")
            
            with col_b:
                probability = result['probability']
                st.metric("Probability", f"{probability:.1%}")
                st.progress(probability)
            
            with col_c:
                st.metric("Return Period", f"{return_period} tahun")
                st.write(f"μ: {result['parameters_used']['mu_location']}")
                st.write(f"β: {result['parameters_used']['beta_scale']}")
            
            # Penjelasan
            st.info(f"**📈 Interpretasi:** {result['message']}")
            
            # Additional explanation
            st.markdown("**🔍 Artinya Untuk Anda:**")
            if result['status'] == "RENDAH":
                st.write("Berdasarkan pola historis, kondisi saat ini relatif aman dari banjir besar.")
            elif result['status'] == "MENENGAH":
                st.write("Peringatan: mendekati periode ulang banjir menengah. Tingkatkan kewaspadaan.")
            else:
                st.write("Peringatan tinggi: parameter menunjukkan kemungkinan banjir besar dalam periode ini.")
            
            # Tampilkan parameter yang digunakan dengan format desimal
            st.markdown("**🔍 Parameter yang digunakan:**")
            param_col1, param_col2 = st.columns(2)
            with param_col1:
                st.write(f"🌧️ **Curah Hujan:** {rainfall:.2f} mm")
                st.write(f"📅 **Periode Ulang:** {return_period} tahun")
            with param_col2:
                st.write(f"📐 **μ (location):** {result['parameters_used']['mu_location']}")
                st.write(f"📏 **β (scale):** {result['parameters_used']['beta_scale']}")

def show_method_comparison():
    """Tampilkan perbandingan metode ANN vs Gumbel"""
    
    st.header("🔄 Perbandingan Metode Prediksi")
    
    st.markdown("""
    | Metode | Kelebihan | Kekurangan | Aplikasi Terbaik |
    |--------|-----------|------------|------------------|
    | **🤖 Neural Network** | - Belajar pola kompleks<br>- Adaptif dengan data baru<br>- Akurasi tinggi | - Butuh data training banyak<br>- Complex interpretation<br>- Computational cost | Prediksi real-time, pattern recognition |
    | **📈 Distribusi Gumbel** | - Statistically sound<br>- Easy to interpret<br>- Minimal data requirements | - Assume distribution<br>- Less adaptive<br>- Limited to extremes | Desain infrastruktur, risk assessment |
    """)
    
    st.success("""
    **🎯 KESIMPULAN:** 
    **Kombinasi kedua metode** memberikan prediksi yang lebih robust. 
    ANN untuk akurasi real-time, Gumbel untuk validasi statistik dan perencanaan jangka panjang.
    """)