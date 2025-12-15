import streamlit as st
import sys, os, traceback

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Sistem Peringatan Dini Banjir",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# PATH SETUP
# ==================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
for p in [BASE_DIR, "controllers", "models", "views"]:
    path = os.path.join(BASE_DIR, p)
    if path not in sys.path and os.path.exists(path):
        sys.path.insert(0, path)

# ==================================================
# DATABASE INIT (SAFE)
# ==================================================
DB_PATH = "flood_system.db"
if not os.path.exists(DB_PATH):
    try:
        from init_tables import init_database
        init_database()
        st.success("✅ Database berhasil diinisialisasi")
    except Exception as e:
        st.error(f"Gagal init database: {e}")
        st.stop()

# ==================================================
# CONTROLLERS (SAFE FALLBACK)
# ==================================================
try:
    from controllers.VisitorController import VisitorController
    from controllers.FloodReportController import FloodReportController
    from controllers.RealTimeDataController import RealTimeDataController
except:
    class VisitorController: pass
    class FloodReportController: pass
    class RealTimeDataController: pass

visitor_controller = VisitorController()
flood_controller = FloodReportController()
realtime_controller = RealTimeDataController()

# ==================================================
# GLOBAL CSS (PROFESSIONAL)
# ==================================================
st.markdown("""
<style>
:root{
  --bg:#0b0f12;
  --panel:#0f1416;
  --accent:#00aee6;
  --border: rgba(255,255,255,0.05);
  --muted:#9aa6ad;
}

.stApp { background: var(--bg); color:#e8eef1; }

/* SIDEBAR */
[data-testid="stSidebar"]{
  background: var(--panel);
  border-right:1px solid var(--border);
}

/* HERO SECTION */
.hero-home{
  height:90vh;
  background:
    linear-gradient(rgba(5,15,30,.75), rgba(5,15,30,.65)),
    url("assets/hero.jpg");
  background-size:cover;
  background-position:center;
  border-radius:18px;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
  margin-bottom:60px;
}

.hero-home h1{
  font-size:64px;
  font-weight:900;
}

.hero-home p{
  font-size:22px;
  font-weight:600;
  max-width:900px;
  margin:auto;
}

/* CARDS */
.feature-card{
  background:linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
  border:1px solid var(--border);
  border-radius:14px;
  padding:24px;
  height:100%;
}

.feature-card h3{
  color:var(--accent);
  font-weight:900;
}

/* BUTTONS */
.stButton button{
  background:var(--accent);
  color:#041016;
  font-weight:800;
  border-radius:10px;
}

/* TEXT */
h1,h2,h3{ color:#f7fbfc; }
p,li{ color:#dfe9ec; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:16px">
            <div style="font-size:2.4rem;color:var(--accent)">🌊</div>
            <h2 style="margin:0;color:var(--accent)">SISTEM BANJIR</h2>
            <p style="color:var(--muted)">Early Warning System</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        if "page" not in st.session_state:
            st.session_state.page = "Home"

        menu = {
            "Home":"Home",
            "Lapor Banjir":"Lapor",
            "Prediksi":"Prediksi",
            "Analisis AI":"AI",
            "Analisis Statistik":"Statistik"
        }

        for k,v in menu.items():
            if st.button(k, use_container_width=True):
                st.session_state.page = v
                st.rerun()

# ==================================================
# HOME PAGE
# ==================================================
def show_homepage():
    st.markdown("""
    <div class="hero-home">
      <div>
        <h1>SISTEM PERINGATAN DINI BANJIR</h1>
        <p>
        Sistem monitoring dan prediksi banjir berbasis Artificial Intelligence
        dan analisis statistik untuk mendukung mitigasi bencana.
        </p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## FITUR UTAMA SISTEM")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>KECERDASAN BUATAN</h3>
        <ul>
          <li>Prediksi real-time</li>
          <li>Monitoring tinggi air</li>
          <li>Update otomatis</li>
          <li>Peringatan dini</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3>ANALISIS STATISTIK</h3>
        <ul>
          <li>Distribusi Gumbel</li>
          <li>Periode ulang banjir</li>
          <li>Validasi ekstrem</li>
          <li>Visualisasi data</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# PLACEHOLDER PAGES
# ==================================================
def simple_page(title):
    st.markdown(f"## {title}")
    st.info("Halaman ini siap dikembangkan.")

# ==================================================
# MAIN
# ==================================================
def main():
    sidebar()

    page = st.session_state.page
    if page == "Home":
        show_homepage()
    elif page == "Lapor":
        simple_page("Lapor Banjir")
    elif page == "Prediksi":
        simple_page("Prediksi Real-time")
    elif page == "AI":
        simple_page("Analisis AI")
    elif page == "Statistik":
        simple_page("Analisis Statistik")

main()
