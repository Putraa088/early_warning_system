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
        st.info("📊 Tidak ada laporan banjir untuk hari ini.")
        return
    
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Laporan", len(reports))
    with col2:
        st.metric("Dengan Foto", sum(1 for r in reports if r['photo_path']))
    with col3:
        st.metric("Tanpa Foto", sum(1 for r in reports if not r['photo_path']))
    with col4:
        unique_areas = len(set(r['address'] for r in reports))
        st.metric("Daerah Terdampak", unique_areas)
    
    st.markdown("---")
    
    # Display reports
    for i, report in enumerate(reports, 1):
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 1, 2])
        
        with col1:
            st.write(f"**{i}.** {report['address']}")
        with col2:
            st.write(report['flood_height'])
        with col3:
            st.write(format_date(report['report_date']))
        with col4:
            st.write(report['report_time'])
        with col5:
            st.write(report['reporter_name'])
        with col6:
            if report['photo_path']:
                if st.button("👁️ Lihat", key=f"view_{i}", use_container_width=True):
                    with st.expander(f"Foto - {report['address']}"):
                        if os.path.exists(report['photo_path']):
                            st.image(report['photo_path'], use_column_width=True)
                        else:
                            st.warning("Foto tidak ditemukan")
            else:
                st.write("❌")
        
        if i < len(reports):
            st.divider()
    
    st.markdown('</div>', unsafe_allow_html=True)

def format_date(date_string):
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        day_name = days[date_obj.weekday()]
        return f"{day_name}, {date_obj.strftime('%d/%m/%y')}"
    except:
        return date_string