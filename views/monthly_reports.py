import streamlit as st
import pandas as pd
import os
from datetime import datetime

def show_monthly_reports_summary(controller):
    """Display monthly reports summary dengan struktur baru"""
    
    st.markdown("""
    <style>
    .time-badge {
        background: rgba(0, 168, 255, 0.15);
        color: #00a8ff;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    reports = controller.get_month_reports()
    
    if not reports:
        st.info(" Tidak ada laporan banjir untuk bulan ini.")
        return
    
    current_month = datetime.now().strftime('%B %Y')
    total_reports = len(reports)
    
    today = datetime.now().strftime('%Y-%m-%d')
    today_reports = [r for r in reports if r.get('report_date') == today]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Laporan", total_reports)
    with col2:
        st.metric("Laporan Hari Ini", len(today_reports))
    with col3:
        unique_reporters = len(set(r.get('Nama Pelapor', '') for r in reports))
        st.metric("Jumlah Pelapor", unique_reporters)
    with col4:
        locations = len(set(r.get('Alamat', '') for r in reports))
        st.metric("Lokasi Berbeda", locations)
    
    st.markdown("---")
    
    st.markdown(f"###  Daftar Laporan Bulan {current_month}")
    
    for i, report in enumerate(reports, 1):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 1])
            
            with col1:
                address_text = f"**{i}. {report.get('Alamat', 'N/A')}**"
                if report.get('report_date') == today:
                    st.markdown(f"{address_text} ", unsafe_allow_html=True)
                else:
                    st.markdown(address_text, unsafe_allow_html=True)
                
                time_display = format_time(report.get('report_time', ''))
                if time_display:
                    st.markdown(f'<span class="time-badge"> {time_display}</span>', unsafe_allow_html=True)
            
            with col2:
                st.write(f"**{report.get('Tinggi Banjir', 'N/A')}**")
            
            with col3:
                date_display = format_date_full(report.get('report_date', ''))
                st.write(date_display)
            
            with col4:
                st.write(report.get('Nama Pelapor', 'N/A'))
            
            with col5:
                if report.get('Photo URL') and os.path.exists(report['Photo URL']):
                    if st.button("Lihat", key=f"view_monthly_{report['id']}", help="Lihat foto"):
                        with st.expander(f"Foto - {report.get('Alamat', 'N/A')}"):
                            try:
                                st.image(report['Photo URL'], use_column_width=True)
                            except:
                                st.warning("Foto tidak dapat ditampilkan")
                else:
                    st.write("📭")
        
        if i < total_reports:
            st.divider()

def format_date_full(date_string):

    try:
        if not date_string:
            return "N/A"
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        day_name = days[date_obj.weekday()]
        return f"{day_name}, {date_obj.strftime('%d/%m/%Y')}"
    except:
        return date_string

def format_time(time_string):

    try:
        if time_string and len(time_string) >= 5:
            return time_string[:5]
        return ""
    except:
        return ""


