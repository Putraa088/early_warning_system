import streamlit as st
from model_ann import predict_flood_ann_with_temp_range, get_ann_parameters

def show_ai_analysis():
    """Display AI/Neural Network analysis with high contrast"""
    
    # 1. Introduction with high contrast
    st.markdown("""
    <div class="card">
        <h2> Bagaimana AI Memprediksi Banjir?</h2>
        <div class="quote-box">
            <h3>"AI belajar dari data banjir sebelumnya seperti manusia belajar dari pengalaman"</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3> PROSES BELAJAR AI</h3>
            <p style="font-weight: 500; color: #475569;">
                1. <strong>Belajar dari Sejarah</strong>
                <br>• Data banjir 5 tahun terakhir
                <br>• Pola curah hujan vs kejadian banjir
                <br>• Relationship antara variabel
            </p>
            <p style="font-weight: 500; color: #475569;">
                2. <strong>Mengenal Pola</strong>
                <br>• Jika hujan X mm + air Y mdpl → risiko Z
                <br>• Deteksi pola berulang
                <br>• Belajar dari kesalahan prediksi sebelumnya
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3> KEMAMPUAN PREDIKSI</h3>
            <p style="font-weight: 500; color: #475569;">
                3. <strong>Memberi Peringatan</strong>
                <br>• Sistem otomatis memberi alert
                <br>• Rekomendasi tindakan
                <br>• Estimasi tingkat risiko
            </p>
            <p style="font-weight: 500; color: #475569;">
                4. <strong>Terus Meningkat</strong>
                <br>• Semakin banyak data, semakin akurat
                <br>• Update model secara berkala
                <br>• Belajar dari pola baru
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Info box with high contrast
    st.markdown("""
    <div class="info-box">
        <h4> CONTOH SEDERHANA</h4>
        <p style="font-weight: 500; color: #475569;">
            "Seperti kita tahu, jika langit gelap + angin kencang → kemungkinan hujan deras. 
            AI belajar pola serupa dari data historis banjir!"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rest of the existing code remains the same...
    # [Keep the existing technical details and demo code here]