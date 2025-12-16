import streamlit as st
import pandas as pd
import os
from datetime import datetime

def show_monthly_reports_summary(controller):
    """Display monthly reports summary"""
    
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
    
    # Get reports
    reports = controller.get_month_reports()
    
    if not reports:
        st.info("📭 Tidak ada laporan banjir untuk bulan ini.")
        return
    
    # Daftar laporan
    current_month = datetime.now().strftime('%B %Y')
    total_reports = len(reports)
    
    # Filter untuk mendapatkan laporan hari ini
    today = datetime.now().strftime('%Y-%m-%d')
    today_reports = [r for r in reports if r['report_date'] == today]
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Laporan", total_reports)
    with col2:
        st.metric("Laporan Hari Ini", len(today_reports))
    with col3:
        unique_reporters = len(set(r['reporter_name'] for r in reports))
        st.metric("Jumlah Pelapor", unique_reporters)
    with col4:
        locations = len(set(r['address'] for r in reports))
        st.metric("Lokasi Berbeda", locations)
    
    st.markdown("---")
    
    st.markdown(f"### 📅 Daftar Laporan Bulan {current_month}")
    
    # Tampilkan laporan
    for i, report in enumerate(reports, 1):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 1])
            
            with col1:
                # Alamat dengan badge jika laporan hari ini
                address_text = f"**{i}. {report['address']}**"
                if report['report_date'] == today:
                    st.markdown(f"{address_text} 🆕", unsafe_allow_html=True)
                else:
                    st.markdown(address_text, unsafe_allow_html=True)
                
                # Waktu
                time_display = format_time(report.get('report_time', ''))
                if time_display:
                    st.markdown(f'<span class="time-badge">🕐 {time_display}</span>', unsafe_allow_html=True)
            
            with col2:
                st.write(f"**{report['flood_height']}**")
            
            with col3:
                date_display = format_date_full(report.get('report_date', ''))
                st.write(date_display)
            
            with col4:
                st.write(report['reporter_name'])
            
            with col5:
                if report.get('photo_path') and os.path.exists(report['photo_path']):
                    if st.button("📷", key=f"view_monthly_{report['id']}", help="Lihat foto"):
                        with st.expander(f"Foto - {report['address']}"):
                            try:
                                st.image(report['photo_path'], use_column_width=True)
                            except:
                                st.warning("Foto tidak dapat ditampilkan")
                else:
                    st.write("📭")
        
        # Divider antar laporan
        if i < total_reports:
            st.divider()

def format_date_full(date_string):
    """Format date untuk display lengkap"""
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
    """Format time untuk display"""
    try:
        if time_string and len(time_string) >= 5:
            return time_string[:5]
        return ""
    except:
        return ""