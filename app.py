# app.py - VERSI PROFESIONAL DENGAN LAYOUT SEJAJAR
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

# ==================== CSS TEMA HITAM PROFESIONAL ====================
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
        text-align: left;
        padding: 12px 20px;
        border-radius: 8px;
        margin: 5px 0;
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
        border-radius: 8px !important;
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
        border-radius: 8px;
        padding: 12px 24px;
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
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(145deg, #1a1a1a, #222222);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #333333;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 168, 255, 0.2);
        border-color: #00a8ff;
    }
    
    .feature-card h3 {
        color: #00a8ff;
        font-size: 1.5rem;
        margin-bottom: 15px;
        border-bottom: 2px solid #00a8ff;
        padding-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .feature-card p {
        color: #cccccc;
        line-height: 1.6;
        margin-bottom: 20px;
        flex-grow: 1;
    }
    
    .feature-card ul {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }
    
    .feature-card li {
        color: #dddddd;
        padding: 8px 0;
        padding-left: 25px;
        position: relative;
        border-bottom: 1px solid #333333;
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
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border-radius: 15px;
        padding: 40px;
        margin-bottom: 30px;
        text-align: center;
        border: 1px solid #333333;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    }
    
    .hero-title {
        color: #00a8ff;
        font-size: 2.5rem;
        margin-bottom: 15px;
        font-weight: bold;
    }
    
    .hero-subtitle {
        color: #cccccc;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Status bar */
    .status-bar {
        background: linear-gradient(90deg, #1a1a1a, #222222);
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid #333333;
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
        color: #00a8ff;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .status-label {
        color: #aaaaaa;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Call to action */
    .cta-section {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, rgba(0,168,255,0.1) 0%, rgba(0,168,255,0.05) 100%);
        border-radius: 15px;
        margin: 30px 0;
        border: 1px solid rgba(0, 168, 255, 0.3);
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
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
    }
    
    .cta-button:hover {
        background: #0097e6;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 168, 255, 0.3);
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

# ==================== SIDEBAR NAVIGATION DENGAN KONTAK ====================
def setup_sidebar():
    with st.sidebar:
        # Logo & Title
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px; padding: 20px; background: linear-gradient(135deg, #1a1a1a 0%, #222222 100%); border-radius: 10px; border: 1px solid #333333;">
            <div style="color: #00a8ff; font-size: 2rem; margin-bottom: 10px;">🌊</div>
            <h2 style="color: #00a8ff; font-size: 1.5rem; margin: 0;">SISTEM BANJIR</h2>
            <p style="color: #aaaaaa; font-size: 0.9rem; margin-top: 5px;">Peringatan Dini & Analisis</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Initialize page state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Home"
        
        # Menu items dengan icon
        menu_items = [
            ("🏠 Dashboard", "Home"),
            ("📝 Lapor Banjir", "Lapor Banjir"),
            ("📊 Laporan Harian", "Laporan Harian"),
            ("📈 Rekapan Bulanan", "Rekapan Bulanan"),
            ("🔮 Prediksi Real-time", "Prediksi Banjir"),
            ("🤖 Analisis AI", "Analisis ANN"),
            ("📊 Analisis Statistik", "Analisis Gumbel")
        ]
        
        # Display menu
        for text, page in menu_items:
            if st.button(text, key=f"menu_{page}", use_container_width=True,
                        type="primary" if st.session_state.current_page == page else "secondary"):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        
        # ==================== KONTAK KAMI ====================
        st.markdown("### 📞 KONTAK KAMI")
        
        # Lokasi
        st.markdown("""
        <div style="background: rgba(0, 168, 255, 0.1); padding: 15px; border-radius: 8px; margin: 10px 0;">
            <div class="contact-row">
                <div class="contact-icon">📍</div>
                <div class="contact-content">
                    <div class="contact-label">Lokasi:</div>
                    <div class="contact-value">Jl. Diponegoro No. 52-58<br>Salatiga, Jawa Tengah</div>
                </div>
            </div>
            <div class="contact-row">
                <div class="contact-icon">📧</div>
                <div class="contact-content">
                    <div class="contact-label">Email:</div>
                    <div class="contact-value">tyarawahyusaputra@gmail.com</div>
                </div>
            </div>
            <div class="contact-row">
                <div class="contact-icon">📱</div>
                <div class="contact-content">
                    <div class="contact-label">Telepon:</div>
                    <div class="contact-value">085156959561</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style="text-align: center; color: #666666; font-size: 0.8rem; padding: 10px;">
            <p>© 2024 Sistem Peringatan Dini Banjir</p>
            <p>v2.0 | AI-Powered</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== PAGE FUNCTIONS ====================
def show_homepage():
    """Display homepage dengan design profesional dan sejajar"""
    
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
            <div class="status-label">Monitoring</div>
        </div>
        <div class="status-item">
            <div class="status-value">99%</div>
            <div class="status-label">Akurasi</div>
        </div>
        <div class="status-item">
            <div class="status-value">Real-time</div>
            <div class="status-label">Update</div>
        </div>
        <div class="status-item">
            <div class="status-value">AI + Stat</div>
            <div class="status-label">Integrasi</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # FEATURES SECTION - CARDS SEJAJAR
    st.markdown("### 🚀 FITUR UTAMA SISTEM")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 KECERDASAN BUATAN</h3>
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
            <h3>📊 ANALISIS STATISTIK</h3>
            <p>Distribusi Gumbel untuk analisis nilai ekstrem dan perhitungan periode ulang banjir.</p>
            <ul>
                <li>Probabilitas kejadian ekstrem</li>
                <li>Periode ulang 5-50 tahun</li>
                <li>Risk assessment terstruktur</li>
                <li>Validasi statistik komprehensif</li>
                <li>Visualisasi data interaktif</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ADDITIONAL FEATURES
    st.markdown("### 🔧 TEKNOLOGI PENDUKUNG")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>💾 Database</h3>
            <p>SQLite dengan struktur data teroptimasi untuk penyimpanan data historis dan real-time.</p>
            <ul>
                <li>Penyimpanan data laporan</li>
                <li>Log prediksi AI</li>
                <li>Backup otomatis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h3>📱 Dashboard</h3>
            <p>Interface interaktif dengan visualisasi data real-time dan kontrol yang mudah digunakan.</p>
            <ul>
                <li>Chart interaktif</li>
                <li>Responsive design</li>
                <li>Multi-language support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # CALL TO ACTION
    st.markdown("""
    <div class="cta-section">
        <h3 style="color: #00a8ff; margin-bottom: 15px;">🚀 SIAP MENGGUNAKAN SISTEM?</h3>
        <p style="color: #cccccc; margin-bottom: 20px;">
            Pilih menu di sidebar untuk mulai menggunakan fitur lengkap sistem kami.
            <br><strong>📈 Sistem telah memproses:</strong> 1,245 data historis | <strong>🎯 Akurasi:</strong> 89.2%
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_flood_report_page():
    """Display flood report page"""
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h2 style="color: #00a8ff; margin-bottom: 10px;">📝 FORM LAPORAN BANJIR</h2>
        <p style="color: #cccccc; font-size: 1.1rem;">
            Laporkan kejadian banjir di sekitar Anda untuk membantu sistem peringatan dini.
        </p>
    </div>
    """, unsafe_allow_html=True)
    show_flood_report_form(flood_controller)

def show_current_month_reports_page():
    """Display current month's reports"""
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h2 style="color: #00a8ff; margin-bottom: 10px;">📊 LAPORAN HARIAN</h2>
        <p style="color: #cccccc; font-size: 1.1rem;">
            Data laporan banjir real-time dari masyarakat.
        </p>
    </div>
    """, unsafe_allow_html=True)
    show_current_month_reports(flood_controller)

def show_monthly_reports_page():
    """Display monthly reports summary"""
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h2 style="color: #00a8ff; margin-bottom: 10px;">📈 REKAPAN BULANAN</h2>
        <p style="color: #cccccc; font-size: 1.1rem;">
            Analisis dan statistik laporan banjir bulan ini.
        </p>
    </div>
    """, unsafe_allow_html=True)
    show_monthly_reports_summary(flood_controller)

def show_prediction_page():
    """Display flood prediction page"""
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h2 style="color: #00a8ff; margin-bottom: 10px;">🔮 PREDIKSI REAL-TIME</h2>
        <p style="color: #cccccc; font-size: 1.1rem;">
            Monitoring dan prediksi banjir berdasarkan data BBWS Bengawan Solo.
        </p>
    </div>
    """, unsafe_allow_html=True)
    show_prediction_dashboard(realtime_controller)

def show_ai_analysis_page():
    """Display AI analysis page"""
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h2 style="color: #00a8ff; margin-bottom: 10px;">🤖 ANALISIS NEURAL NETWORK</h2>
        <p style="color: #cccccc; font-size: 1.1rem;">
            Prediksi risiko banjir menggunakan Artificial Intelligence.
        </p>
    </div>
    """, unsafe_allow_html=True)
    show_ai_analysis()

def show_gumbel_analysis_page():
    """Display statistical analysis page"""
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h2 style="color: #00a8ff; margin-bottom: 10px;">📊 ANALISIS DISTRIBUSI GUMBEL</h2>
        <p style="color: #cccccc; font-size: 1.1rem;">
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

