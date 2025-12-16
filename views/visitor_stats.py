import streamlit as st

def show_visitor_stats(stats):
    """Display visitor statistics component untuk homepage saja"""
    
    st.markdown("""
    <style>
    .visitor-stats-container {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        border: 1px solid #333333;
    }
    .stats-header h3 {
        margin: 0 0 25px 0;
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
        color: #00a8ff;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-bottom: 20px;
    }
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stat-number {
        font-size: 2.8em;
        font-weight: bold;
        margin-bottom: 8px;
        color: #00a8ff;
    }
    .stat-label {
        font-size: 1em;
        color: #aaaaaa;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="visitor-stats-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="stats-header"><h3> STATISTIK PENGUNJUNG</h3></div>', unsafe_allow_html=True)
    
    # Stats grid
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    
    # Today visitors
    st.markdown(f'''
    <div class="stat-card">
        <div class="stat-number">{stats.get('today', 0)}</div>
        <div class="stat-label">Pengunjung Hari Ini</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Month visitors
    st.markdown(f'''
    <div class="stat-card">
        <div class="stat-number">{stats.get('month', 0)}</div>
        <div class="stat-label">Pengunjung Bulan Ini</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Online visitors
    st.markdown(f'''
    <div class="stat-card">
        <div class="stat-number">{stats.get('online', 0)}</div>
        <div class="stat-label">Pengunjung Online</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)