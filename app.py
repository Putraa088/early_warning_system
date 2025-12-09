import streamlit as st
import sys
import os
import traceback

# ==================== CONFIG ====================
st.set_page_config(
    page_title="Sistem Peringatan Dini Banjir",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PATH SETUP ====================
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

for folder in ['controllers', 'models', 'views']:
    folder_path = os.path.join(current_dir, folder)
    if os.path.exists(folder_path) and folder_path not in sys.path:
        sys.path.insert(0, folder_path)

# ==================== DATABASE INITIALIZATION (SAFE) ====================
# Note: kept behavior but added clearer messaging and avoided a silent crash
DB_PATH = 'flood_system.db'
if not os.path.exists(DB_PATH):
    st.warning("⚠️ Database belum diinisialisasi. Menjalankan init database...")
    try:
        from init_tables import init_database
        init_database()
        st.success("✅ Database berhasil diinisialisasi!")
    except Exception as e:
        st.error(f"❌ Gagal inisialisasi database: {e}")
        st.exception(traceback.format_exc())
        st.stop()

# ==================== IMPORT CONTROLLERS (dengan fallback yang informatif) ====================
try:
    from controllers.VisitorController import VisitorController
    from controllers.FloodReportController import FloodReportController
    from controllers.RealTimeDataController import RealTimeDataController
except Exception as e:
    st.error(f"❌ Import Error Controller: {e}")
    st.info("Menggunakan mode fallback untuk pengembangan/testing.")
    st.exception(traceback.format_exc())

    class VisitorController:
        def track_visit(self, page):
            return None
        def get_visitor_stats(self):
            return {}

    class FloodReportController:
        def submit_report(self, *args, **kwargs):
            return False, "Fallback"
        def get_today_reports(self):
            return []

    class RealTimeDataController:
        def get_comprehensive_data(self):
            return []

# ==================== IMPORT VIEWS (dengan fallback informatif) ====================
try:
    from views.visitor_stats import show_visitor_stats
    from views.flood_report_form import show_flood_report_form
    from views.flood_reports_table import show_current_month_reports
    from views.monthly_reports import show_monthly_reports_summary
    from views.prediction_dashboard import show_prediction_dashboard
    from views.ai_analysis import show_ai_analysis
    from views.statistical_analysis import show_statistical_analysis
except Exception as e:
    st.error(f"❌ Import Error Views: {e}")
    st.info("Beberapa view tidak tersedia, menjalankan fallback sederhana.")
    st.exception(traceback.format_exc())

    def show_visitor_stats(*args, **kwargs):
        st.info("Visitor stats not available")

    def show_flood_report_form(*args, **kwargs):
        st.info("Report form not available")

    def show_current_month_reports(*args, **kwargs):
        st.info("Reports not available")

    def show_monthly_reports_summary(*args, **kwargs):
        st.info("Monthly reports not available")

    def show_prediction_dashboard(*args, **kwargs):
        st.info("Prediction dashboard not available")

    def show_ai_analysis(*args, **kwargs):
        st.info("AI analysis not available")

    def show_statistical_analysis(*args, **kwargs):
        st.info("Statistical analysis not available")

# ==================== REFINED (PROFESSIONAL) CSS THEME ====================
# Keputusan: keep CSS inline for portability, but make it smaller and safer.
CSS_THEME = r"""
<style>
:root{
  --bg:#0b0f12;
  --panel:#0f1416;
  --muted:#9aa6ad;
  --accent:#00aee6; /* refined cyan */
  --card:#0f1416;
  --border: rgba(255,255,255,0.04);
}

/* App background */
.stApp, .block-container{ background-color: var(--bg) !important; color: #e8eef1 !important; }

/* Sidebar */
[data-testid="stSidebar"]{ background-color: var(--panel) !important; border-right: 1px solid var(--border) !important; }
[data-testid="stSidebar"] .stButton button{ background: transparent; color: #e8eef1 !important; border: 1px solid transparent; width:100%; padding:10px 16px; text-align:left; border-radius:8px; font-weight:600; }
[data-testid="stSidebar"] .stButton button:hover{ background: rgba(0,174,230,0.06); transform: translateX(3px); }

/* Hero & cards */
.hero-section, .feature-card, .cta-section{ background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); border:1px solid var(--border); border-radius:12px; }
.feature-card{ padding:20px; }
.feature-card h3{ color: var(--accent); margin-bottom:10px; font-weight:800; }

/* Text / headings */
h1,h2,h3{ color:#f7fbfc !important; }
.stMarkdown, .stText, p, span, label{ color: #dfe9ec !important; }

/* Inputs */
.stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox select{ background: #0b1113 !important; color:#e8eef1 !important; border:1px solid rgba(255,255,255,0.04) !important; border-radius:8px !important; padding:8px !important; }
.stTextInput input::placeholder, .stTextArea textarea::placeholder{ color: var(--muted) !important; opacity:1 !important; }

/* File uploader */
.stFileUploader [data-testid="stFileUploadDropzone"]{ background:#0b1113 !important; border:1px dashed rgba(255,255,255,0.03) !important; border-radius:10px; }

/* Buttons */
.stButton button{ background: var(--accent) !important; color: #041016 !important; font-weight:700; padding:10px 16px; border-radius:8px; border:none; }
.stButton button:hover{ filter:brightness(0.95); transform:translateY(-2px); }

/* Small text */
small, .stSmall{ color: var(--muted) !important; }

/* Reduce aggressive global selectors to avoid breaking Streamlit internals */

/* Tables and metrics */
.stDataFrame, .stTable{ color:#e8eef1 !important; }
[data-testid="stMetricValue"]{ color: var(--accent) !important; }

/* Make containers that were white adapt to dark theme */
div[style*="background-color: white"], div[style*="#fff"], div[style*="background: white"]{ background-color: transparent !important; color:#e8eef1 !important; }


.stFileUploader label {
    color: #000000 !important;
}

.stFileUploader div div {
    color: #000000 !important;
}

</style>
"""

st.markdown(CSS_THEME, unsafe_allow_html=True)

# ==================== INIT CONTROLLERS IN SESSION ====================
if 'controllers_initialized' not in st.session_state:
    try:
        st.session_state.visitor_controller = VisitorController()
        st.session_state.flood_controller = FloodReportController()
        st.session_state.realtime_controller = RealTimeDataController()
        st.session_state.controllers_initialized = True
    except Exception:
        st.session_state.controllers_initialized = False

if st.session_state.controllers_initialized:
    visitor_controller = st.session_state.visitor_controller
    flood_controller = st.session_state.flood_controller
    realtime_controller = st.session_state.realtime_controller
else:
    visitor_controller = VisitorController()
    flood_controller = FloodReportController()
    realtime_controller = RealTimeDataController()

# ==================== SIDEBAR NAVIGATION (SAME STRUCTURE) ====================
def setup_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center; margin-bottom:20px; padding:16px; border-radius:10px;">
                <div style="color: var(--accent); font-size:2.2rem;">🌊</div>
                <h2 style="color:var(--accent); margin:0; font-weight:900;">SISTEM BANJIR</h2>
                <p style="color:var(--muted); margin-top:6px; font-weight:600;">Peringatan Dini & Analisis</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")

        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Home"

        menu_items = [
            (" Home", "Home"),
            (" Lapor Banjir", "Lapor Banjir"),
            (" Laporan Harian", "Laporan Harian"),
            (" Rekapan Bulanan", "Rekapan Bulanan"),
            (" Prediksi Real-time", "Prediksi Banjir"),
            (" Analisis AI", "Analisis ANN"),
            (" Analisis Statistik", "Analisis Gumbel")
        ]

        for text, page in menu_items:
            if st.button(text, key=f"menu_{page}", use_container_width=True,
                         type="primary" if st.session_state.current_page == page else "secondary"):
                st.session_state.current_page = page
                st.rerun()

        st.markdown("---")
        st.markdown("### KONTAK KAMI:")
        st.markdown(
            """
            <div style="background: rgba(0,174,230,0.06); padding:12px; border-radius:8px;">
                <div class="contact-row">
                    <div class="contact-icon" style="font-size:1.1rem;">📍</div>
                    <div class="contact-content">
                        <div class="contact-label">LOKASI:</div>
                        <div class="contact-value">Jl. Diponegoro No. 52-58<br>Salatiga, Jawa Tengah</div>
                    </div>
                </div>
                <div style="height:1px; background: rgba(255,255,255,0.03); margin:10px 0;"></div>
                <div class="contact-row">
                    <div class="contact-icon" style="font-size:1.1rem;">📧</div>
                    <div class="contact-content">
                        <div class="contact-label">EMAIL:</div>
                        <div class="contact-value">tyarawahyusaputra@gmail.com</div>
                    </div>
                </div>
                <div style="height:1px; background: rgba(255,255,255,0.03); margin:10px 0;"></div>
                <div class="contact-row">
                    <div class="contact-icon" style="font-size:1.1rem;">📞</div>
                    <div class="contact-content">
                        <div class="contact-label">TELEPON:</div>
                        <div class="contact-value">085156959561</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")

# ==================== PAGES (structure preserved) ====================
def show_homepage():
    st.markdown(
        """
        <div class="hero-section">
            <div class="hero-title">🌊 SISTEM PERINGATAN DINI BANJIR</div>
            <div class="hero-subtitle">Integrasi Deep Learning dan Analisis Statistik untuk Prediksi Banjir yang Akurat</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="status-bar">
            <div class="status-item"><div class="status-value">24/7</div><div class="status-label">MONITORING</div></div>
            <div class="status-item"><div class="status-value">90%</div><div class="status-label">AKURASI</div></div>
            <div class="status-item"><div class="status-value">REAL-TIME</div><div class="status-label">UPDATE</div></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### FITUR UTAMA SISTEM")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
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
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h3> ANALISIS STATISTIK</h3>
                <p>Distribusi Gumbel untuk analisis nilai ekstrem dan perhitungan periode ulang banjir.</p>
                <ul>
                    <li>Probabilitas kejadian ekstrem</li>
                    <li>Periode ulang 5-50 tahun</li>
                    <li>Risk assessment terstruktur</li>
                    <li>Validasi statistik komprehensif</li>
                    <li>Visualisasi data interaktif</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### TEKNOLOGI PENDUKUNG")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <h3> DATABASE</h3>
                <p>SQLite dengan struktur data teroptimasi untuk penyimpanan data historis dan real-time.</p>
                <ul>
                    <li>Penyimpanan data laporan</li>
                    <li>Log prediksi AI</li>
                    <li>Backup otomatis</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            """
            <div class="feature-card">
                <h3> DASHBOARD</h3>
                <p>Interface interaktif dengan visualisasi data real-time dan kontrol yang mudah digunakan.</p>
                <ul>
                    <li>Chart interaktif</li>
                    <li>Responsive design</li>
                    <li>Multi-language support</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="cta-section">
            <h3 style="color: var(--accent) !important; margin-bottom: 10px; font-weight:900;">🚀 SIAP MENGGUNAKAN SISTEM?</h3>
            <p style="color:#dfe9ec !important; margin-bottom:6px; font-weight:700;">Pilih menu di sidebar untuk mulai menggunakan fitur lengkap sistem kami.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_flood_report_page():
    st.markdown(
        """
        <div class="hero-section" style="padding: 30px;">
            <h2 style="color: var(--accent) !important; margin-bottom: 10px; font-weight: 900;">📝 FORM LAPORAN BANJIR</h2>
            <p style="color: #dfe9ec !important; font-size:1.05rem; font-weight:700;">Laporkan kejadian banjir di sekitar Anda untuk membantu sistem peringatan dini.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    show_flood_report_form(flood_controller)


def show_current_month_reports_page():
    st.markdown(
        """
        <div class="hero-section" style="padding: 30px;">
            <h2 style="color: var(--accent) !important; margin-bottom: 10px; font-weight: 900;">📊 LAPORAN HARIAN</h2>
            <p style="color: #dfe9ec !important; font-size:1.05rem; font-weight:700;">Data laporan banjir real-time dari masyarakat.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    show_current_month_reports(flood_controller)


def show_monthly_reports_page():
    st.markdown(
        """
        <div class="hero-section" style="padding: 30px;">
            <h2 style="color: var(--accent) !important; margin-bottom: 10px; font-weight: 900;">📈 REKAPAN BULANAN</h2>
            <p style="color: #dfe9ec !important; font-size:1.05rem; font-weight:700;">Analisis dan statistik laporan banjir bulan ini.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    show_monthly_reports_summary(flood_controller)


def show_prediction_page():
    st.markdown(
        """
        <div class="hero-section" style="padding: 30px;">
            <h2 style="color: var(--accent) !important; margin-bottom: 10px; font-weight: 900;"> PREDIKSI REAL-TIME</h2>
            <p style="color: #dfe9ec !important; font-size:1.05rem; font-weight:700;">Monitoring dan prediksi banjir berdasarkan data BBWS Bengawan Solo.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    show_prediction_dashboard(realtime_controller)


def show_ai_analysis_page():
    st.markdown(
        """
        <div class="hero-section" style="padding: 30px;">
            <h2 style="color: var(--accent) !important; margin-bottom: 10px; font-weight: 900;"> ANALISIS NEURAL NETWORK</h2>
            <p style="color: #dfe9ec !important; font-size:1.05rem; font-weight:700;">Prediksi risiko banjir menggunakan Artificial Intelligence.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    show_ai_analysis()


def show_gumbel_analysis_page():
    st.markdown(
        """
        <div class="hero-section" style="padding: 30px;">
            <h2 style="color: var(--accent) !important; margin-bottom: 10px; font-weight: 900;"> ANALISIS DISTRIBUSI GUMBEL</h2>
            <p style="color: #dfe9ec !important; font-size:1.05rem; font-weight:700;">Analisis statistik untuk prediksi kejadian ekstrem.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    show_statistical_analysis()

# ==================== MAIN APP ====================

def main():
    setup_sidebar()

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
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    main()
