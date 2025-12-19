import streamlit as st
import sys
import os

# Tambahkan path ke sys.path
sys.path.append(os.path.dirname(__file__))

from controllers.FloodReportController import FloodReportController

def test_form():
    st.title("🧪 TEST FORM LAPORAN BANJIR")
    
    controller = FloodReportController()
    
    with st.form("test_form"):
        st.subheader("Test Data Input")
        
        address = st.text_input("Alamat", "Jl. Test 123")
        flood_height = st.selectbox("Tinggi Banjir", 
                                ["Setinggi mata kaki", "Setinggi betis", "Setinggi lutut"])
        reporter_name = st.text_input("Nama Pelapor", "Test User")
        reporter_phone = st.text_input("No HP", "08123456789")
        
        submitted = st.form_submit_button("Test Submit")
        
        if submitted:
            st.info("Mengirim data test...")
            
            success, message = controller.submit_report(
                address=address,
                flood_height=flood_height,
                reporter_name=reporter_name,
                reporter_phone=reporter_phone,
                photo_file=None  # No file for test
            )
            
            if success:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")

if __name__ == "__main__":
    test_form()