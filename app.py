import streamlit as st
import streamlit.components.v1 as components
import sys
import os
import traceback
import time

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

# ==================== DATABASE INITIALIZATION ====================
DB_PATH = 'flood_system.db'
print(f"🔍 Checking database at: {os.path.abspath(DB_PATH)}")

if not os.path.exists(DB_PATH):
    st.warning("⚠️ Database belum diinisialisasi. Menjalankan init database...")
    try:
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flood_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                address TEXT NOT NULL,
                flood_height TEXT NOT NULL,
                reporter_name TEXT NOT NULL,
                reporter_phone TEXT,
                photo_path TEXT,
                ip_address TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        st.success("✅ Database berhasil diinisialisasi!")
    except Exception as e:
        st.error(f"❌ Gagal inisialisasi database: {e}")
else:
    print(f"✅ Database found: {os.path.getsize(DB_PATH)} bytes")

# ==================== IMPORT CONTROLLERS ====================
try:
    from controllers.VisitorController import VisitorController
    from controllers.FloodReportController import FloodReportController
    from controllers.RealTimeDataController import RealTimeDataController
    print("✅ Semua controllers berhasil di-import")
except Exception as e:
    st.error(f"Import Error Controller: {e}")
    
    class VisitorController:
        def track_visit(self, page): return None
        def get_visitor_stats(self): return {}
    
    class FloodReportController:
        def submit_report(self, *args, **kwargs):
            return False, "Sistem offline - Google Sheets tidak terhubung"
        def get_today_reports(self): return []
        def get_month_reports(self): return []
        def get_all_reports(self): return []
        def get_monthly_statistics(self): return {}
        def get_client_ip(self): return "127.0.0.1"
    
    class RealTimeDataController:
        def get_comprehensive_data(self): return []
        def get_overall_risk_status(self, p): return "RENDAH", "green"
        def is_same_location(self, l1, l2): return True

# ==================== IMPORT MODEL PREDICTION ====================
try:
    from model_ann import predict_flood_ann_with_temp_range
except ImportError:
    def predict_flood_ann_with_temp_range(rainfall, water_level, humidity, temp_min, temp_max):
        """Fallback prediction function"""
        temp_avg = (temp_min + temp_max) / 2
        risk = min(1.0, (rainfall / 300) * 0.5 + (water_level / 150) * 0.3 + (humidity / 100) * 0.15 + ((temp_avg - 20) / 20) * 0.05)
        
        if risk >= 0.7:
            status = "TINGGI"
            message = "WASPADA! Potensi banjir tinggi"
        elif risk >= 0.4:
            status = "MENENGAH"
            message = "SIAGA! Pantau perkembangan"
        else:
            status = "RENDAH"
            message = "AMAN, tetap waspada"
        
        return {
            'risk_level': round(risk, 3),
            'status': status,
            'message': message,
            'temperature_range': {'min': temp_min, 'max': temp_max, 'average': temp_avg}
        }

# ==================== IMPORT VIEWS ====================
try:
    from views.flood_report_form import show_flood_report_form
    from views.flood_reports_table import show_current_month_reports
    from views.monthly_reports import show_monthly_reports_summary
    from views.prediction_dashboard import show_prediction_dashboard
    from views.panduan_page import show_panduan_page 
except Exception as e:
    st.error(f"Import Error Views: {e}")

    def show_flood_report_form(*args, **kwargs):
        st.info("Report form not available")

    def show_current_month_reports(*args, **kwargs):
        st.info("Reports not available")

    def show_monthly_reports_summary(*args, **kwargs):
        st.info("Monthly reports not available")

    def show_prediction_dashboard(*args, **kwargs):
        st.info("Prediction dashboard not available")
    
    def show_panduan_page():  
        st.info("Panduan tidak tersedia")

