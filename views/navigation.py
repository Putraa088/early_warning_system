import streamlit as st

def show_sticky_navigation():
    """Display sticky horizontal navigation dengan dropdown"""
    
    st.markdown("""
    <nav class="sticky-nav">
        <div class="nav-container">
            <ul class="nav-menu">
                <li class="nav-item">
                    <a class="nav-link %s" onclick="handleNavClick('Home')">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link %s" onclick="handleNavClick('Lapor Banjir')">Lapor Banjir</a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link %s">Catatan Banjir ▼</a>
                    <div class="dropdown-content">
                        <a onclick="handleNavClick('Catatan Banjir Hari Ini')">Catatan Banjir Hari Ini</a>
                        <a onclick="handleNavClick('Catatan Banjir Bulan Ini')">Catatan Banjir Bulan Ini</a>
                    </div>
                </li>
                <li class="nav-item">
                    <a class="nav-link %s" onclick="handleNavClick('Prediksi Banjir')">Prediksi Banjir</a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link %s">Analisis Prediktif ▼</a>
                    <div class="dropdown-content">
                        <a onclick="handleNavClick('Analisis ANN + Hasil Prediksi')">Analisis ANN + Hasil Prediksi</a>
                        <a onclick="handleNavClick('Analisis Gumbel + Hasil Prediksi')">Analisis Gumbel + Hasil Prediksi</a>
                    </div>
                </li>
            </ul>
        </div>
    </nav>
    
    <div class="main-content">
    """ % (
        "active" if st.session_state.get('current_page') == 'Home' else "",
        "active" if st.session_state.get('current_page') == 'Lapor Banjir' else "",
        "active" if st.session_state.get('current_page') in ['Catatan Banjir Hari Ini', 'Catatan Banjir Bulan Ini'] else "",
        "active" if st.session_state.get('current_page') == 'Prediksi Banjir' else "",
        "active" if st.session_state.get('current_page') in ['Analisis ANN + Hasil Prediksi', 'Analisis Gumbel + Hasil Prediksi'] else ""
    ), unsafe_allow_html=True)