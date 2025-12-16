import streamlit as st
import pandas as pd

def show_prediction_dashboard(controller):
    """Display flood prediction dashboard with clean design"""
    
    # Get predictions
    with st.spinner("Memuat data prediksi..."):
        predictions = controller.get_comprehensive_data()
    
    if not predictions:
        st.warning("Data prediksi tidak tersedia saat ini.")
        return
    
    # Overall Risk Status
    overall_status, _ = controller.get_overall_risk_status(predictions)
    
    # Status color
    if overall_status == "RENDAH":
        status_color = "success"
        status_icon = "✅"
    elif overall_status == "MENENGAH":
        status_color = "warning"
        status_icon = "⚠️"
    else:
        status_color = "error"
        status_icon = "🚨"
    
    # Display overall status
    st.markdown(f"""
    <div style="background: {'#10b981' if overall_status == 'RENDAH' else '#f59e0b' if overall_status == 'MENENGAH' else '#ef4444'}; 
                color: white; padding: 25px; border-radius: 10px; margin-bottom: 25px; text-align: center;">
        <h2 style="color: white; margin: 0;">Status Risiko Banjir: {overall_status}</h2>
        <p style="margin: 10px 0 0 0; opacity: 0.9;">Berdasarkan data real-time terkini</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    st.markdown("### Data Real-time")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        latest_water = predictions[0]['water_level_mdpl'] if predictions else 0
        st.metric(
            "Tinggi Air Terkini",
            f"{latest_water} mdpl",
            "Level air"
        )
    
    with col2:
        latest_rainfall = predictions[0]['rainfall_mm'] if predictions else 0
        st.metric(
            "Curah Hujan",
            f"{latest_rainfall} mm",
            "Per jam"
        )
    
    with col3:
        update_time = predictions[0]['last_update'] if predictions else "N/A"
        st.metric(
            "Update Terakhir",
            update_time
        )
    
    st.markdown("---")
    
    # Location details
    st.markdown("### Detail per Lokasi")
    
    for pred in predictions:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            
            with col1:
                st.markdown(f"**{pred['location']}**")
                st.caption(f"Sumber: {pred['source']} | Update: {pred['last_update']}")
            
            with col2:
                st.markdown(f"**Tinggi Air:** {pred['water_level_mdpl']} mdpl")
                status_text = f"**Status:** {pred['water_status']}"
                if pred['water_status'] == "RENDAH":
                    st.success(status_text)
                elif pred['water_status'] == "MENENGAH":
                    st.warning(status_text)
                else:
                    st.error(status_text)
            
            with col3:
                st.markdown("**Prediksi AI**")
                risk = pred['ann_risk']
                status = pred['ann_status']
                st.progress(risk)
                st.markdown(f"{status} ({risk:.1%})")
            
            with col4:
                st.markdown("**Analisis Statistik**")
                risk = pred['gumbel_risk']
                status = pred['gumbel_status']
                st.progress(risk)
                st.markdown(f"{status} ({risk:.1%})")
            
            with st.expander("Detail Prediksi"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("** Neural Network**")
                    st.write(f"- Status: {pred['ann_status']}")
                    st.write(f"- Risk Level: {pred['ann_risk']:.3f}")
                    st.write(f"- Analisis: {pred['ann_message']}")
                
                with col_b:
                    st.markdown("** Distribusi Gumbel**")
                    st.write(f"- Status: {pred['gumbel_status']}")
                    st.write(f"- Risk Level: {pred['gumbel_risk']:.3f}")
                    st.write(f"- Analisis: {pred['gumbel_message']}")
            
            st.markdown("---")
            