# ==================== CSS THEME ====================
CSS_THEME = r"""
<style>
:root{
  --bg:#0b0f12;
  --panel:#0f1416;
  --muted:#9aa6ad;
  --accent:#00aee6;
  --card:#0f1416;
  --border: rgba(255,255,255,0.04);
}

/* KEMBALIKAN SCROLLBAR NORMAL */
.stApp, .block-container{ 
    background-color: var(--bg) !important; 
    color: #e8eef1 !important; 
}

[data-testid="stSidebar"]{ 
    background-color: var(--panel) !important; 
    border-right: 1px solid var(--border) !important; 
}

[data-testid="stSidebar"] .stButton button{ 
    background: transparent; 
    color: #e8eef1 !important; 
    border: 1px solid transparent; 
    width:100%; 
    padding: 12px 20px;
    text-align: left; 
    border-radius: 8px; 
    font-weight: 500;
    font-size: 16px;
    margin: 4px 0;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] .stButton button:hover{ 
    background: rgba(0,174,230,0.08); 
    transform: translateX(4px);
}

[data-testid="stSidebar"] .stButton button:active{ 
    background: rgba(0,174,230,0.12); 
}

.sidebar-header {
    text-align: center;
    margin: 20px 0 30px 0;
    padding: 0 10px;
}

.sidebar-title {
    color: var(--accent);
    font-size: 1.8rem;
    font-weight: 700;
    margin: 10px 0 5px 0;
}

.hero-section, .feature-card, .cta-section{ 
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); 
    border:1px solid var(--border); 
    border-radius:12px; 
}

.feature-card{ 
    padding: 24px; 
}

.feature-card h3{ 
    color: var(--accent); 
    margin-bottom:12px; 
    font-weight:700; 
}

h1,h2,h3{ 
    color:#f7fbfc !important; 
}

.stMarkdown, .stText, p, span, label{ 
    color: #dfe9ec !important; 
}

.stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox select{ 
    background: #0b1113 !important; 
    color:#e8eef1 !important; 
    border:1px solid rgba(255,255,255,0.04) !important; 
    border-radius:8px !important; 
    padding:10px 12px !important; 
}

.stTextInput input::placeholder, .stTextArea textarea::placeholder{ 
    color: var(--muted) !important; 
    opacity:1 !important; 
}

.stFileUploader [data-testid="stFileUploadDropzone"]{ 
    background:#0b1113 !important; 
    border:1px dashed rgba(255,255,255,0.03) !important; 
    border-radius:10px; 
}

.stButton button{ 
    background: var(--accent) !important; 
    color: #041016 !important; 
    font-weight:600; 
    padding: 12px 24px;
    border-radius:8px; 
    border:none; 
    font-size: 16px;
}

.stButton button:hover{ 
    filter:brightness(0.95); 
    transform:translateY(-2px);
}

.stSmall{ 
    color: var(--muted) !important; 
}

.stDataFrame, .stTable{ 
    color:#e8eef1 !important; 
}

[data-testid="stMetricValue"]{ 
    color: var(--accent) !important; 
}

.contact-info {
    background: rgba(0,174,230,0.06); 
    padding: 16px;
    border-radius: 10px;
    margin: 20px 0;
}

.contact-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 12px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.03);
}

.contact-item:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
}

.contact-icon {
    font-size: 1.2rem;
    margin-right: 12px;
    color: var(--accent);
    min-width: 24px;
}

.contact-content {
    flex: 1;
}

.contact-label {
    color: var(--muted);
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 2px;
}

.contact-value {
    color: #dfe9ec;
    font-size: 0.95rem;
    font-weight: 400;
    line-height: 1.4;
}

.text-center {
    text-align: center !important;
}

.full-width {
    width: 100%;
}

.section-divider {
    height: 1px;
    background: rgba(255,255,255,0.04);
    margin: 25px 0;
}

.prediction-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 30px;
    margin: 20px 0;
}

.prediction-header {
    text-align: center;
    margin-bottom: 30px;
}

/* HAPUS ATURAN OVERFLOW HIDDEN */
.element-container, .st-emotion-cache-1p1nwyz {
    /* overflow: hidden !important; */ /* DIHAPUS */
}

/* Pastikan scrollbar normal */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 100% !important;
}

/* Form container dengan scroll normal */
[data-testid="stForm"] {
    overflow: auto !important;
}
</style>
"""

