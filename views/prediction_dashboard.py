import streamlit as st
import plotly.graph_objects as go

def show_prediction_dashboard(controller):
    """Tampilkan dashboard prediksi banjir real-time dengan tema hitam"""
    
    st.markdown("""
    <style>
    .risk-card {
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
        color: white;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .risk-low { 
        background: linear-gradient(135deg, #00b09b, #96c93d);
        border: 1px solid #00b09b;
    }
    .risk-medium { 
        background: linear-gradient(135deg, #f8b500, #f8a500);
        border: 1px solid #f8b500;
    }
    .risk-high { 
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        border: 1px solid #ff416c;
    }
    .data-card {
        background: linear-gradient(145deg, #1a1a1a, #222222);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00a8ff;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        color: #dddddd;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Ambil data real-time
    with st.spinner("🔄 Mengambil data real-time dari BBWS Bengawan Solo..."):
        predictions = controller.get_comprehensive_data()
    
    # STATUS RISIKO OVERALL
    overall_status, status_color = controller.get_overall_risk_status(predictions)
    
    status_class = "low" if overall_status == "RENDAH" else "medium" if overall_status == "MENENGAH" else "high"
    
    st.markdown(f"""
    <div class="risk-card risk-{status_class}">
        <h2 style="margin:0; font-size: 1.8em;">STATUS RISIKO BANJIR: {overall_status}</h2>
        <p style="margin:10px 0 0 0; font-size: 1.1em; opacity: 0.9;">Berdasarkan data real-time BBWS Bengawan Solo</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # DATA REAL-TIME TERBARU
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.subheader("📊 DATA REAL-TIME TERBARU")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        latest_water = predictions[0]['water_level_mdpl'] if predictions else 0
        st.metric("🌊 Tinggi Air Terkini", f"{latest_water} mdpl", "BBWS Bengawan Solo")
    
    with col2:
        latest_rainfall = predictions[0]['rainfall_mm'] if predictions else 0
        st.metric("🌧️ Curah Hujan Terkini", f"{latest_rainfall} mm", "BBWS Bengawan Solo")
    
    with col3:
        update_time = predictions[0]['last_update'] if predictions else "N/A"
        st.metric("🕐 Update Terakhir", update_time, "Real-time")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # DETAIL LOKASI
    st.subheader("📍 DETAIL PER LOKASI")
    
    for pred in predictions:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        
        with col1:
            st.write(f"**{pred['location']}**")
            st.caption(f"🕐 Update: {pred['last_update']} | 📍 Sumber: {pred['source']}")
        
        with col2:
            st.metric("💧 Tinggi Air", f"{pred['water_level_mdpl']} mdpl")
        
        with col3:
            ann_color = "🟢" if pred['ann_status'] == "RENDAH" else "🟡" if pred['ann_status'] == "MENENGAH" else "🔴"
            st.write(f"**🤖 AI:** {ann_color} {pred['ann_status']}")
            st.caption(f"Risk: {pred['ann_risk']:.3f}")
        
        with col4:
            gumbel_color = "🟢" if pred['gumbel_status'] == "RENDAH" else "🟡" if pred['gumbel_status'] == "MENENGAH" else "🔴"
            st.write(f"**📈 Stat:** {gumbel_color} {pred['gumbel_status']}")
            st.caption(f"Risk: {pred['gumbel_risk']:.3f}")
        
        with st.expander("🔍 Lihat Detail Prediksi"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**🤖 Neural Network:**")
                st.write(f"- ⚠️ Risk Level: **{pred['ann_risk']:.3f}**")
                st.write(f"- 📊 Status: **{pred['ann_status']}**")
                st.write(f"- 💬 Pesan: {pred['ann_message']}")
            
            with col_b:
                st.markdown("**📈 Distribusi Gumbel:**")
                st.write(f"- ⚠️ Risk Level: **{pred['gumbel_risk']:.3f}**")
                st.write(f"- 📊 Status: **{pred['gumbel_status']}**")
                st.write(f"- 💬 Pesan: {pred['gumbel_message']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # REKOMENDASI
    show_recommendations(overall_status)

def show_recommendations(risk_status):
    """Tampilkan rekomendasi berdasarkan status risiko"""
    st.subheader("💡 REKOMENDASI & TINDAKAN")
    
    if risk_status == "RENDAH":
        st.markdown("""
        <div class="data-card" style="border-left-color: #00b09b;">
        <h3 style="color: #00b09b;">✅ KONDISI AMAN</h3>
        <ul style="color: #dddddd;">
            <li>🔍 Tetap pantau perkembangan cuaca</li>
            <li>💧 Pastikan saluran air di sekitar rumah lancar</li>
            <li>📄 Siapkan dokumen penting di tempat aman</li>
            <li>📱 Download aplikasi peringatan dini banjir</li>
            <li>📞 Simpan nomor darurat: 085156959561</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    elif risk_status == "MENENGAH":
        st.markdown("""
        <div class="data-card" style="border-left-color: #f8b500;">
        <h3 style="color: #f8b500;">🟡 STATUS SIAGA</h3>
        <ul style="color: #dddddd;">
            <li>⚠️ Waspada terhadap hujan deras</li>
            <li>🚫 Hindari daerah rendah dan tepi sungai</li>
            <li>🎒 Siapkan tas darurat berisi dokumen penting</li>
            <li>📡 Pantau informasi dari pihak berwenang</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="data-card" style="border-left-color: #ff416c;">
        <h3 style="color: #ff416c;">🔴 STATUS BAHAYA</h3>
        <ul style="color: #dddddd;">
            <li>🚨 Segera evakuasi ke tempat yang lebih tinggi</li>
            <li>🔌 Matikan listrik dan gas</li>
            <li>🚷 Jangan berjalan di arus banjir</li>
            <li>📞 Hubungi nomor darurat: 085156959561</li>
            <li>👥 Ikuti instruksi dari petugas</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)