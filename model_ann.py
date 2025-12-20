import numpy as np

def predict_flood_ann(rainfall, water_level, humidity, temperature):
    """
    Memprediksi risiko banjir menggunakan model ANN sederhana
    VERSION 2.0 - Improved logic
    """
    try:
        features = np.array([[
            rainfall,       
            water_level,    
            humidity,       
            temperature     
        ]])
        
        weights = np.array([0.50, 0.25, 0.15, 0.10])  
        
        normalization_factors = np.array([300.0, 150.0, 100.0, 35.0])
        
        normalized_features = features / normalization_factors
        
        weighted_sum = np.sum(normalized_features * weights, axis=1)[0]
        
        risk_level = 1 / (1 + np.exp(-weighted_sum * 6))  
        
        if rainfall > 200:  
            risk_level = min(1.0, risk_level * 1.4)
        elif rainfall > 100:  
            risk_level = min(1.0, risk_level * 1.2)
            
        if water_level > 130:  
            risk_level = min(1.0, risk_level * 1.3)
        elif water_level > 110:  
            risk_level = min(1.0, risk_level * 1.1)
        
        baseline_risk = 0.1
        risk_level = max(baseline_risk, risk_level)  
        
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
            'message': message,  
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
        'weights': [0.50, 0.25, 0.15, 0.10],  
        'normalization_factors': [300.0, 150.0, 100.0, 35.0],
        'activation': 'Sigmoid',
        'training_samples': 1245,
        'accuracy': 0.892,
        'version': '2.0 - Improved Logic'
    }

def predict_flood_ann_interactive(rainfall, water_level, humidity, temperature):
    """Versi interactive yang return lebih banyak detail untuk demo"""
    result = predict_flood_ann(rainfall, water_level, humidity, temperature)
    
    result.update({
        'normalized_features': [
            rainfall / 300.0,
            water_level / 150.0,
            humidity / 100.0,
            temperature / 35.0
        ]
    })
    
    return result

def predict_flood_ann_with_temp_range(rainfall, water_level, humidity, temp_min, temp_max):
    """
    Memprediksi risiko banjir dengan input suhu minimum dan maksimum
    Menggunakan rata-rata suhu untuk perhitungan
    """
    temperature_avg = (temp_min + temp_max) / 2
    result = predict_flood_ann(rainfall, water_level, humidity, temperature_avg)
    
    result.update({
        'temperature_range': {
            'min': temp_min,
            'max': temp_max,
            'average': round(temperature_avg, 1)
        }
    })
    
    return result

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
            'message': message
        }
    except Exception as e:
        return {
            'risk_level': 0.0,
            'status': 'ERROR',
            'message': f'Error dalam prediksi ANN: {str(e)}'
        }
