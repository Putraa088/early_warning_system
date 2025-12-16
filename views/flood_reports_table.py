import streamlit as st
import pandas as pd
from datetime import datetime
import os

def show_current_month_reports(controller):
    """Display current month's reports"""
    
    st.markdown("""
    <style>
    .report-card {
        background: linear-gradient(145deg, #1a1a1a, #222222);
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border: 1px solid #333333;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get today's reports
    reports = controller.get_today_reports()
    
    if not reports:
        st.info("📭 Tidak ada laporan banjir untuk hari ini.")
        return
    
    st.markdown("---")
    
    # Header
    st.markdown(f"### 📋 Daftar Laporan Hari Ini ({len(reports)} laporan)")
    
    # Display reports
    for i, report in enumerate(reports, 1):
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 1, 2])
        
        with col1:
            st.write(f"**{i}. {report['address']}**")
            if 'timestamp' in report:
                st.caption(f"ID: {report['id']} | {report['timestamp'][11:19]}")
        
        with col2:
            st.write(f"**{report['flood_height']}**")
        
        with col3:
            date_display = format_date(report.get('report_date', ''))
            st.write(date_display)
        
        with col4:
            # Format time jika ada
            time_display = report.get('report_time', '')[:5] if report.get('report_time') and len(report.get('report_time', '')) >= 5 else "N/A"
            st.write(time_display)
        
        with col5:
            st.write(report['reporter_name'])
        
        with col6:
            if report.get('photo_path') and os.path.exists(report['photo_path']):
                if st.button("📷 Lihat", key=f"view_{report['id']}", use_container_width=True):
                    with st.expander(f"Foto - {report['address']}"):
                        try:
                            st.image(report['photo_path'], use_column_width=True)
                        except Exception as e:
                            st.warning(f"Gagal menampilkan foto: {e}")
            else:
                st.write("📭 Tidak ada")
        
        if i < len(reports):
            st.divider()
    
    # Summary
    with st.expander("📊 Statistik Hari Ini"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Laporan", len(reports))
        with col2:
            unique_locations = len(set(r['address'] for r in reports))
            st.metric("Lokasi Berbeda", unique_locations)
        with col3:
            reporters = len(set(r['reporter_name'] for r in reports))
            st.metric("Pelapor Berbeda", reporters)

def format_date(date_string):
    """Format date untuk display"""
    try:
        if not date_string:
            return "N/A"
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        day_name = days[date_obj.weekday()]
        return f"{day_name}, {date_obj.strftime('%d/%m/%y')}"
    except:
        return date_string