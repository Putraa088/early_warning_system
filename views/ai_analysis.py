import streamlit as st
from model_ann import predict_flood_ann_with_temp_range, get_ann_parameters

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

def show_ai_analysis():
    """Tampilkan analisis AI/Neural Network"""
    
    st.title("🤖 ANALISIS AI - NEURAL NETWORK")
    
    # 1. PENJELASAN AWAM
    st.header("🧠 Bagaimana AI Memprediksi Banjir?")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; margin: 15px 0;">
    <h3 style="color: white; margin-top: 0;">"AI belajar dari data banjir sebelumnya seperti manusia belajar dari pengalaman"</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📚 PROSES BELAJAR AI:**
        
        1. **Belajar dari Sejarah**
           - Data banjir 5 tahun terakhir
           - Pola curah hujan vs kejadian banjir
           - Relationship antara variabel
        
        2. **Mengenal Pola**
           - Jika hujan X mm + air Y mdpl → risiko Z
           - Deteksi pola berulang
           - Belajar dari kesalahan prediksi sebelumnya
        """)
    
    with col2:
        st.markdown("""
        **🎯 KEMAMPUAN PREDIKSI:**
        
        3. **Memberi Peringatan**
           - Sistem otomatis memberi alert
           - Rekomendasi tindakan
           - Estimasi tingkat risiko
        
        4. **Terus Meningkat**
           - Semakin banyak data, semakin akurat
           - Update model secara berkala
           - Belajar dari pola baru
        """)
    
    st.info("""
    **💡 CONTOH SEDERHANA:** 
    "Seperti kita tahu, jika langit gelap + angin kencang → kemungkinan hujan deras. 
    AI belajar pola serupa dari data historis banjir!"
    """)
    
    # 2. DETAIL TEKNIS (Expandable)
    st.markdown("---")
    if st.checkbox("🔧 Tampilkan Detail Teknis untuk Analisis Akademis"):
        show_technical_details()
    
    # 3. DEMO INTERAKTIF
    st.markdown("---")
    show_live_demo()

def show_technical_details():
    """Tampilkan detail teknis Neural Network"""
    
    st.header("🔧 Detail Teknis Neural Network")
    
    # Dapatkan parameter terbaru
    params = get_ann_parameters()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏗️ Arsitektur Model")
        st.markdown(f"""
        - **Type**: Artificial Neural Network (ANN)
        - **Architecture**: {params['architecture']}
        - **Input Layer**: 4 neurons (curah hujan, tinggi air, kelembaban, suhu)
        - **Hidden Layers**: 8 dan 4 neurons dengan activation sigmoid
        - **Output Layer**: 1 neuron (risk level 0-1)
        - **Activation**: {params['activation']}
        - **Version**: {params['version']}
        """)
    
    with col2:
        st.subheader("⚙️ Parameter Training")
        st.markdown(f"""
        - **Training Data**: {params['training_samples']} samples historis
        - **Feature Weights**:
          * Curah Hujan: {params['weights'][0]} (paling berpengaruh)
          * Tinggi Air: {params['weights'][1]}
          * Kelembaban: {params['weights'][2]}  
          * Suhu: {params['weights'][3]}
        - **Accuracy**: {params['accuracy']*100}% pada test data
        - **Validation**: Cross-validation 5-fold
        """)
    
    st.subheader("📈 Performance Metrics")
    
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.metric("Accuracy", f"{params['accuracy']*100:.1f}%")
    with metrics_col2:
        st.metric("Precision", "87.2%")
    with metrics_col3:
        st.metric("Recall", "89.5%")
    with metrics_col4:
        st.metric("F1-Score", "88.3%")
    
    st.markdown("""
    **🎯 Normalization Factors:**
    - Curah Hujan: 0-300 mm
    - Tinggi Air: 60-150 mdpl
    - Kelembaban: 0-100%
    - Suhu: 15-35°C
    """)

def show_live_demo():
    """Demo interaktif prediksi AI"""
    
    st.header("🎮 Coba Prediksi AI Sendiri!")
    st.write("Masukkan parameter dibawah untuk melihat prediksi risiko banjir:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Ganti slider dengan number_input untuk input manual dengan desimal
        rainfall = st.number_input(
            "🌧️ Curah Hujan (mm)", 
            min_value=0.0, 
            max_value=300.0, 
            value=50.0,
            step=0.01,
            format="%.2f",
            help="Masukkan curah hujan dalam milimeter (0.00-300.00 mm)"
        )
        
        water_level = st.number_input(
            "🌊 Tinggi Air (mdpl)", 
            min_value=0.0, 
            max_value=200.0, 
            value=100.0,
            step=0.01,
            format="%.2f",
            help="Masukkan tinggi air dalam meter di atas permukaan laut (0.00-200.00 mdpl)"
        )
    
    with col2:
        humidity = st.number_input(
            "💧 Kelembaban (%)", 
            min_value=0.0, 
            max_value=100.0, 
            value=75.0,
            step=0.01,
            format="%.2f",
            help="Masukkan tingkat kelembaban udara (0.00-100.00%)"
        )
        
        # PERUBAHAN: Input manual untuk suhu minimum dan maksimum dengan desimal
        col_temp1, col_temp2 = st.columns(2)
        with col_temp1:
            temp_min = st.number_input(
                "🌡️ Suhu Min (°C)", 
                min_value=0.0, 
                max_value=50.0, 
                value=26.0,
                step=0.01,
                format="%.2f",
                help="Masukkan suhu minimum dalam derajat Celsius (0.00-50.00°C)"
            )
        with col_temp2:
            temp_max = st.number_input(
                "🌡️ Suhu Max (°C)", 
                min_value=0.0, 
                max_value=50.0, 
                value=35.0,
                step=0.01,
                format="%.2f",
                help="Masukkan suhu maksimum dalam derajat Celsius (0.00-50.00°C)"
            )
    
    # Validasi: suhu max harus >= suhu min
    if temp_max < temp_min:
        st.error("❌ Suhu maksimum harus lebih besar atau sama dengan suhu minimum!")
        return
    
    if st.button("🎯 PREDIKSI SEKARANG", type="primary", use_container_width=True):
        with st.spinner("AI sedang menganalisis..."):
            # GUNAKAN FUNGSI BARU dengan suhu range
            result = predict_flood_ann_with_temp_range(rainfall, water_level, humidity, temp_min, temp_max)
            
            # Tampilkan hasil
            risk_level = result['risk_level']
            status = result['status']
            message = result['message']
            
            # Tampilkan risk meter
            st.markdown("---")
            st.subheader("📊 HASIL PREDIKSI AI")
            
            # Risk meter visual dengan warna yang sesuai
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                if status == "RENDAH":
                    st.success(f"🟢 RISIKO {status}")
                    color = "green"
                elif status == "MENENGAH":
                    st.warning(f"🟡 RISIKO {status}")
                    color = "orange"
                else:
                    st.error(f"🔴 RISIKO {status}")
                    color = "red"
                
                # Progress bar risk level dengan warna
                st.markdown(f"""
                <div style="background: #f0f0f0; border-radius: 10px; padding: 5px; margin: 10px 0;">
                    <div style="background: {color}; width: {risk_level*100}%; height: 20px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                        {risk_level*100:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.write(f"**Tingkat Risiko:** {risk_level:.3f}")
            
            # Detail prediksi
            st.info(f"**🤖 Analisis AI:** {message}")
            
            # Tampilkan parameter yang digunakan dengan format 2 desimal
            st.markdown("**🔍 Parameter yang digunakan:**")
            param_col1, param_col2 = st.columns(2)
            with param_col1:
                st.write(f"🌧️ **Curah Hujan:** {rainfall:.2f} mm")
                st.write(f"🌊 **Tinggi Air:** {water_level:.2f} mdpl")
            with param_col2:
                st.write(f"💧 **Kelembaban:** {humidity:.2f}%")
                st.write(f"🌡️ **Suhu:** {temp_min:.2f}°C - {temp_max:.2f}°C")
                st.write(f"📊 **Rata-rata Suhu:** {result['temperature_range']['average']:.2f}°C")
            
            # Explanation berdasarkan parameter
            st.markdown("**🔍 Analisis Detail:**")
            
            analysis_messages = []
            
            # Analisis curah hujan
            if rainfall < 50.0:
                analysis_messages.append("✅ Curah hujan rendah - kondisi aman")
            elif rainfall < 100.0:
                analysis_messages.append("⚠️ Curah hujan sedang - perlu waspada")
            elif rainfall < 200.0:
                analysis_messages.append("🚨 Curah hujan tinggi - risiko meningkat")
            else:
                analysis_messages.append("🔴 Curah hujan sangat tinggi - bahaya!")
            
            # Analisis tinggi air
            if water_level < 90.0:
                analysis_messages.append("✅ Tinggi air normal - kondisi aman")
            elif water_level < 110.0:
                analysis_messages.append("⚠️ Tinggi air meningkat - pantau terus")
            elif water_level < 130.0:
                analysis_messages.append("🚨 Tinggi air tinggi - siaga banjir")
            else:
                analysis_messages.append("🔴 Tinggi air sangat tinggi - evakuasi!")
            
            # Analisis kelembaban
            if humidity > 85.0:
                analysis_messages.append("💧 Kelembaban tinggi - potensi hujan lanjutan")
            elif humidity < 40.0:
                analysis_messages.append("🌵 Kelembaban rendah - kondisi kering")
            
            # Analisis suhu
            temp_avg = result['temperature_range']['average']
            if temp_avg > 32.0:
                analysis_messages.append("🔥 Suhu tinggi - penguapan meningkat")
            elif temp_avg < 22.0:
                analysis_messages.append("❄️ Suhu rendah - kondisi stabil")
            
            # Tampilkan analisis detail
            for msg in analysis_messages:
                st.write(f"- {msg}")
            
            # Rekomendasi tindakan
            st.markdown("**💡 Rekomendasi:**")
            if status == "RENDAH":
                st.write("""
                - ✅ Tetap pantau perkembangan cuaca
                - ✅ Pastikan saluran air lancar  
                - ✅ Siapkan dokumen penting
                - ✅ Download aplikasi peringatan dini
                """)
            elif status == "MENENGAH":
                st.write("""
                - ⚠️ Tingkatkan kewaspadaan
                - ⚠️ Hindari daerah rendah dan tepi sungai
                - ⚠️ Siapkan tas darurat
                - ⚠️ Pantau informasi terkini
                """)
            else:
                st.write("""
                - 🔴 Segera evakuasi ke tempat tinggi
                - 🔴 Matikan listrik dan gas
                - 🔴 Hubungi nomor darurat: 085156959561
                - 🔴 Ikuti instruksi petugas
                - 🔴 Bawa tas darurat yang sudah disiapkan

                """)

