flood-monitoring-system/
│
├── app.py  # Main application entry point
│
├── panduan/
│   └── views/
│       └── panduan_page.py  # Guide/help page
│
├── lapor_banjir/
│   ├── views/
│   │   └── flood_report_form.py  # Flood reporting form UI
│   │
│   └── controllers/
│       └── FloodReportController.py  # Controls flood report logic
│           │
│           └── models/
│               ├── FloodReportModel.py  # Local database (SQLite) operations
│               └── GoogleSheetsModel.py  # Cloud synchronization (Google Sheets)
│
├── catatan_laporan/
│   ├── views/
│   │   ├── flood_reports_table.py  # Daily reports table view
│   │   └── monthly_reports.py  # Monthly reports view
│   │
│   └── controllers/
│       └── FloodReportController.py  # Shared controller for reports
│
├── prediksi_realtime/
│   ├── views/
│   │   └── prediction_dashboard.py  # Real-time prediction dashboard UI
│   │
│   └── controllers/
│       └── RealTimeDataController.py  # Manages real-time data processing
│           │
│           ├── model_ann.py  # Artificial Neural Network for predictions
│           └── gumbel_distribution.py  # Statistical analysis using Gumbel distribution
│
└── simulasi_banjir/
    └── model_ann.py  # Direct ANN model for flood simulations
