flood-monitoring-system/
├── app.py
├── panduan/
│   └── views/
│       └── panduan_page.py
├── lapor_banjir/
│   ├── views/
│   │   └── flood_report_form.py
│   └── controllers/
│       └── FloodReportController.py
│           ├── models/
│           │   ├── FloodReportModel.py
│           │   └── GoogleSheetsModel.py
├── catatan_laporan/
│   ├── views/
│   │   ├── flood_reports_table.py
│   │   └── monthly_reports.py
│   └── controllers/
│       └── FloodReportController.py
├── prediksi_realtime/
│   ├── views/
│   │   └── prediction_dashboard.py
│   └── controllers/
│       └── RealTimeDataController.py
│           ├── model_ann.py
│           └── gumbel_distribution.py
└── simulasi_banjir/
    └── model_ann.py
