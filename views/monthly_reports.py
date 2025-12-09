import streamlit as st
import pandas as pd
from datetime import datetime

def show_monthly_reports_summary(controller):
    """Display monthly reports summary"""
    
    st.markdown("""
    <style>
    .stat-card {
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
        border: 1px solid #333333;
    }
    .stat-number {
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 5px;
        color: #00a8ff;
    }
    .stat-label {
        font-size: 0.9em;
        color: #aaaaaa;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get statistics
    stats = controller.get_monthly_statistics()
    reports = controller.get_month_reports()
    
    if not reports:
        st.info("📊 Tidak ada laporan banjir untuk bulan ini.")
        return
    
    # Statistics
    st.markdown("### 📈 Statistik Bulanan")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total_reports']}</div>
            <div class="stat-label">Total Laporan</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['avg_per_day']}</div>
            <div class="stat-label">Rata-rata/Hari</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['most_common_height_count']}</div>
            <div class="stat-label">{stats['most_common_height']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        area = stats['most_affected_area'][:15] + "..." if len(stats['most_affected_area']) > 15 else stats['most_affected_area']
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['most_affected_area_count']}</div>
            <div class="stat-label">{area}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 Daftar Laporan")
    
    # Simple table
    for i, report in enumerate(reports, 1):
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
        
        with col1:
            st.write(f"**{i}.** {report['address']}")
        with col2:
            st.write(report['flood_height'])
        with col3:
            st.write(format_date(report['report_date']))
        with col4:
            st.write(report['reporter_name'])
        with col5:
            st.write("✅" if report['photo_path'] else "❌")
        
        if i < len(reports):
            st.divider()

def format_date(date_string):
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')
    except:
        return date_string