st.markdown(CSS_THEME, unsafe_allow_html=True)

# ==================== INIT CONTROLLERS IN SESSION ====================
if 'controllers_initialized' not in st.session_state:
    try:
        print("🔄 Initializing controllers...")
        st.session_state.visitor_controller = VisitorController()
        st.session_state.flood_controller = FloodReportController()
        st.session_state.realtime_controller = RealTimeDataController()
        st.session_state.controllers_initialized = True
        print("✅ All controllers initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing controllers: {e}")
        import traceback
        traceback.print_exc()
        st.session_state.controllers_initialized = False

if st.session_state.controllers_initialized:
    visitor_controller = st.session_state.visitor_controller
    flood_controller = st.session_state.flood_controller
    realtime_controller = st.session_state.realtime_controller
else:
    visitor_controller = VisitorController()
    flood_controller = FloodReportController()
    realtime_controller = RealTimeDataController()

# ==================== SIDEBAR NAVIGATION ====================
def setup_sidebar():
    with st.sidebar:
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Home"
        
        menu_items = [
            ("Home", "Home"),
            ("Panduan", "Panduan"),  
            ("Lapor Banjir", "Lapor Banjir"),
            ("Catatan Laporan", "Catatan Laporan"),  
            ("Prediksi Real-time", "Prediksi Banjir"),
            ("Simulasi Banjir", "Simulasi Banjir")
        ]

        st.markdown('<div style="margin: 10px 0;">', unsafe_allow_html=True)
        
        for text, page in menu_items:
            is_active = st.session_state.current_page == page
            
            if st.button(text, key=f"menu_{page}", use_container_width=True,
                        type="primary" if is_active else "secondary"):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### Kontak Kami:")
        
        with st.container():
            st.markdown("**LOKASI**")
            st.markdown("Jl. Diponegoro No. 52-58")
            st.markdown("Salatiga, Jawa Tengah")
            
            st.markdown("---")
            
            st.markdown("**EMAIL**")
            st.markdown("tyarawahyusaputra@gmail.com")
            
            st.markdown("---")
            
            st.markdown("**TELEPON**")
            st.markdown("085156959561")

