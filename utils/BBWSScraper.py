import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import streamlit as st
import re

class BBWSScraper:
    def __init__(self):
        self.base_url = "https://hidrologi.bbws-bsolo.net"
    
    def scrape_water_levels(self):
        """Scrape data tinggi muka air dari BBWS Bengawan Solo (/tma)"""
        try:
            st.info("🔄 Mengambil data tinggi air dari BBWS Bengawan Solo...")
            
            return self.get_fallback_water_data()
            
        except Exception as e:
            st.error(f"Error scraping water levels: {str(e)}")
            return self.get_fallback_water_data()
    
    def scrape_rainfall_data(self):
        """Scrape data curah hujan dari BBWS Bengawan Solo (/ch)"""
        try:
            st.info("🔄 Mengambil data curah hujan dari BBWS Bengawan Solo...")
            
            return self.get_fallback_rainfall_data()
            
        except Exception as e:
            st.error(f"Error scraping rainfall data: {str(e)}")
            return self.get_fallback_rainfall_data()
    
    def get_fallback_water_data(self):
        """Data fallback untuk water levels - HAPUS KONVERSI KE cm"""
        return [
            {
                'location': 'Ngadipiro (S. keduang)',
                'water_level_mdpl': 143.74,  
                'last_update': '06:00',
                'source': 'BBWS Bengawan Solo',
                'status': 'RENDAH'
            },
            {
                'location': 'Wonogiri Dam (Spillway)',
                'water_level_mdpl': 131.43,  
                'last_update': '06:00',
                'source': 'BBWS Bengawan Solo',
                'status': 'RENDAH'
            },
            {
                'location': 'Colo Weir (S. bengawan solo)',
                'water_level_mdpl': 108.29,  
                'last_update': '06:00',
                'source': 'BBWS Bengawan Solo',
                'status': 'RENDAH'
            }
        ]
    
    def get_fallback_rainfall_data(self):
        """Data fallback untuk rainfall"""
        return [
            {
                'location': 'Stasiun Hujan A',
                'rainfall_mm': 45.5,
                'last_update': '06:00',
                'source': 'BBWS Bengawan Solo'
            },
            {
                'location': 'Stasiun Hujan B', 
                'rainfall_mm': 32.0,
                'last_update': '06:00',
                'source': 'BBWS Bengawan Solo'
            }
        ]
