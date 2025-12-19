import streamlit as st
import pandas as pd
import os
from datetime import datetime

def show_current_month_reports(controller):
    """Display current month's reports dengan error handling"""
    
    st.markdown("""
    <style>
    .report-card {
        background: linear-gradient(145deg, #1a1a1a, #222222);
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border: 1px solid #333333;
    }
    .photo-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 0.9rem;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)
    
    try:
        # Get today's reports dari controller
        reports = controller.get_today_reports()
    except AttributeError as e:
        st.error(f"❌ Error: Controller tidak memiliki method get_today_reports()")
        st.info("⚠️ Silakan periksa kode controller Anda.")
        return
    except Exception as e:
        st.error(f"❌ Error mendapatkan data: {e}")
        return
    
    if not reports:
        st.info("📭 Tidak ada laporan banjir untuk hari ini.")
        return
    
    st.markdown("---")
    
    # Header
    st.markdown(f"### 📋 Daftar Laporan Hari Ini ({len(reports)} laporan)")
    
    # Display reports
    for i, report in enumerate(reports, 1):
        with st.container():
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            
            col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 1, 2])
            
            with col1:
                # Alamat
                address = report.get('Alamat', report.get('alamat', 'N/A'))
                st.write(f"**{i}. {address}**")
                
                # ID dan waktu
                report_id = report.get('id', 'N/A')
                timestamp = report.get('Timestamp', '')
                if timestamp:
                    st.caption(f"ID: {report_id} | {timestamp[11:19]}")
                else:
                    st.caption(f"ID: {report_id}")
            
            with col2:
                # Tinggi Banjir
                flood_height = report.get('Tinggi Banjir', report.get('tinggi_banjir', 'N/A'))
                st.write(f"**{flood_height}**")
            
            with col3:
                # Tanggal
                date_display = format_date(report.get('report_date', ''))
                st.write(date_display)
            
            with col4:
                # Waktu
                time_display = format_time(report.get('report_time', ''))
                st.write(time_display)
            
            with col5:
                # Nama Pelapor
                reporter_name = report.get('Nama Pelapor', report.get('nama_pelapor', 'N/A'))
                st.write(reporter_name)
            
            with col6:
                # Foto
                photo_url = report.get('Photo URL', report.get('photo_url', ''))
                
                if photo_url:
                    # Check jika foto ada
                    if os.path.exists(str(photo_url)):
                        if st.button("👁️ Lihat", key=f"view_{report_id}", use_container_width=True):
                            with st.expander(f"📷 Foto - {address[:30]}...", expanded=True):
                                try:
                                    st.image(photo_url, use_column_width=True)
                                except Exception as e:
                                    st.warning(f"Gagal menampilkan foto: {e}")
                    elif 'drive.google.com' in str(photo_url):
                        # Google Drive URL
                        if st.button("🔗 Buka", key=f"drive_{report_id}", use_container_width=True):
                            st.markdown(f"[📎 Buka Foto di Google Drive]({photo_url})")
                    else:
                        st.write("📭 Tidak ada")
                else:
                    st.write("📭 Tidak ada")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Divider antar laporan
        if i < len(reports):
            st.divider()
    
    # Summary
    with st.expander("📊 Statistik Hari Ini", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Laporan", len(reports))
        with col2:
            # Lokasi berbeda
            unique_locations = len(set(
                r.get('Alamat', r.get('alamat', '')) for r in reports
            ))
            st.metric("Lokasi Berbeda", unique_locations)
        with col3:
            # Pelapor berbeda
            unique_reporters = len(set(
                r.get('Nama Pelapor', r.get('nama_pelapor', '')) for r in reports
            ))
            st.metric("Pelapor Berbeda", unique_reporters)

def format_date(date_string):
    """Format date untuk display"""
    try:
        if not date_string:
            return "N/A"
        
        # Parse date
        if isinstance(date_string, str):
            date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        else:
            date_obj = date_string
        
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        day_name = days[date_obj.weekday()]
        
        return f"{day_name}, {date_obj.strftime('%d/%m/%y')}"
    except:
        return str(date_string) if date_string else "N/A"

def format_time(time_string):
    """Format time untuk display"""
    try:
        if not time_string:
            return ""
        
        if isinstance(time_string, str):
            if ':' in time_string:
                return time_string[:5]  # HH:MM
            return time_string
        else:
            return str(time_string)
    except:
        return str(time_string) if time_string else ""
