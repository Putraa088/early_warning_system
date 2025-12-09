# app.py - TAMBAHKAN SETELAH st.set_page_config()
import sys
import os

# ==================== HARUS DULUAN! ====================
st.set_page_config(
    page_title="Sistem Peringatan Dini Banjir",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== FIX PYTHON PATH ====================
current_dir = os.path.dirname(os.path.abspath(__file__))

# Tambahkan root directory ke path
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Tambahkan juga subdirectories ke path
for folder in ['controllers', 'models', 'views']:
    folder_path = os.path.join(current_dir, folder)
    if os.path.exists(folder_path) and folder_path not in sys.path:
        sys.path.insert(0, folder_path)

# Debug (opsional, bisa dihapus setelah berhasil)
# st.write(f"Python path: {sys.path}")

# ==================== INIT DATABASE ====================
# Pastikan database sudah ada
if not os.path.exists('flood_system.db'):
    st.warning("⚠️ Database belum diinisialisasi. Menjalankan init database...")
    try:
        from init_tables import init_database
        init_database()
        st.success("✅ Database berhasil diinisialisasi!")
    except Exception as e:
        st.error(f"❌ Gagal inisialisasi database: {e}")
        st.stop()

# ==================== IMPORTS ====================
try:
    from controllers.VisitorController import VisitorController
    from controllers.FloodReportController import FloodReportController
    from controllers.RealTimeDataController import RealTimeDataController
except ImportError as e:
    st.error(f"❌ Import Error Controller: {e}")
    st.stop()

# Import views
try:
    from views.visitor_stats import show_visitor_stats
    from views.flood_report_form import show_flood_report_form
    from views.flood_reports_table import show_current_month_reports
    from views.monthly_reports import show_monthly_reports_summary
    from views.prediction_dashboard import show_prediction_dashboard
    from views.ai_analysis import show_ai_analysis
    from views.statistical_analysis import show_statistical_analysis
except ImportError as e:
    st.error(f"❌ Import Error Views: {e}")
    st.stop()

# ==================== CSS TEMA HITAM ====================
st.markdown("""
<style>
    /* Background utama */
    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #333333;
    }
    
    [data-testid="stSidebar"] .stButton button {
        background-color: #222222;
        color: white;
        border: 1px solid #444444;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #333333;
        border-color: #666666;
        transform: translateX(5px);
    }
    
    /* Main content */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #0a0a0a;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        border-bottom: 2px solid #00a8ff;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Text */
    p, span, div, label {
        color: #dddddd !important;
    }
    
    /* Input fields */
    .stTextInput input, .stSelectbox select, .stNumberInput input, .stTextArea textarea {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus, .stNumberInput input:focus {
        border-color: #00a8ff !important;
        box-shadow: 0 0 0 2px rgba(0, 168, 255, 0.2) !important;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #00a8ff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #0097e6;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 168, 255, 0.3);
    }
    
    .stButton button[kind="secondary"] {
        background-color: #444444;
    }
    
    /* Cards */
    .card {
        background: linear-gradient(145deg, #1a1a1a, #222222);
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid #333333;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00a8ff !important;
        font-size: 2rem !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #aaaaaa !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #111111;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #444444;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555555;
    }
    
    /* Style untuk kontak - FIXED */
    .contact-section {
        background: linear-gradient(145deg, #1a1a1a, #222222);
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid #333333;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .contact-title {
        color: #00a8ff;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 15px;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    
    .contact-row {
        display: flex;
        align-items: flex-start;
        margin: 12px 0;
        padding: 8px 0;
    }
    
    .contact-icon {
        color: #00a8ff;
        font-size: 1.2rem;
        min-width: 30px;
        text-align: center;
        margin-top: 2px;
    }
    
    .contact-content {
        color: #dddddd;
        font-size: 0.9rem;
        line-height: 1.5;
        flex: 1;
    }
    
    .contact-label {
        color: #ffffff;
        font-weight: 600;
        margin-bottom: 3px;
        display: block;
    }
    
    .contact-value {
        color: #cccccc;
        line-height: 1.4;
    }
    
    .contact-divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #444444, transparent);
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== INIT CONTROLLERS ====================
if 'controllers_initialized' not in st.session_state:
    st.session_state.visitor_controller = VisitorController()
    st.session_state.flood_controller = FloodReportController()
    st.session_state.realtime_controller = RealTimeDataController()
    st.session_state.controllers_initialized = True

visitor_controller = st.session_state.visitor_controller
flood_controller = st.session_state.flood_controller
realtime_controller = st.session_state.realtime_controller

# ==================== SIDEBAR NAVIGATION DENGAN KONTAK ====================
def setup_sidebar():
    with st.sidebar:
        # Logo & Title
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #00a8ff; font-size: 1.8rem; margin-bottom: 5px;">🌊</h1>
            <h2 style="color: #00a8ff; font-size: 1.5rem; margin: 0;">SISTEM BANJIR</h2>
            <p style="color: #aaaaaa; font-size: 0.9rem; margin-top: 5px;">Peringatan Dini & Analisis</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Initialize page state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Home"
        
        # Menu items
        menu_items = [
            (" Home", "Home"),
            (" Lapor Banjir", "Lapor Banjir"),
            (" Laporan Harian", "Laporan Harian"),
            (" Rekapan Bulanan", "Rekapan Bulanan"),
            (" Prediksi Real-time", "Prediksi Banjir"),
            (" Analisis AI", "Analisis ANN"),
            (" Analisis Statistik", "Analisis Gumbel")
        ]
        
        # Display menu
        for text, page in menu_items:
            if st.button(text, key=f"menu_{page}", use_container_width=True,
                        type="primary" if st.session_state.current_page == page else "secondary"):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        
        # ==================== KONTAK KAMI - STREAMLIT NATIVE ====================
        st.markdown("### 📞 KONTAK KAMI")
        
        # Lokasi
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown("📍")
            with col2:
                st.markdown("**Lokasi:**")
                st.markdown("Jl. Diponegoro No. 52-58")
                st.markdown("Kota, 50711")
                st.markdown("Salatiga, Jawa Tengah")
        
        st.divider()
        
        # Email
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown("📧")
            with col2:
                st.markdown("**Email:**")
                st.markdown("tyarawahyusaputra@gmail.com")
                st.markdown("662022008@student.uksw.edu")
        
        st.divider()
        
        # Telepon
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown("📱")
            with col2:
                st.markdown("**Telepon:**")
                st.markdown("085156959561")
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style="text-align: center; color: #666666; font-size: 0.8rem; padding: 10px;">
            <p>© 2024 Sistem Peringatan Dini Banjir</p>
            <p>v2.0 - Tema Hitam</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== PAGE FUNCTIONS ====================
def show_homepage():
    """Display homepage"""
    st.markdown("""
    <div class="card">
        <h1 style="text-align: center; color: #00a8ff;">🌊 SISTEM PERINGATAN DINI BANJIR</h1>
        <p style="text-align: center; font-size: 1.2rem; margin-top: 10px;">
            Integrasi Deep Learning dan Analisis Statistik untuk Prediksi Banjir yang Akurat
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3> KECERDASAN BUATAN</h3>
            <p>Neural Network untuk prediksi real-time berdasarkan pola data historis.</p>
            <ul>
                <li>Analisis curah hujan</li>
                <li>Monitoring tinggi air</li>
                <li>Prediksi risiko otomatis</li>
                <li>Update real-time</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3> ANALISIS STATISTIK</h3>
            <p>Distribusi Gumbel untuk analisis nilai ekstrem dan periode ulang.</p>
            <ul>
                <li>Probabilitas kejadian</li>
                <li>Periode ulang banjir</li>
                <li>Risk assessment</li>
                <li>Validasi statistik</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Visitor Statistics
    try:
        stats = visitor_controller.get_visitor_stats()
        show_visitor_stats(stats)
    except:
        pass

def show_flood_report_page():
    """Display flood report page"""
    st.markdown("""
    <div class="card">
        <h2>📝 FORM LAPORAN BANJIR</h2>
        <p>Laporkan kejadian banjir di sekitar Anda untuk membantu sistem peringatan dini.</p>
    </div>
    """, unsafe_allow_html=True)
    show_flood_report_form(flood_controller)

def show_current_month_reports_page():
    """Display current month's reports"""
    st.markdown("""
    <div class="card">
        <h2>📊 LAPORAN HARIAN</h2>
        <p>Data laporan banjir real-time dari masyarakat.</p>
    </div>
    """, unsafe_allow_html=True)
    show_current_month_reports(flood_controller)

def show_monthly_reports_page():
    """Display monthly reports summary"""
    st.markdown("""
    <div class="card">
        <h2>📈 REKAPAN BULANAN</h2>
        <p>Analisis dan statistik laporan banjir bulan ini.</p>
    </div>
    """, unsafe_allow_html=True)
    show_monthly_reports_summary(flood_controller)

def show_prediction_page():
    """Display flood prediction page"""
    st.markdown("""
    <div class="card">
        <h2>🔮 PREDIKSI REAL-TIME</h2>
        <p>Monitoring dan prediksi banjir berdasarkan data BBWS Bengawan Solo.</p>
    </div>
    """, unsafe_allow_html=True)
    show_prediction_dashboard(realtime_controller)

def show_ai_analysis_page():
    """Display AI analysis page"""
    st.markdown("""
    <div class="card">
        <h2>🤖 ANALISIS NEURAL NETWORK</h2>
        <p>Prediksi risiko banjir menggunakan Artificial Intelligence.</p>
    </div>
    """, unsafe_allow_html=True)
    show_ai_analysis()

def show_gumbel_analysis_page():
    """Display statistical analysis page"""
    st.markdown("""
    <div class="card">
        <h2>📈 ANALISIS DISTRIBUSI GUMBEL</h2>
        <p>Analisis statistik untuk prediksi kejadian ekstrem.</p>
    </div>
    """, unsafe_allow_html=True)
    show_statistical_analysis()

# ==================== TRACK VISIT ====================
def track_page_visit(page_title):
    """Track page visits for statistics"""
    try:
        visitor_controller.track_visit(page_title)
    except:
        pass

# ==================== MAIN APP ====================
def main():
    # Setup sidebar navigation
    setup_sidebar()
    
    # Track page visit
    track_page_visit(st.session_state.current_page)
    
    # Route to appropriate page
    page_handlers = {
        "Home": show_homepage,
        "Lapor Banjir": show_flood_report_page,
        "Laporan Harian": show_current_month_reports_page,
        "Rekapan Bulanan": show_monthly_reports_page,
        "Prediksi Banjir": show_prediction_page,
        "Analisis ANN": show_ai_analysis_page,
        "Analisis Gumbel": show_gumbel_analysis_page,
    }
    
    handler = page_handlers.get(st.session_state.current_page, show_homepage)
    handler()

if __name__ == "__main__":
    # Initialize current page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    

    main()