# ==================== HOME PAGE ====================
def show_homepage():
    st.markdown(
        """
        <div class="hero-section" style="padding: 40px; margin: 30px 0; text-align: center;">
            <h1 style="color: var(--accent) !important; margin-bottom: 30px; font-weight: 800; font-size: 3rem;">
                SISTEM PERINGATAN DINI BANJIR
            </h1>
            <p style="color: #dfe9ec !important; font-size: 1.4rem; font-weight: 400; line-height: 1.6; margin-bottom: 20px;">
                Platform monitoring dan prediksi banjir berbasis Artificial Intelligence<br>
                dan analisis statistik untuk mendukung mitigasi bencana.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("### Tentang Sistem")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <p>Sistem ini membantu memantau kondisi hujan dan ketinggian air untuk memberikan informasi awal mengenai potensi banjir. Data diperbarui secara berkala agar masyarakat dapat memperoleh informasi yang jelas dan terkini..</p>
                <ul style="color: #dfe9ec; padding-left: 20px;">
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h3>Manfaat Sistem ini?</h3>
                <ul style="color: #dfe9ec; padding-left: 20px;">
                    <li>Membantu meningkatkan kewaspadaan terhadap banjir</li>
                    <li>Mendukung persiapan dini dan pengambilan langkah pencegahan</li>
                    <li>Menyediakan informasi yang mudah dipahami dan diakses</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==================== KALKULATOR BANJIR PAGE ====================
def show_flood_calculator_page():
    st.markdown(
        """
        <div class="prediction-header">
            <h1 style="color: var(--accent) !important; margin-bottom: 15px; font-weight: 800;">Simulasi Banjir</h1>
            <p style="color: #dfe9ec !important; font-size: 1.2rem; font-weight: 400;">
                Masukkan parameter cuaca untuk mendapatkan prediksi risiko banjir yang akurat
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.container():
        st.markdown("### Parameter Cuaca")
        
        with st.form("flood_calculator_form", clear_on_submit=False):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Curah Hujan")
                rainfall = st.number_input(
                    "Curah Hujan (mm)",
                    min_value=0.0,
                    max_value=500.0,
                    value=100.0,
                    step=0.01,
                    format="%.2f",
                    help="Masukkan curah hujan dalam mm (0.00-500.00 mm)",
                    key="rainfall_input"
                )
                st.caption(f"Nilai: {rainfall:.2f} mm")
            
            with col2:
                st.markdown("#### Tinggi Air")
                water_level = st.number_input(
                    "Tinggi Air (mdpl)",
                    min_value=60.0,
                    max_value=150.0,
                    value=100.0,
                    step=0.01,
                    format="%.2f",
                    help="Masukkan tinggi air dalam mdpl (60.00-150.00 mdpl)",
                    key="water_input"
                )
                st.caption(f"Nilai: {water_level:.2f} mdpl")
            
            st.markdown("---")
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("#### Kelembapan")
                humidity = st.number_input(
                    "Kelembapan (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=70.0,
                    step=0.01,
                    format="%.2f",
                    help="Masukkan kelembapan dalam persen (0.00-100.00%)",
                    key="humidity_input"
                )
                st.caption(f"Nilai: {humidity:.2f}%")
            
            with col4:
                st.markdown("#### Suhu Harian")
                
                temp_col1, temp_col2 = st.columns(2)
                
                with temp_col1:
                    temp_min = st.number_input(
                        "Suhu Min (°C)",
                        min_value=-50.0,
                        max_value=50.0,
                        value=24.0,
                        step=0.1,
                        format="%.1f",
                        help="Suhu minimum harian (-50.0 sampai 50.0°C)",
                        key="temp_min_input"
                    )
                
                with temp_col2:
                    temp_max = st.number_input(
                        "Suhu Max (°C)",
                        min_value=-50.0,
                        max_value=50.0,
                        value=32.0,
                        step=0.1,
                        format="%.1f",
                        help="Suhu maksimum harian (-50.0 sampai 50.0°C)",
                        key="temp_max_input"
                    )
                
                if temp_max < temp_min:
                    st.error("⚠️ Suhu maksimum harus lebih besar atau sama dengan suhu minimum")
                    temp_max = temp_min
                
                temp_avg = (temp_min + temp_max) / 2
                st.caption(f"Rentang: {temp_min:.1f}°C – {temp_max:.1f}°C | Rata-rata: {temp_avg:.1f}°C")
            
            submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
            with submit_col2:
                submitted = st.form_submit_button(
                    "PREDIKSI SEKARANG",
                    use_container_width=True,
                    type="primary"
                )
    
    # ========== PREDIKSI TANPA GOOGLE SHEETS ==========
    if submitted:
        with st.spinner("Menganalisis data..."):
            time.sleep(0.8)
            
            try:
                rainfall_val = float(rainfall)
                water_level_val = float(water_level)
                humidity_val = float(humidity)
                temp_min_val = float(temp_min)
                temp_max_val = float(temp_max)
                
                result = predict_flood_ann_with_temp_range(
                    rainfall=rainfall_val,
                    water_level=water_level_val,
                    humidity=humidity_val,
                    temp_min=temp_min_val,
                    temp_max=temp_max_val
                )
                
                show_calculator_result(result, rainfall_val, water_level_val, 
                                    humidity_val, temp_min_val, temp_max_val)
                
            except Exception as e:
                st.error(f"Error dalam prediksi: {str(e)}")
                
                temp_avg = (float(temp_min) + float(temp_max)) / 2
                simple_risk = min(1.0, (float(rainfall) / 300) * 0.6 + (float(water_level) / 150) * 0.25 + (float(humidity) / 100) * 0.15)
                
                if simple_risk >= 0.7:
                    status = "TINGGI"
                    message = "WASPADA! Potensi banjir tinggi"
                elif simple_risk >= 0.4:
                    status = "MENENGAH"
                    message = "SIAGA! Pantau perkembangan"
                else:
                    status = "RENDAH"
                    message = "AMAN, tetap waspada"
                
                simple_result = {
                    'risk_level': round(simple_risk, 3),
                    'status': status,
                    'message': message,
                    'temperature_range': {'min': float(temp_min), 'max': float(temp_max), 'average': temp_avg}
                }
                
                show_calculator_result(simple_result, float(rainfall), float(water_level), 
                                    float(humidity), float(temp_min), float(temp_max))

def show_calculator_result(result, rainfall, water_level, humidity, temp_min, temp_max):
    """Tampilkan hasil kalkulator di website"""
    
    st.markdown("---")
    st.markdown("### HASIL PREDIKSI")
    st.caption("Berdasarkan parameter yang dimasukkan")
    
    status_colors = {
        'RENDAH': '#10b981',
        'MENENGAH': '#f59e0b',
        'TINGGI': '#ef4444'
    }
    
    risk_color = status_colors.get(result['status'], '#6b7280')
    risk_level = result.get('risk_level', 0.0)
    
    st.markdown(f"""
    <h1 style="color: {risk_color}; text-align: center; margin: 20px 0; font-size: 2.5rem;">
        {result['status']}
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align: center; font-size: 1.2rem; color: #dfe9ec; margin-bottom: 20px;">
        Risk Level: <strong>{risk_level:.3f}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 15px; margin: 20px 0;">
            <p style="color: #dfe9ec; margin: 0; font-size: 1.1rem; font-weight: 500; text-align: center;">
                {result.get('message', 'Prediksi risiko banjir')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("**Tingkat Risiko:**")
    progress_col1, progress_col2 = st.columns([4, 1])
    with progress_col1:
        st.progress(float(risk_level))
    with progress_col2:
        st.markdown(f"**{risk_level:.1%}**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 0.9rem;'>RENDAH<br>(0.0-0.5)</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 0.9rem;'>MENENGAH<br>(0.5-0.8)</p>", unsafe_allow_html=True)
    with col3:
        st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 0.9rem;'>TINGGI<br>(0.8-1.0)</p>", unsafe_allow_html=True)
    
    with st.expander("DETAIL PARAMETER INPUT", expanded=False):
        st.markdown("###  Parameter yang Dimasukkan")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(" Curah Hujan", f"{rainfall:.2f} mm")
            if rainfall > 200:
                st.error(">200 mm: HUJAN SANGAT LEBAT")
            elif rainfall > 100:
                st.warning("100-200 mm: HUJAN LEBAT")
            else:
                st.success("<100 mm: HUJAN NORMAL")
        
        with col2:
            st.metric("💧 Tinggi Air", f"{water_level:.2f} mdpl")
            if water_level > 130:
                st.error(">130 mdpl: TINGGI")
            elif water_level > 110:
                st.warning("110-130 mdpl: MENENGAH")
            else:
                st.success("<110 mdpl: NORMAL")
        
        with col3:
            st.metric(" Kelembapan", f"{humidity:.2f}%")
            if humidity > 80:
                st.warning(">80%: SANGAT LEMBAP")
            elif humidity > 60:
                st.info("60-80%: LEMBAP")
            else:
                st.success("<60%: NORMAL")
        
        with col4:
            temp_avg = (temp_min + temp_max) / 2
            st.metric(" Suhu Rata-rata", f"{temp_avg:.1f}°C")
            st.caption(f"Min: {temp_min:.1f}°C | Max: {temp_max:.1f}°C")
            if temp_avg > 30:
                st.error(">30°C: PANAS")
            elif temp_avg > 25:
                st.warning("25-30°C: HANGAT")
            else:
                st.success("<25°C: NORMAL")
    
    st.markdown("---")
    if st.button("🔄 Uji Parameter Lain", use_container_width=True, type="secondary"):
        st.rerun()

# ==================== CATATAN LAPORAN PAGE (MENU PEMILIHAN) ====================
def show_catatan_laporan_page():
    """Halaman utama Catatan Laporan (Menu pemilihan)"""
    st.markdown(
        """
        <div class="hero-section" style="padding: 30px; margin-bottom: 30px;">
            <h2 style="color: var(--accent) !important; margin-bottom: 15px; font-weight: 700;">Executive Dashboard: Laporan & Statistik</h2>
            <p style="color: #dfe9ec !important; font-size: 1.1rem; font-weight: 400;">
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div class="feature-card" style="cursor: pointer; text-align: center;">
                <h3> Harian</h3>
                <p>Laporan banjir yang tercatat hari ini</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Lihat Laporan Harian", key="go_harian_from_main", use_container_width=True):
            st.session_state.current_page = "Harian"
            st.rerun()
    
    with col2:
        st.markdown(
            """
            <div class="feature-card" style="cursor: pointer; text-align: center;">
                <h3> Bulanan</h3>
                <p>Laporan dan Statistik Tahunan</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Lihat Rekapan Bulanan", key="go_bulanan_from_main", use_container_width=True):
            st.session_state.current_page = "Bulanan"
            st.rerun()

# ==================== HARIAN PAGE (LAPORAN HARIAN) ====================
def show_harian_page():
    """Halaman Laporan Harian dengan tombol kembali"""
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("Kembali", key="back_from_harian", type="secondary"):
            st.session_state.current_page = "Catatan Laporan"
            st.rerun()
    
    st.markdown(
        """
        <div class="hero-section" style="padding: 30px; margin-bottom: 30px;">
            <h2 style="color: var(--accent) !important; margin-bottom: 15px; font-weight: 700;">Manajemen Laporan 24 jam</h2>
            <p style="color: #dfe9ec !important; font-size: 1.1rem; font-weight: 400;">
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    show_current_month_reports(flood_controller)

# ==================== BULANAN PAGE (REKAPAN BULANAN + STATISTIK 1 TAHUN) ====================
def show_bulanan_page():
    """Halaman Rekapan Bulanan dengan tombol kembali"""
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("Kembali", key="back_from_bulanan", type="secondary"):
            st.session_state.current_page = "Catatan Laporan"
            st.rerun()
    
    st.markdown(
        """
        <div class="hero-section" style="padding: 30px; margin-bottom: 30px;">
            <h2 style="color: var(--accent) !important; margin-bottom: 15px; font-weight: 700;">Sistem Monitoring & Evaluasi Laporan</h2>
            <p style="color: #dfe9ec !important; font-size: 1.1rem; font-weight: 400;">
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    tab1, tab2 = st.tabs([" Laporan Bulan Ini", " Statistik 1 Tahun"])
    
    with tab1:
        show_monthly_reports_summary(flood_controller)
    
    with tab2:
        st.markdown("### Statistik Laporan 1 Tahun")
        st.caption("Data historis laporan banjir selama 12 bulan terakhir")
        
        yearly_stats = flood_controller.get_yearly_statistics()
        months_data = yearly_stats.get('months_data', [])
        
        if not months_data:
            st.info(" Belum ada data laporan untuk 12 bulan terakhir.")
            st.info("Sistem akan menampilkan data secara otomatis ketika ada laporan baru.")
            return
        
        month_names = [item['month_name'] for item in months_data]
        report_counts = [item['report_count'] for item in months_data]
        is_current_flags = [item['is_current'] for item in months_data]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            total_reports_year = yearly_stats.get('total_reports', 0)
            st.metric("Total Laporan (1 Tahun)", total_reports_year)
        
        with col2:
            avg_per_month = yearly_stats.get('avg_per_month', 0)
            st.metric("Rata-rata per Bulan", f"{avg_per_month:.1f}")
        
        with col3:
            max_month = yearly_stats.get('max_month', "Tidak ada")
            max_count = yearly_stats.get('max_count', 0)
            st.metric("Bulan Tertinggi", f"{max_month} ({max_count})")
        
        st.markdown("---")
        
        st.markdown("#### Grafik Jumlah Laporan per Bulan")
        
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        colors = ['#ff6b6b' if is_current else '#00a8ff' 
                for is_current in is_current_flags]
        
        bars = ax.bar(month_names, report_counts, color=colors)
        
        for bar, count in zip(bars, report_counts):
            height = bar.get_height()
            if height > 0:  
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{int(count)}', ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel('Bulan', fontsize=12)
        ax.set_ylabel('Jumlah Laporan', fontsize=12)
        ax.set_title(f'Distribusi Laporan Banjir 12 Bulan Terakhir', fontsize=14, pad=20)
        ax.grid(axis='y', alpha=0.3)
        ax.set_axisbelow(True)
        
        plt.xticks(rotation=45)
        
        ax.set_ylim(bottom=0)
        
        plt.tight_layout()
        
        st.pyplot(fig)
        
        with st.expander(" Lihat Data Lengkap", expanded=False):
            import pandas as pd
            table_data = []
            for item in months_data:
                table_data.append({
                    'Bulan': item['month_name'],
                    'Periode': item['year_month'],
                    'Jumlah Laporan': item['report_count'],
                    'Status': 'Bulan Berjalan' if item['is_current'] else 'Bulan Sebelumnya'
                })
            
            if table_data:
                df = pd.DataFrame(table_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=" Download Data (CSV)",
                    data=csv,
                    file_name=f"statistik_laporan_{yearly_stats.get('current_year_month', '')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("Tidak ada data untuk ditampilkan")
        
        st.markdown("---")
        st.markdown("####  Analisis Tren")
        
        if len(report_counts) >= 2:
            current_count = report_counts[-1] if report_counts else 0
            prev_count = report_counts[-2] if len(report_counts) >= 2 else 0
            
            if prev_count > 0:
                change_percent = ((current_count - prev_count) / prev_count) * 100
                if change_percent > 0:
                    st.warning(f"⚠️ **Peningkatan {abs(change_percent):.1f}%** dari bulan sebelumnya")
                elif change_percent < 0:
                    st.success(f"✅ **Penurunan {abs(change_percent):.1f}%** dari bulan sebelumnya")
                else:
                    st.info(" **Stabil** - jumlah laporan sama dengan bulan sebelumnya")
            
            zero_months = [month for month, count in zip(month_names, report_counts) if count == 0]
            if zero_months:
                st.info(f" **Bulan tanpa laporan:** {', '.join(zero_months)}")

# ==================== PAGE HANDLERS LAINNYA ====================
def show_flood_report_page():
    st.markdown(
        """
        <div class="hero-section" style="padding: 30px; margin-bottom: 30px;">
            <h2 style="color: var(--accent) !important; margin-bottom: 15px; font-weight: 700;">Laporkan kondisi banjir di sekitar Anda untuk membantu kami melakukan langkah penanggulangan</h2>
            <p style="color: #dfe9ec !important; font-size: 1.1rem; font-weight: 400;">
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    show_flood_report_form(flood_controller)

def show_prediction_page():
    st.markdown(
        """
        <div class="hero-section" style="padding: 30px; margin-bottom: 30px;">
            <h2 style="color: var(--accent) !important; margin-bottom: 15px; font-weight: 700;">Prediksi Real-time</h2>
            <p style="color: #dfe9ec !important; font-size: 1.1rem; font-weight: 400;">
                Monitoring dan prediksi banjir berdasarkan data BBWS Bengawan Solo.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    show_prediction_dashboard(realtime_controller)

# ==================== MAIN APP ====================
def main():
    setup_sidebar()

    page_handlers = {
        "Home": show_homepage,
        "Panduan": show_panduan_page,  
        "Lapor Banjir": show_flood_report_page,
        "Catatan Laporan": show_catatan_laporan_page,
        "Harian": show_harian_page,
        "Bulanan": show_bulanan_page,
        "Prediksi Banjir": show_prediction_page,
        "Simulasi Banjir": show_flood_calculator_page
    }

    current_page = st.session_state.current_page
    handler = page_handlers.get(current_page, show_homepage)
    
    handler()

if __name__ == "__main__":
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    
    main()
