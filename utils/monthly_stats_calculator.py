from datetime import datetime
import pandas as pd

class MonthlyStatsCalculator:
    @staticmethod
    def calculate_from_reports(reports):
        """Calculate monthly statistics from reports"""
        if not reports:
            return {
                'total_reports': 0,
                'avg_risk': 0,
                'high_risk_days': 0,
                'most_affected_area': 'Tidak ada data',
                'response_time_avg': 0
            }
        
        # Hitung total reports
        total_reports = len(reports)
        
        # Hitung area paling sering
        area_counts = {}
        for report in reports:
            address = report.get('address', '')
            if address:
                # Extract jalan from address
                import re
                match = re.search(r'(Jl\.|Jalan)\s+([^,]+)', address)
                if match:
                    area = match.group(2).strip()
                    area_counts[area] = area_counts.get(area, 0) + 1
        
        most_affected_area = 'Tidak terdeteksi'
        if area_counts:
            most_affected_area = max(area_counts, key=area_counts.get)
        
        # Hitung hari dengan laporan
        dates = set()
        for report in reports:
            report_date = report.get('report_date', '')
            if report_date:
                dates.add(report_date)
        
        high_risk_days = len(dates) if dates else 0
        
        return {
            'total_reports': total_reports,
            'avg_risk': 0.0,  # Placeholder, bisa dihitung dari predictions
            'high_risk_days': high_risk_days,
            'most_affected_area': most_affected_area[:50],  # Limit length
            'response_time_avg': 45  # Placeholder
        }
    
    @staticmethod
    def calculate_from_predictions(predictions):
        """Calculate risk statistics from predictions"""
        if not predictions:
            return {
                'avg_risk': 0,
                'high_risk_count': 0,
                'risk_distribution': {}
            }
        
        risk_levels = []
        high_risk_count = 0
        status_count = {'RENDAH': 0, 'MENENGAH': 0, 'TINGGI': 0}
        
        for pred in predictions:
            risk = pred.get('Risk Level', 0)
            if isinstance(risk, str):
                try:
                    risk = float(risk)
                except:
                    risk = 0
            
            risk_levels.append(risk)
            
            status = pred.get('Status', '').upper()
            if status in status_count:
                status_count[status] += 1
            
            if risk >= 0.7:
                high_risk_count += 1
        
        avg_risk = sum(risk_levels) / len(risk_levels) if risk_levels else 0
        
        return {
            'avg_risk': round(avg_risk, 3),
            'high_risk_count': high_risk_count,
            'risk_distribution': status_count
        }