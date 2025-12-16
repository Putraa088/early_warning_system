import streamlit as st

def show_flood_report_form(controller):
    """Show flood report form with dropdown for flood height"""
    
    st.markdown("### Formulir Laporan Banjir")
    
    with st.form("flood_report_form"):
        # Input alamat
        address = st.text_area(
            "Lokasi Kejadian*",
            placeholder="Contoh: Jl. Diponegoro No. 52, Salatiga, Jawa Tengah",
            help="Sebutkan lokasi kejadian banjir dengan jelas",
            value="Somopuro Lor"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # DROPDOWN untuk tinggi banjir dengan default value
            flood_options = {
                "": 0,  # Pilihan kosong
                "Rendah (10-30 cm)": 20,
                "Sedang (31-70 cm)": 50,
                "Tinggi (71-150 cm)": 100,
                "Sangat Tinggi (>150 cm)": 200
            }
            
            flood_height_text = st.selectbox(
                "Tinggi Banjir*",
                options=list(flood_options.keys()),
                help="Pilih kategori tinggi banjir",
                index=0
            )
            
            # Ambil nilai numerik dari pilihan
            flood_height = flood_options[flood_height_text]
            
            # Tampilkan nilai yang dipilih
            if flood_height > 0:
                st.info(f"Tinggi banjir: {flood_height} cm")
            else:
                st.warning("⚠️ Pilih tinggi banjir")
        
        with col2:
            reporter_name = st.text_input(
                "Nama Pelapor*",
                placeholder="Nama lengkap pelapor",
                help="Nama Anda sebagai pelapor",
                value="Settings! Betis"
            )
        
        # PERUBAHAN 1: Nomor Telepon menjadi WAJIB
        reporter_phone = st.text_input(
            "Nomor Telepon*",  # UBAH: hapus (Opsional)
            placeholder="081234567890",
            help="Nomor telepon untuk konfirmasi (wajib diisi)",
            value="883719843916"
        )
        
        # PERUBAHAN 2: Foto Kejadian menjadi WAJIB
        photo_file = st.file_uploader(
            "Foto Kejadian (WAJIB)*",  # UBAH: (WAJIB)*
            type=['jpg', 'jpeg', 'png', 'gif'],
            help="Upload foto kejadian banjir (wajib diisi)"
        )
        
        if photo_file:
            st.image(photo_file, caption="Pratinjau Foto", width=300)
            st.success("✅ Foto berhasil diupload")
        else:
            st.warning("⚠️ Harap upload foto kejadian")
        
        # Terms and conditions
        st.markdown("---")
        agreed = st.checkbox(
            "Saya menyetujui bahwa data yang saya berikan adalah benar dan dapat dipertanggungjawabkan*"
        )
        
        # Submit button
        submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
        with submit_col2:
            submitted = st.form_submit_button(
                "📤 KIRIM LAPORAN",
                use_container_width=True,
                type="primary",
                disabled=not agreed
            )
        
        if submitted:
            # VALIDASI: Cek semua field wajib
            error_messages = []
            
            if not address or address.strip() == "":
                error_messages.append("📍 Lokasi kejadian harus diisi")
            
            if flood_height <= 0:
                error_messages.append("🌊 Pilih tinggi banjir")
            
            if not reporter_name or reporter_name.strip() == "":
                error_messages.append("👤 Nama pelapor harus diisi")
            
            # VALIDASI NOMOR TELEPON (WAJIB)
            if not reporter_phone or reporter_phone.strip() == "":
                error_messages.append("📱 Nomor telepon harus diisi")
            elif not reporter_phone.strip().isdigit() or len(reporter_phone.strip()) < 10:
                error_messages.append("📱 Nomor telepon harus angka minimal 10 digit")
            
            # VALIDASI FOTO (WAJIB)
            if photo_file is None:
                error_messages.append("📷 Foto kejadian wajib diupload")
            
            if error_messages:
                for error in error_messages:
                    st.error(error)
            else:
                with st.spinner("Mengirim laporan..."):
                    success, message = controller.submit_report(
                        address=address.strip(),
                        flood_height=float(flood_height),
                        reporter_name=reporter_name.strip(),
                        reporter_phone=reporter_phone.strip(),
                        photo_file=photo_file
                    )
                    
                    if success:
                        st.success(message)
                        st.balloons()
                        # Auto reset form
                        st.rerun()
                    else:
                        st.error(message)
