import numpy as np
import math

def predict_flood_gumbel(rainfall, return_period=10):
    """
    Prediksi menggunakan distribusi Gumbel untuk extreme value analysis
    """
    try:
        # Parameter Gumbel berdasarkan data historis
        mu = 85.0   # location parameter
        beta = 22.5 # scale parameter
        
        # Hitung probability menggunakan CDF Gumbel
        z = (rainfall - mu) / beta
        probability = math.exp(-math.exp(-z))
        
        # Risk level berdasarkan probability
        risk_level = min(1.0, probability * 1.5)
        
        # Tentukan status
        if risk_level >= 0.7:
            status = "TINGGI"
        elif risk_level >= 0.4:
            status = "MENENGAH"
        else:
            status = "RENDAH"
        
        return {
            'risk_level': round(risk_level, 3),
            'probability': round(probability, 4),
            'parameters_used': {
                'mu_location': mu,
                'beta_scale': beta,
                'return_period': return_period
            },
            'message': f'Distribusi Gumbel: Prob {probability:.1%}',
            'status': status
        }
        
    except Exception as e:
        return {
            'risk_level': 0.0,
            'probability': 0.0,
            'message': f'Error: {str(e)}',
            'status': 'ERROR'
        }
def get_gumbel_parameters():
    """Return parameter Gumbel untuk display di technical details"""
    return {
        'mu_location': 85.0,
        'beta_scale': 22.5,
        'distribution_type': 'Gumbel Type I (Extreme Value Type I)',
        'data_source': 'BMKG Historical Data 10 years',
        'application': 'Extreme flood prediction'
    }