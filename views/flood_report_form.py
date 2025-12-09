import streamlit as st
import os

def show_flood_report_form(controller):
    """Display flood report form dengan tema hitam"""
    
    st.markdown("""
    <style>
    .form-container {
        background: linear-gradient(145deg, #1a1a1a, #222222);
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin: 20px 0;
        border: 1px solid #333333;
    }
    
    .form-title {
        color: #00a8ff;
        text-align: center;
        margin-bottom: 25px;
        font-size: 1.8em;
        font-weight: 700;
        border-bottom: 2px solid #00a8ff;
        padding-bottom: 10px;
    }
    
    .upload-section {
        background: #2a2a2a;
        border: 2px dashed #444444;
        border-radius: 10px;
        padding: 25px;
        text-align: center;
        margin: 20px 0;
        color: #cccccc;
    }
    
    .upload-section:hover {
        border-color: #00a8ff;
        background: #333333;
    }
    
    .status-valid {
        color: #00d26a;
        font-weight: bold;
    }
    
    .status-invalid {
        color: #ff4b4b;
        font-weight: bold;
    }
    
    .validation-box {
        background: #2a2a2a;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #00a8ff;
        margin: 15px 0;
        color: #cccccc;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Form Container
    st.markdown("""
    <div class="form-container">
        <div class="form-title">📋 FORM LAPORAN BANJIR</div>
    """, unsafe_allow_html=True)

    # Check daily limit
    try:
        client_ip = controller.get_client_ip()
        can_submit = controller.check_daily_limit(client_ip)
        
        if not can_submit:
            st.error("❌ Maaf, Anda telah mencapai batas maksimal 10 laporan per hari. Silakan kembali besok.")
            st.markdown('</div>', unsafe_allow_html=True)
            return
    except:
        pass

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