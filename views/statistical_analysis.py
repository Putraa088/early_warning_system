import streamlit as st
from gumbel_distribution import predict_flood_gumbel
import math

def show_statistical_analysis():
    """Display Gumbel Distribution analysis with high contrast"""
    
    # 1. Introduction with high contrast
    st.markdown("""
    <div class="card">
        <h2> Memahami Konsep Periode Ulang</h2>
        <div class="quote-box">
            <h3>"Seperti memperkirakan kapan banjir besar akan terulang berdasarkan pola sejarah"</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 20px;">
            <h4 style="color: #2563eb;"> BANJIR 5-TAHUNAN</h4>
            <p style="font-weight: 500; color: #475569;">
                Terjadi setiap 5 tahun sekali
                <br><strong>Risiko:</strong> SEDANG
                <br>Dalam 5 tahun mendatang, kemungkinan terjadi 63.2%
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 20px;">
            <h4 style="color: #2563eb;"> BANJIR 10-TAHUNAN</h4>
            <p style="font-weight: 500; color: #475569;">
                Lebih besar, lebih jarang
                <br><strong>Risiko:</strong> TINGGI saat mendekati periode
                <br>Dalam 10 tahun mendatang, kemungkinan terjadi 86.5%
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 20px;">
            <h4 style="color: #2563eb;"> BANJIR 50-TAHUNAN</h4>
            <p style="font-weight: 500; color: #475569;">
                Sangat besar, sangat jarang
                <br><strong>Risiko:</strong> SANGAT TINGGI
                <br>Butuh persiapan ekstra dan infrastruktur khusus
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Info box with high contrast
    st.markdown("""
    <div class="info-box">
        <h4> BAGAIMANA MEMAHAMINYA?</h4>
        <p style="font-weight: 500; color: #475569;">
            "Seperti mengetahui bahwa setiap 5 tahun biasanya ada badai besar di daerah kita. 
            Distribusi Gumbel membantu memperkirakan kemungkinan dan waktu kejadian ekstrem tersebut."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rest of the existing code remains the same...
    # [Keep the existing technical details and demo code here]