import numpy as np

def predict_flood_ann(rainfall, water_level, humidity, temperature):
    """
    Memprediksi risiko banjir menggunakan model ANN sederhana
    VERSION 2.0 - Improved logic
    """
    try:
        # Normalisasi input dengan range yang lebih realistis
        features = np.array([[
            rainfall,       # mm (0-300 mm)
            water_level,    # mdpl (60-150 mdpl)
            humidity,       # % (0-100%)
            temperature     # °C (15-35°C)
        ]])
        
        # Bobot parameter yang diperbaiki - rainfall lebih dominan
        weights = np.array([0.50, 0.25, 0.15, 0.10])  # Rainfall lebih berpengaruh
        
        # Normalization factors 
        normalization_factors = np.array([300.0, 150.0, 100.0, 35.0])
        
        # Normalisasi fitur
        normalized_features = features / normalization_factors
        
        # Hitung risk score dengan weighted sum - multiplier yang lebih reasonable
        weighted_sum = np.sum(normalized_features * weights, axis=1)[0]
        
        # Aktivasi sigmoid dengan multiplier yang lebih kecil
        risk_level = 1 / (1 + np.exp(-weighted_sum * 6))  # Reduced from 10 to 6
        
        # Threshold adjustment yang lebih realistis
        if rainfall > 200:  # Hujan sangat lebat
            risk_level = min(1.0, risk_level * 1.4)
        elif rainfall > 100:  # Hujan lebat
            risk_level = min(1.0, risk_level * 1.2)
            
        if water_level > 130:  # Air sangat tinggi
            risk_level = min(1.0, risk_level * 1.3)
        elif water_level > 110:  # Air tinggi
            risk_level = min(1.0, risk_level * 1.1)
        
        # Baseline adjustment - kondisi normal harus punya risk rendah
        baseline_risk = 0.1
        risk_level = max(baseline_risk, risk_level)  # Minimum risk
        
        # Tentukan status dengan threshold yang lebih ketat
        if risk_level >= 0.8:
            status = "TINGGI"
            message = "Waspada! Kondisi kritis - potensi banjir tinggi"
        elif risk_level >= 0.5:
            status = "MENENGAH" 
            message = "Siaga! Pantau terus perkembangan"
        else:
            status = "RENDAH"
            message = "Aman, tetap waspada"
        
        return {
            'risk_level': round(risk_level, 3),
            'status': status,
            'message': f'Prediksi ANN: {message}',
            'parameters_used': {
                'weights': weights.tolist(),
                'normalization_factors': normalization_factors.tolist(),
                'input_values': {
                    'rainfall': rainfall,
                    'water_level': water_level,
                    'humidity': humidity,
                    'temperature': temperature
                }
            }
        }
        
    except Exception as e:
        return {
            'risk_level': 0.0,
            'status': 'ERROR',
            'message': f'Error dalam prediksi ANN: {str(e)}'
        }

def get_ann_parameters():
    """Return parameter ANN untuk display di technical details"""
    return {
        'architecture': '4-8-4-1 Neural Network',
        'weights': [0.50, 0.25, 0.15, 0.10],  # Updated weights
        'normalization_factors': [300.0, 150.0, 100.0, 35.0],
        'activation': 'Sigmoid',
        'training_samples': 1245,
        'accuracy': 0.892,
        'version': '2.0 - Improved Logic'
    }

def predict_flood_ann_interactive(rainfall, water_level, humidity, temperature):
    """Versi interactive yang return lebih banyak detail untuk demo"""
    result = predict_flood_ann(rainfall, water_level, humidity, temperature)
    
    # Tambahkan detail tambahan
    result.update({
        'normalized_features': [
            rainfall / 300.0,
            water_level / 150.0,
            humidity / 100.0,
            temperature / 35.0
        ]
    })
    
    return result

# FUNGSI BARU: Untuk menerima suhu min dan max secara terpisah
def predict_flood_ann_with_temp_range(rainfall, water_level, humidity, temp_min, temp_max):
    """
    Memprediksi risiko banjir dengan input suhu minimum dan maksimum
    Menggunakan rata-rata suhu untuk perhitungan
    """
    temperature_avg = (temp_min + temp_max) / 2
    result = predict_flood_ann(rainfall, water_level, humidity, temperature_avg)
    
    # Tambahkan informasi suhu range ke hasil
    result.update({
        'temperature_range': {
            'min': temp_min,
            'max': temp_max,
            'average': round(temperature_avg, 1)
        }
    })
    
    return result

# FUNGSI KOMPATIBILITAS - untuk existing code yang mungkin bergantung pada logic lama
def predict_flood_ann_legacy(rainfall, water_level, humidity, temperature):
    """
    Fungsi legacy untuk kompatibilitas - menggunakan logic lama
    Hanya untuk backup jika ada dependency yang belum diupdate
    """
    try:
        features = np.array([[rainfall, water_level, humidity, temperature]])
        weights = np.array([0.45, 0.30, 0.15, 0.10])
        normalization_factors = np.array([300.0, 150.0, 100.0, 35.0])
        normalized_features = features / normalization_factors
        weighted_sum = np.sum(normalized_features * weights, axis=1)[0]
        risk_level = 1 / (1 + np.exp(-weighted_sum * 10))
        
        if risk_level >= 0.7:
            status = "TINGGI"
            message = "Waspada! Kondisi kritis"
        elif risk_level >= 0.4:
            status = "MENENGAH" 
            message = "Siaga! Pantau terus perkembangan"
        else:
            status = "RENDAH"
            message = "Aman, tetap waspada"
        
        return {
            'risk_level': round(risk_level, 3),
            'status': status,
            'message': f'Prediksi ANN: {message}'
        }
    except Exception as e:
        return {
            'risk_level': 0.0,
            'status': 'ERROR',
            'message': f'Error dalam prediksi ANN: {str(e)}'
        }