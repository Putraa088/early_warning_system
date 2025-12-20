import streamlit as st

def show_flood_report_form(controller):
    """Display flood report form with simple design"""
    
    with st.container():
        st.markdown("###  Form Laporan Banjir")
        st.caption("Isi form di bawah untuk melaporkan kondisi banjir di sekitar Anda")
        
        with st.form("flood_report_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                address = st.text_input(
                    "Alamat Lengkap*",
                    placeholder="Jl/Gang/Kelurahan/Kecamatan",
                    help="Masukkan alamat lengkap kejadian banjir"
                )
                
                flood_height = st.selectbox(
                    "Tinggi Banjir*",
                    ["Pilih tinggi banjir", "Setinggi mata kaki", "Setinggi betis", 
                    "Setinggi lutut", "Lebih dari lutut"]
                )
            
            with col2:
                reporter_name = st.text_input(
                    "Nama Pelapor*",
                    placeholder="Nama lengkap Anda"
                )
                
                reporter_phone = st.text_input(
                    "Nomor Telepon* ",
                    placeholder="0812-3456-7890",
                    help="untuk konfirmasi"
                )
            
            
            photo_file = st.file_uploader(
                "Unggah Foto (**WAJIB**)",
                type=['jpg', 'jpeg', 'png'],
                help="Upload foto kondisi banjir jika tersedia"
            )
            
            
            submitted = st.form_submit_button(
                " Kirim Laporan",
                type="primary",
                use_container_width=True
            )
            
            if submitted:
                st.write("---")
                st.info(" Memproses laporan....")
                
                errors = []
                
                if not address or address.strip() == "":
                    errors.append("❌ Alamat harus diisi")
                
                if flood_height == "Pilih tinggi banjir":
                    errors.append("❌ Pilih tinggi banjir")
                
                if not reporter_name or reporter_name.strip() == "":
                    errors.append("❌ Nama pelapor harus diisi")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    
                    try:
                        success, message = controller.submit_report(
                            address=address.strip(),
                            flood_height=flood_height,
                            reporter_name=reporter_name.strip(),
                            reporter_phone=reporter_phone.strip() if reporter_phone else None,
                            photo_file=photo_file
                        )
                        
                        if success:
                            st.success(message)

                        else:
                            st.error(message)
                            
                    except Exception as e:
                        st.error(f"❌ Terjadi kesalahan sistem: {str(e)}")
                        st.info("Silakan coba lagi atau hubungi admin.")
