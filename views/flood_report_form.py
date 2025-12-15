import streamlit as st

def show_flood_report_form(controller):
    """Display flood report form with simple design"""
    
    with st.container():
        st.markdown("### Isi Form Laporan")
        
        with st.form("flood_report_form"):
            # Form fields
            col1, col2 = st.columns(2)
            
            with col1:
                address = st.text_input(
                    "Alamat Lengkap",
                    placeholder="Jl/gang/kelurahan/kecamatan",
                    help="Masukkan alamat lengkap kejadian banjir"
                )
                
                flood_height = st.selectbox(
                    "Tinggi Banjir",
                    ["Pilih tinggi banjir", "Setinggi mata kaki", "Setinggi betis", "Setinggi lutut", "Lebih dari lutut"]
                )
            
            with col2:
                reporter_name = st.text_input(
                    "Nama Pelapor",
                    placeholder="Nama lengkap Anda"
                )
                
                reporter_phone = st.text_input(
                    "Nomor Telepon",
                    placeholder="0812-3456-7890",
                    help="Opsional, untuk konfirmasi"
                )
            
            # Photo upload
            photo_file = st.file_uploader(
                "Unggah Foto (**WAJIB**)",
                type=['jpg', 'jpeg', 'png'],
                help="Upload foto kondisi banjir jika tersedia"
            )
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button(
                    "Kirim Laporan",
                    type="primary",
                    use_container_width=True
                )
            
            if submitted:
                # Validation
                if not address or address.strip() == "":
                    st.error("Alamat harus diisi")
                elif flood_height == "Pilih tinggi banjir":
                    st.error("Pilih tinggi banjir")
                elif not reporter_name or reporter_name.strip() == "":
                    st.error("Nama pelapor harus diisi")
                else:
                    with st.spinner("Mengirim laporan..."):
                        try:
                            success, message = controller.submit_report(
                                address=address,
                                flood_height=flood_height,
                                reporter_name=reporter_name,
                                reporter_phone=reporter_phone,
                                photo_file=photo_file
                            )
                            
                            if success:
                                st.success(message)
                                st.info("Data Anda telah dicatat. Terima kasih atas laporannya.")
                            else:
                                st.error(message)
                        except Exception as e:
                            st.error(f"Terjadi kesalahan: {str(e)}")
