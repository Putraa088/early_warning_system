#!/usr/bin/env python3
"""
Test Google Sheets Connection - FINAL VERSION
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

def test_google_sheets():
    print("=" * 60)
    print("🧪 FINAL GOOGLE SHEETS TEST")
    print("=" * 60)
    
    try:
        from models.GoogleSheetsModel import GoogleSheetsModel
        
        print("1. Initializing GoogleSheetsModel...")
        model = GoogleSheetsModel()
        
        if not model.client:
            print("❌ Google Sheets not connected")
            return False
        
        print("✅ Google Sheets connected successfully!")
        
        # Test saving data
        print("\n2. Testing data save...")
        test_data = {
            'address': 'Jl. Test Connection Final',
            'flood_height': 'Setinggi lutut',
            'reporter_name': 'Test User Final',
            'reporter_phone': '08123456789',
            'ip_address': '192.168.1.100',
            'photo_url': 'test_final.jpg'
        }
        
        success = model.save_flood_report(test_data)
        if success:
            print("✅ Test data saved to Google Sheets!")
        else:
            print("❌ Failed to save test data")
            return False
        
        # Test retrieving data
        print("\n3. Testing data retrieval...")
        reports = model.get_recent_reports(limit=5)
        print(f"✅ Retrieved {len(reports)} recent reports")
        
        if reports:
            print("\n📋 Latest reports:")
            for i, report in enumerate(reports[-3:], 1):  # Last 3 reports
                print(f"  {i}. {report['address']} - {report['reporter_name']}")
        
        print("\n" + "=" * 60)
        print("🎉 GOOGLE SHEETS TEST PASSED!")
        print("\n🎯 Verification Steps:")
        print("1. Open your Google Sheets")
        print("2. Check worksheet 'flood_reports'")
        print("3. Should see new test data at the bottom")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_google_sheets()
    if not success:
        print("\n🔧 Troubleshooting:")
        print("1. Check credentials.json file exists")
        print("2. Verify private key format (proper newlines)")
        print("3. Check spreadsheet ID is correct")
        print("4. Ensure service account has editor access to spreadsheet")
        sys.exit(1)
