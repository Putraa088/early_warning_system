import streamlit as st
import pandas as pd
from datetime import datetime
import os

def show_current_month_reports(controller):
    """Display current month's reports - TERBARU DI ATAS"""
    
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
    
    # Get today's reports (sudah terurut dari terbaru)
    reports = controller.get_today_reports()
    
    if not reports:
        st.info("Tidak ada laporan banjir untuk hari ini.")
        return
    
    st.markdown("---")
    
    # Header dengan informasi urutan
    st.markdown(f"### Daftar Laporan")
    
    # Display reports (sudah terurut dari terbaru)
    for i, report in enumerate(reports, 1):
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 1, 2])
        
        with col1:
            st.write(f"**{i}. {report['address']}**")
        
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
                if st.button("Lihat", key=f"view_{i}", use_container_width=True):
                    with st.expander(f"Foto - {report['address']}"):
                        if os.path.exists(report['photo_path']):
                            st.image(report['photo_path'], use_column_width=True)
                        else:
                            st.warning("Foto tidak ditemukan")
            else:
                st.write("Tidak ada")
        
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
