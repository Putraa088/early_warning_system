USER INTERFACE (app.py)
│
└── 📘 Panduan
│    └── views/panduan_page.py
│
├── 📝 Lapor Banjir
│   ├── views/flood_report_form.py
│   └── controllers/FloodReportController.py
│       ├── models/FloodReportModel.py (SQLite)
│       └── models/GoogleSheetsModel.py (Cloud)
│
├── 📋 Catatan Laporan
│   ├── views/flood_reports_table.py (Harian)
│   ├── views/monthly_reports.py (Bulanan)
│   └── controllers/FloodReportController.py
│
├── 📊 Prediksi Real-time
│   ├── views/prediction_dashboard.py
│   └── controllers/RealTimeDataController.py
│       ├── model_ann.py (AI)
│       └── gumbel_distribution.py (Stats)
│
└── 🧮 Simulasi Banjir
    └── model_ann.py (langsung)
