def get_monthly_stats(controller):
    import sqlite3
    import pandas as pd

    conn = sqlite3.connect("flood_system.db")
    df = pd.read_sql_query("""
        SELECT DATE(timestamp) AS tgl, COUNT(*) AS jumlah
        FROM flood_reports
        WHERE strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')
        GROUP BY DATE(timestamp)
        ORDER BY tgl
    """, conn)
    conn.close()
    return df
    
def show_monthly_reports_summary(controller):
    import streamlit as st
    import pandas as pd

    df = get_monthly_stats(controller)

    if df.empty:
        st.info("Belum ada laporan di bulan ini.")
        return

    total = df["jumlah"].sum()
    rata = df["jumlah"].mean()
    puncak = df.loc[df["jumlah"].idxmax()]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Laporan Bulanan", total)
    col2.metric("Rata-rata Laporan / Hari", f"{rata:.2f}")
    col3.metric("Puncak Laporan", f"{puncak['tgl']} ( {puncak['jumlah']} laporan )")

    st.markdown("### Grafik Jumlah Laporan Harian")
    st.bar_chart(df.set_index("tgl"))
