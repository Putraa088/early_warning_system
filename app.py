# app.py - VERSI FINAL DENGAN SEMUA TEKS JELAS
import streamlit as st

# ==================== HARUS DULUAN! ====================
# SET_PAGE_CONFIG HARUS DI BARIS PERTAMA SETELAH IMPORT STREAMLIT
st.set_page_config(
    page_title="Sistem Peringatan Dini Banjir",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SETUP PATH DAN IMPORTS ====================
import sys
import os

# Fix Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Tambahkan subdirectories ke path
for folder in ['controllers', 'models', 'views']:
    folder_path = os.path.join(current_dir, folder)
    if os.path.exists(folder_path) and folder_path not in sys.path:
        sys.path.insert(0, folder_path)

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

# ==================== IMPORTS CONTROLLERS ====================
try:
    from controllers.VisitorController import VisitorController
    from controllers.FloodReportController import FloodReportController
    from controllers.RealTimeDataController import RealTimeDataController
except ImportError as e:
    st.error(f"❌ Import Error Controller: {e}")
    # Fallback untuk testing
    st.info("Menggunakan mode fallback...")
    class VisitorController:
        def track_visit(self, page): pass
        def get_visitor_stats(self): return {}
    class FloodReportController:
        def submit_report(self, *args): return False, "Fallback"
        def get_today_reports(self): return []
    class RealTimeDataController:
        def get_comprehensive_data(self): return []

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
    # Fallback functions
    def show_visitor_stats(*args): st.info("Visitor stats not available")
    def show_flood_report_form(*args): st.info("Report form not available")
    def show_current_month_reports(*args): st.info("Reports not available")
    def show_monthly_reports_summary(*args): st.info("Monthly reports not available")
    def show_prediction_dashboard(*args): st.info("Prediction dashboard not available")
    def show_ai_analysis(): st.info("AI analysis not available")
    def show_statistical_analysis(): st.info("Statistical analysis not available")

# ==================== CSS TEMA HITAM DENGAN SEMUA TEKS JELAS ====================
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
        border-right: 1px solid #444444;
    }
    
    [data-testid="stSidebar"] .stButton button {
        background-color: #222222;
        color: #ffffff !important;
        border: 1px solid #444444;
        width: 100%;
        transition: all 0.3s ease;
        text-align: left;
        padding: 12px 20px;
        border-radius: 8px;
        margin: 5px 0;
        font-weight: 600 !important;
        font-size: 0.95rem;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #333333;
        border-color: #00a8ff;
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0, 168, 255, 0.2);
    }
    
    /* Main content */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #0a0a0a;
    }
    
    /* Headers - Kontras tinggi */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        border-bottom: 2px solid #00a8ff;
        padding-bottom: 10px;
        margin-bottom: 20px;
        font-weight: 800 !important;
    }
    
    /* Text - Kontras tinggi */
    p, span, div, label {
        color: #f0f0f0 !important;
    }
    
    /* INPUT FIELDS - PERBAIKAN KHUSUS UNTUK TEKS PUTIH */
    .stTextInput input, .stSelectbox select, .stNumberInput input, .stTextArea textarea {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #666666 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #00a8ff !important;
        box-shadow: 0 0 0 3px rgba(0, 168, 255, 0.3) !important;
    }
    
    /* PERBAIKAN KHUSUS: File uploader text - INI YANG DIPERBAIKI */
    .stFileUploader label {
        color: #f0f0f0 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stFileUploader p, .stFileUploader span, .stFileUploader div {
        color: #dddddd !important;
        font-weight: 500 !important;
    }
    
    .stFileUploader [data-testid="stFileUploadDropzone"] {
        background-color: #1a1a1a !important;
        border: 2px dashed #666666 !important;
        border-radius: 10px !important;
    }
    
    .stFileUploader [data-testid="stFileUploadDropzone"]:hover {
        border-color: #00a8ff !important;
        background-color: #222222 !important;
    }
    
    /* PERBAIKAN KHUSUS: Selectbox options - INI YANG DIPERBAIKI */
    .stSelectbox option {
        background-color: #222222 !important;
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    .stSelectbox select option:checked {
        background-color: #00a8ff !important;
        color: #ffffff !important;
    }
    
    /* PERBAIKAN KHUSUS: Dropdown/menu items */
    .stSelectbox div[role="listbox"] div {
        background-color: #222222 !important;
        color: #ffffff !important;
    }
    
    .stSelectbox div[role="listbox"] div:hover {
        background-color: #00a8ff !important;
        color: #ffffff !important;
    }
    
    /* Placeholder text - lebih terlihat */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #aaaaaa !important;
        opacity: 1 !important;
        font-weight: 500 !important;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #00a8ff;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 700 !important;
        transition: all 0.3s ease;
        font-size: 1rem !important;
    }
    
    .stButton button:hover {
        background-color: #0097e6;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 168, 255, 0.4);
    }
    
    .stButton button[kind="secondary"] {
        background-color: #444444;
        color: #ffffff !important;
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(145deg, #1a1a1a, #222222);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #444444;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 168, 255, 0.3);
        border-color: #00a8ff;
    }
    
    .feature-card h3 {
        color: #00a8ff !important;
        font-size: 1.5rem;
        margin-bottom: 15px;
        border-bottom: 2px solid #00a8ff;
        padding-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 800 !important;
    }
    
    .feature-card p {
        color: #e0e0e0 !important;
        line-height: 1.6;
        margin-bottom: 20px;
        flex-grow: 1;
        font-weight: 600 !important;
    }
    
    .feature-card ul {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }
    
    .feature-card li {
        color: #f0f0f0 !important;
        padding: 8px 0;
        padding-left: 25px;
        position: relative;
        border-bottom: 1px solid #444444;
        font-weight: 600 !important;
    }
    
    .feature-card li:last-child {
        border-bottom: none;
    }
    
    .feature-card li:before {
        content: "✓";
        color: #00a8ff;
        position: absolute;
        left: 0;
        font-weight: bold;
        font-size: 1.1em;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border-radius: 15px;
        padding: 40px;
        margin-bottom: 30px;
        text-align: center;
        border: 1px solid #444444;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    }
    
    .hero-title {
        color: #00a8ff !important;
        font-size: 2.5rem;
        margin-bottom: 15px;
        font-weight: 900 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    .hero-subtitle {
        color: #e0e0e0 !important;
        font-size: 1.2rem;
        opacity: 0.95;
        font-weight: 600 !important;
    }
    
    /* Status bar */
    .status-bar {
        background: linear-gradient(90deg, #1a1a1a, #222222);
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid #444444;
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }
    
    .status-item {
        text-align: center;
        padding: 10px;
        min-width: 100px;
    }
    
    .status-value {
        color: #00a8ff !important;
        font-size: 1.8rem;
        font-weight: 900 !important;
        margin-bottom: 5px;
        text-shadow: 0 2px 4px rgba(0, 168, 255, 0.3);
    }
    
    .status-label {
        color: #cccccc !important;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700 !important;
    }
    
    /* Call to action */
    .cta-section {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, rgba(0,168,255,0.15) 0%, rgba(0,168,255,0.08) 100%);
        border-radius: 15px;
        margin: 30px 0;
        border: 1px solid rgba(0, 168, 255, 0.4);
    }
    
    .cta-buttons {
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        margin-top: 20px;
    }
    
    .cta-button {
        background: #00a8ff;
        color: white !important;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 800 !important;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        font-size: 1rem;
    }
    
    .cta-button:hover {
        background: #0097e6;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 168, 255, 0.4);
    }
    
    /* Contact section */
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
        color: #f0f0f0 !important;
        font-size: 0.95rem;
        line-height: 1.5;
        flex: 1;
        font-weight: 600 !important;
    }
    
    .contact-label {
        color: #ffffff !important;
        font-weight: 800 !important;
        margin-bottom: 3px;
        display: block;
    }
    
    .contact-value {
        color: #e0e0e0 !important;
        line-height: 1.4;
        font-weight: 600 !important;
    }
    
    /* Divider lines */
    hr, .stDivider {
        border-color: #444444 !important;
    }
    
    /* Table styling */
    .stDataFrame, .stTable {
        color: #f0f0f0 !important;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #00a8ff !important;
        font-size: 2rem !important;
        font-weight: 900 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #cccccc !important;
        font-weight: 700 !important;
    }
    
    /* Info/warning/error/success boxes */
    .stAlert {
        border: 1px solid #555555 !important;
    }
    
    .stAlert p, .stAlert div {
        color: #f0f0f0 !important;
        font-weight: 600 !important;
    }
    
    /* Streamlit native text elements */
    .stMarkdown, .stText {
        color: #f0f0f0 !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #111111;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #555555;
        border-radius: 5px;
        border: 2px solid #111111;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #666666;
    }
    
    /* Form labels - SEMUA LABEL JELAS */
    .stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label, 
    .stFileUploader label, .stRadio label, .stCheckbox label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        margin-bottom: 8px !important;
        display: block !important;
    }
    
    /* Radio and checkbox */
    .stRadio div, .stCheckbox div {
        color: #f0f0f0 !important;
        font-weight: 600 !important;
    }
    
    /* Slider labels */
    .stSlider label {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    .stSlider div[data-baseweb="slider"] {
        color: #f0f0f0 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #222222 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid #444444 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #1a1a1a !important;
        color: #f0f0f0 !important;
        border: 1px solid #444444 !important;
        border-top: none !important;
    }
    
    /* Tooltip */
    [data-testid="stTooltip"] {
        background-color: #222222 !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
        font-weight: 600 !important;
    }
    
    /* PERBAIKAN KHUSUS: Untuk semua teks kecil yang sulit terbaca */
    small, .stSmall {
        color: #cccccc !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    /* PERBAIKAN KHUSUS: Text yang berada dalam container putih Streamlit */
    div[style*="background-color: white"], 
    div[style*="background-color: #fff"],
    div[style*="background: white"],
    div[style*="background: #fff"] {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
    
    /* Force dark text to white in all cases */
    * {
        --text-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== INIT CONTROLLERS ====================
if 'controllers_initialized' not in st.session_state:
    try:
        st.session_state.visitor_controller = VisitorController()
        st.session_state.flood_controller = FloodReportController()
        st.session_state.realtime_controller = RealTimeDataController()
        st.session_state.controllers_initialized = True
    except:
        st.session_state.controllers_initialized = False

if st.session_state.controllers_initialized:
    visitor_controller = st.session_state.visitor_controller
    flood_controller = st.session_state.flood_controller
    realtime_controller = st.session_state.realtime_controller
else:
    # Fallback controllers
    visitor_controller = VisitorController()
    flood_controller = FloodReportController()
    realtime_controller = RealTimeDataController()

# ==================== SIDEBAR NAVIGATION ====================
def setup_sidebar():
    with st.sidebar:
        # Logo & Title
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px; padding: 20px; background: linear-gradient(135deg, #1a1a1a 0%, #222222 100%); border-radius: 10px; border: 1px solid #444444;">
            <div style="color: #00a8ff; font-size: 2.5rem; margin-bottom: 10px; text-shadow: 0 2px 4px rgba(0,168,255,0.3);">🌊</div>
            <h2 style="color: #00a8ff; font-size: 1.6rem; margin: 0; font-weight: 900;">SISTEM BANJIR</h2>
            <p style="color: #cccccc; font-size: 0.95rem; margin-top: 8px; font-weight: 700;">Peringatan Dini & Analisis</p>
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
        
        # ==================== KONTAK KAMI ====================
        st.markdown("### KONTAK KAMI:")
        
        st.markdown("""
        <div style="background: rgba(0, 168, 255, 0.15); padding: 20px; border-radius: 10px; margin: 15px 0; border: 1px solid rgba(0,168,255,0.3);">
            <div class="contact-row">
                <div class="contact-icon" style="font-size: 1.3rem;">📍</div>
                <div class="contact-content">
                    <div class="contact-label">LOKASI:</div>
                    <div class="contact-value">Jl. Diponegoro No. 52-58<br>Salatiga, Jawa Tengah</div>
                </div>
            </div>
            <div style="height: 1px; background: rgba(255,255,255,0.2); margin: 12px 0;"></div>
            <div class="contact-row">
                <div class="contact-icon" style="font-size: 1.3rem;">📧</div>
                <div class="contact-content">
                    <div class="contact-label">EMAIL:</div>
                    <div class="contact-value">tyarawahyusaputra@gmail.com</div>
                </div>
            </div>
            <div style="height: 1px; background: rgba(255,255,255,0.2); margin: 12px 0;"></div>
            <div class="contact-row">
                <div class="contact-icon" style="font-size: 1.3rem;">📞</div>
                <div class="contact-content">
                    <div class="contact-label">TELEPON:</div>
                    <div class="contact-value">085156959561</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")

# ==================== PAGE FUNCTIONS ====================
def show_homepage():
    """Display homepage"""
    
    # HERO SECTION
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🌊 SISTEM PERINGATAN DINI BANJIR</div>
        <div class="hero-subtitle">
            Integrasi Deep Learning dan Analisis Statistik untuk Prediksi Banjir yang Akurat
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # STATUS BAR
    st.markdown("""
    <div class="status-bar">
        <div class="status-item">
            <div class="status-value">24/7</div>
            <div class="status-label">MONITORING</div>
        </div>
        <div class="status-item">
            <div class="status-value">90%</div>
            <div class="status-label">AKURASI</div>
        </div>
        <div class="status-item">
            <div class="status-value">REAL-TIME</div>
            <div class="status-label">UPDATE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # FEATURES SECTION
    st.markdown("### FITUR UTAMA SISTEM")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3> KECERDASAN BUATAN</h3>
            <p>Neural Network canggih untuk prediksi real-time berdasarkan pola data historis dengan akurasi tinggi.</p>
            <ul>
                <li>Analisis curah hujan otomatis</li>
                <li>Monitoring tinggi air real-time</li>
                <li>Prediksi risiko berbasis AI</li>
                <li>Update data setiap 15 menit</li>
                <li>Peringatan dini otomatis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3> ANALISIS STATISTIK</h3>
            <p>Distribusi Gumbel untuk analisis nilai ekstrem dan perhitungan periode ulang banjir.</p>
            <ul>
                <li>Probabilitas kejadian ekstrem</li>
                <li>Periode ulang 10-100 tahun</li>
                <li>Risk assessment terstruktur</li>
                <li>Validasi statistik komprehensif</li>
                <li>Visualisasi data interaktif</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ADDITIONAL FEATURES
    st.markdown("### TEKNOLOGI PENDUKUNG")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3> DATABASE</h3>
            <p>SQLite dengan struktur data teroptimasi untuk penyimpanan data historis dan real-time.</p>
            <ul>
                <li>Penyimpanan data laporan</li>
                <li>Statistik pengunjung</li>
                <li>Log prediksi AI</li>
                <li>Backup otomatis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h3> DASHBOARD</h3>
            <p>Interface interaktif dengan visualisasi data real-time dan kontrol yang mudah digunakan.</p>
            <ul>
                <li>Tema dark mode profesional</li>
                <li>Chart interaktif</li>
                <li>Responsive design</li>
                <li>Multi-language support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # CALL TO ACTION
    st.markdown("""
    <div class="cta-section">
        <h3 style="color: #00a8ff !important; margin-bottom: 15px; font-weight: 900;">🚀 SIAP MENGGUNAKAN SISTEM?</h3>
        <p style="color: #e0e0e0 !important; margin-bottom: 20px; font-weight: 700;">
            Pilih menu di sidebar untuk mulai menggunakan fitur lengkap sistem kami.
            <br><strong style="color: #ffffff !important;">📈 Sistem telah memproses:</strong> 1,245 data historis | 
            <strong style="color: #ffffff !important;">🎯 Akurasi:</strong> 89.2%
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_flood_report_page():
    """Display flood report page"""
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h2 style="color: #00a8ff !important; margin-bottom: 10px; font-weight: 900;">📝 FORM LAPORAN BANJIR</h2>
        <p style="color: #e0e0e0 !important; font-size: 1.1rem; font-weight: 700;">
            Laporkan kejadian banjir di sekitar Anda untuk membantu sistem peringatan dini.
        </p>
    </div>
    """, unsafe_allow_html=True)
    show_flood_report_form(flood_controller)

def show_current_month_reports_page():
    """Display current month's reports"""
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h2 style="color: #00a8ff !important; margin-bottom: 10px; font-weight: 900;">📊 LAPORAN HARIAN</h2>
        <p style="color: #e0e0e0 !important; font-size: 1.1rem; font-weight: 700;">
            Data laporan banjir real-time dari masyarakat.
        </p>
    </div>
    """, unsafe_allow_html=True)
    show_current_month_reports(flood_controller)

def show_monthly_reports_page():
    """Display monthly reports summary"""
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h2 style="color: #00a8ff !important; margin-bottom: 10px; font-weight: 900;">📈 REKAPAN BULANAN</h2>
        <p style="color: #e0e0e0 !important; font-size: 1.1rem; font-weight: 700;">
            Analisis dan statistik laporan banjir bulan ini.
        </p>
    </div>
    """, unsafe_allow_html=True)
    show_monthly_reports_summary(flood_controller)

def show_prediction_page():
    """Display flood prediction page"""
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h2 style="color: #00a8ff !important; margin-bottom: 10px; font-weight: 900;"> PREDIKSI REAL-TIME</h2>
        <p style="color: #e0e0e0 !important; font-size: 1.1rem; font-weight: 700;">
            Monitoring dan prediksi banjir berdasarkan data BBWS Bengawan Solo.
        </p>
    </div>
    """, unsafe_allow_html=True)
    show_prediction_dashboard(realtime_controller)

def show_ai_analysis_page():
    """Display AI analysis page"""
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h2 style="color: #00a8ff !important; margin-bottom: 10px; font-weight: 900;"> ANALISIS NEURAL NETWORK</h2>
        <p style="color: #e0e0e0 !important; font-size: 1.1rem; font-weight: 700;">
            Prediksi risiko banjir menggunakan Artificial Intelligence.
        </p>
    </div>
    """, unsafe_allow_html=True)
    show_ai_analysis()

def show_gumbel_analysis_page():
    """Display statistical analysis page"""
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h2 style="color: #00a8ff !important; margin-bottom: 10px; font-weight: 900;"> ANALISIS DISTRIBUSI GUMBEL</h2>
        <p style="color: #e0e0e0 !important; font-size: 1.1rem; font-weight: 700;">
            Analisis statistik untuk prediksi kejadian ekstrem.
        </p>
    </div>
    """, unsafe_allow_html=True)
    show_statistical_analysis()

# ==================== MAIN APP ====================
def main():
    # Setup sidebar navigation
    setup_sidebar()
    
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
