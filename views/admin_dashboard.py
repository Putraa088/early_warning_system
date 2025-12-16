import streamlit as st
import pandas as pd
from datetime import datetime

def show_admin_dashboard(flood_controller):
    """Admin dashboard untuk monitor data dari Google Sheets"""
    
    st.title("📊 Admin Dashboard")
    
    # Check if Google Sheets is available
    if not hasattr(flood_controller, 'sheets_model') or not flood_controller.sheets_model.client:
        st.warning("Google Sheets tidak terhubung. Dashboard terbatas.")
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Total reports
        reports = flood_controller.get_month_reports()
        st.metric("Total Laporan Bulan Ini", len(reports))
    
    with col2:
        # Google Sheets status
        if hasattr(flood_controller, 'sheets_model') and flood_controller.sheets_model.client:
            st.metric("Google Sheets", "✅ Terhubung")
        else:
            st.metric("Google Sheets", "❌ Offline")
    
    with col3:
        # Predictions count
        st.metric("Prediksi Hari Ini", "N/A")
    
    with col4:
        # System status
        st.metric("Status Sistem", "🟢 Online")
    
    st.markdown("---")
    
    # Google Sheets Data
    st.subheader("📈 Data dari Google Sheets")
    
    tab1, tab2, tab3 = st.tabs(["📋 Laporan", "📊 Prediksi", "📈 Statistik"])
    
    with tab1:
        if hasattr(flood_controller, 'sheets_model') and flood_controller.sheets_model.client:
            try:
                reports = flood_controller.sheets_model.get_recent_reports(limit=20)
                if reports:
                    df = pd.DataFrame(reports)
                    st.dataframe(df, use_container_width=True)
                    
                    # Export button
                    if st.button("📥 Export to CSV"):
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"flood_reports_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                else:
                    st.info("Belum ada data laporan di Google Sheets")
            except Exception as e:
                st.error(f"Error mengambil data: {e}")
        else:
            st.info("Google Sheets tidak tersedia")
    
    with tab2:
        if hasattr(flood_controller, 'sheets_model') and flood_controller.sheets_model.client:
            try:
                predictions = flood_controller.sheets_model.get_predictions(limit=20)
                if predictions:
                    df = pd.DataFrame(predictions)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("Belum ada data prediksi di Google Sheets")
            except Exception as e:
                st.error(f"Error mengambil prediksi: {e}")
    
    with tab3:
        if hasattr(flood_controller, 'sheets_model') and flood_controller.sheets_model.client:
            try:
                stats = flood_controller.sheets_model.get_statistics()
                if stats:
                    st.json(stats)
                    
                    # Update statistics button
                    if st.button("🔄 Update Statistics"):
                        with st.spinner("Updating statistics..."):
                            success = flood_controller.update_monthly_statistics()
                            if success:
                                st.success("Statistics updated!")
                                st.rerun()
                            else:
                                st.error("Failed to update statistics")
                else:
                    st.info("Belum ada statistik di Google Sheets")
            except Exception as e:
                st.error(f"Error mengambil statistik: {e}")
    
    # System Actions
    st.markdown("---")
    st.subheader("⚙️ System Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh All Data", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("📊 Generate Monthly Report", use_container_width=True):
            st.info("Fitur coming soon...")
    
    with col3:
        if st.button("🧹 Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache cleared!")
            st.rerun()
