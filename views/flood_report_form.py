import streamlit as st
import os

def show_flood_report_form(controller):
    LIMIT_HARIAN = 5
    today_count = controller.get_today_report_count()
    sisa = LIMIT_HARIAN - today_count

    st.markdown(f"""
        <div style='padding:12px;border-radius:8px;border:1px solid rgba(255,255,255,0.15);
        background:rgba(0,174,230,0.08);margin-bottom:15px;'>
            <h4 style='margin:0;color:#00aee6;'>📌 Kuota Laporan Harian</h4>
            <p style='margin:0;font-size:1.1rem;'>Sisa kuota: <b>{sisa}</b> laporan lagi.</p>
        </div>
    """, unsafe_allow_html=True)

    if sisa <= 0:
        st.error("❌ Kuota laporan hari ini sudah habis.")
        return


    # Upload Foto
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.subheader("📷 Upload Bukti Foto Banjir")
    st.markdown("**Format:** JPG, PNG, GIF • **Maksimal:** 5MB")
    st.markdown('</div>', unsafe_allow_html=True)
    
    photo_file = st.file_uploader(
        "Pilih file foto",
        type=['jpg', 'jpeg', 'png', 'gif'],
        help="Unggah foto bukti kejadian banjir",
        key="photo_uploader"
    )
    
    # File validation
    photo_file_valid = False
    if photo_file is not None:
        try:
            file_size = len(photo_file.getvalue()) / 1024 / 1024
            if file_size > 5:
                st.error(f"❌ File terlalu besar! {file_size:.2f}MB > 5MB")
            else:
                st.success(f"✅ File {photo_file.name} ({file_size:.2f}MB) siap diupload")
                photo_file_valid = True
        except:
            # Jika tidak bisa mendapatkan size, tetap anggap valid
            photo_file_valid = True
            st.success(f"✅ File {photo_file.name} siap diupload")
    
    st.divider()
    
    # Form Fields
    st.subheader("📝 Data Laporan (Wajib Diisi)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        address = st.text_input(
            "📍 Alamat yang terkena banjir *",
            placeholder="Contoh: Jl/gang/Desa RT XX RW XX",
            help="Masukkan alamat lengkap lokasi banjir",
            key="address_field"
        )
        
        flood_height = st.selectbox(
            "📏 Ketinggian banjir *",
            ["Pilih ketinggian banjir", "Setinggi mata kaki", "Setinggi betis", "Setinggi lutut", 
             "Setinggi paha", "Setinggi pinggang", "Setinggi dada", "Setinggi leher", "Lebih dari leher"],
            help="Pilih perkiraan ketinggian banjir",
            key="flood_height_field"
        )
    
    with col2:
        reporter_name = st.text_input(
            "👤 Nama Pelapor *", 
            placeholder="Masukkan nama lengkap",
            help="Nama lengkap pelapor",
            key="reporter_name_field"
        )
        
        reporter_phone = st.text_input(
            "📱 No. HP Pelapor",
            placeholder="Contoh: 08xxxxxxxxxxx",
            help="Nomor HP untuk konfirmasi (opsional)",
            key="reporter_phone_field"
        )
    
    # Validation
    address_valid = address and address.strip() != ""
    flood_height_valid = flood_height != "Pilih ketinggian banjir"
    reporter_name_valid = reporter_name and reporter_name.strip() != ""
    
    # PERUBAHAN: Foto opsional untuk testing
    is_form_valid = all([address_valid, flood_height_valid, reporter_name_valid])
    
    # Show validation status
    st.divider()
    st.subheader("Status Validasi Formulir")
    
    st.markdown('<div class="validation-box">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if address_valid:
            st.markdown('<p class="status-valid">• Alamat: ✅ Lengkap</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-invalid">• Alamat: ❌ Belum diisi</p>', unsafe_allow_html=True)
            
        if flood_height_valid:
            st.markdown('<p class="status-valid">• Tinggi Banjir: ✅ Dipilih</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-invalid">• Tinggi Banjir: ❌ Belum dipilih</p>', unsafe_allow_html=True)
    
    with col2:
        if reporter_name_valid:
            st.markdown('<p class="status-valid">• Nama Pelapor: ✅ Lengkap</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-invalid">• Nama Pelapor: ❌ Belum diisi</p>', unsafe_allow_html=True)
            
        if photo_file is not None:
            st.markdown('<p class="status-valid">• File Bukti: ✅ Terupload</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-valid">• File Bukti: ❌ Belum diisi</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Kembali", use_container_width=True, type="secondary"):
            st.session_state.current_page = "Home"
            st.rerun()
    
    with col2:
        submitted = st.button(
            "📤 Kirim Laporan", 
            use_container_width=True,
            type="primary",
            disabled=not is_form_valid
        )
    
    # Handle submission
    if submitted and is_form_valid:
        with st.spinner("🔄 Mengirim laporan..."):
            try:
                success, message = controller.submit_report(
                    address=address.strip(),
                    flood_height=flood_height,
                    reporter_name=reporter_name.strip(),
                    reporter_phone=reporter_phone.strip() if reporter_phone else None,
                    photo_file=photo_file
                )
                
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                    st.info("✅ Form berhasil dikirim! Anda bisa submit lagi jika perlu.")
                else:
                    st.error(f"❌ {message}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Close form container

    st.markdown('</div>', unsafe_allow_html=True)
