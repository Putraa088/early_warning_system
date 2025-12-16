from GoogleSheetsModel import GoogleSheetsModel

print("🧪 Testing Google Sheets Connection...")
model = GoogleSheetsModel()

if model.client:
    print("✅ Google Sheets connected!")
    
    # Test worksheet
    ws = model.get_worksheet("flood_reports")
    if ws:
        print(f"✅ Worksheet: {ws.title}")
        
        # Get all headers
        all_values = ws.get_all_values()
        if all_values:
            print(f"✅ Headers: {all_values[0]}")
            print(f"✅ Total rows: {len(all_values)}")
            
            # Test append
            test_data = {
                'address': 'Jl. Test Connection',
                'flood_height': 'Setinggi lutut',
                'reporter_name': 'Test User',
                'reporter_phone': '08123456789',
                'ip_address': '192.168.1.100',
                'photo_url': 'test.jpg'
            }
            
            success = model.save_flood_report(test_data)
            print(f"✅ Test save: {success}")
    else:
        print("❌ Worksheet not found")
else:
    print("❌ Google Sheets not connected")