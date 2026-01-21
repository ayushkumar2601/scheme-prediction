"""
Test Export Functionality
Quick test to verify all export formats work correctly
"""

print("Testing Export Functionality...")
print("=" * 60)

# Test imports
print("\n1. Testing imports...")
try:
    from export_utils import export_manager
    print("   ✓ export_utils imported successfully")
except ImportError as e:
    print(f"   ✗ Error importing export_utils: {e}")
    exit(1)

try:
    from reportlab.lib.pagesizes import letter
    print("   ✓ reportlab imported successfully")
except ImportError:
    print("   ✗ reportlab not installed. Run: pip install reportlab")
    exit(1)

try:
    import openpyxl
    print("   ✓ openpyxl imported successfully")
except ImportError:
    print("   ✗ openpyxl not installed. Run: pip install openpyxl")
    exit(1)

try:
    from pptx import Presentation
    print("   ✓ python-pptx imported successfully")
    pptx_available = True
except ImportError:
    print("   ⚠ python-pptx not installed. PowerPoint export will be disabled.")
    print("     To enable: pip install python-pptx")
    pptx_available = False

# Create sample data
print("\n2. Creating sample data...")
sample_data = {
    'summary': {
        'total_people_affected': 1500000,
        'total_enrolments': 900000,
        'total_updates': 600000,
        'peak_date': '2025-04-15',
        'peak_volume': 75000,
        'duration_days': 45
    },
    'regional_impact': [
        {
            'state': 'Maharashtra',
            'predicted_enrolments': 150000,
            'predicted_updates': 100000,
            'total_impact': 250000,
            'pct_increase': 35.5,
            'risk_level': 'High'
        },
        {
            'state': 'Uttar Pradesh',
            'predicted_enrolments': 200000,
            'predicted_updates': 120000,
            'total_impact': 320000,
            'pct_increase': 42.0,
            'risk_level': 'High'
        },
        {
            'state': 'Karnataka',
            'predicted_enrolments': 80000,
            'predicted_updates': 50000,
            'total_impact': 130000,
            'pct_increase': 28.0,
            'risk_level': 'Medium'
        }
    ],
    'daily_impact': [
        {'date': '2025-04-01', 'enrolments': 20000, 'updates': 15000, 'total': 35000},
        {'date': '2025-04-02', 'enrolments': 22000, 'updates': 16000, 'total': 38000},
        {'date': '2025-04-03', 'enrolments': 25000, 'updates': 18000, 'total': 43000}
    ],
    'risk_assessment': {
        'high_risk_states': ['Maharashtra', 'Uttar Pradesh'],
        'medium_risk_states': ['Karnataka', 'Tamil Nadu'],
        'low_risk_states': ['Goa', 'Sikkim']
    }
}
print("   ✓ Sample data created")

# Test PDF Export
print("\n3. Testing PDF export...")
try:
    pdf_buffer = export_manager.export_to_pdf(
        sample_data,
        "Test Policy",
        None
    )
    print(f"   ✓ PDF generated successfully ({len(pdf_buffer.getvalue())} bytes)")
    
    # Save test file
    with open('test_export_report.pdf', 'wb') as f:
        f.write(pdf_buffer.getvalue())
    print("   ✓ Test PDF saved as 'test_export_report.pdf'")
except Exception as e:
    print(f"   ✗ PDF export failed: {e}")

# Test Excel Export
print("\n4. Testing Excel export...")
try:
    excel_buffer = export_manager.export_to_excel(
        sample_data,
        "Test Policy"
    )
    print(f"   ✓ Excel generated successfully ({len(excel_buffer.getvalue())} bytes)")
    
    # Save test file
    with open('test_export_data.xlsx', 'wb') as f:
        f.write(excel_buffer.getvalue())
    print("   ✓ Test Excel saved as 'test_export_data.xlsx'")
except Exception as e:
    print(f"   ✗ Excel export failed: {e}")

# Test CSV Export
print("\n5. Testing CSV export...")
try:
    csv_buffer = export_manager.export_to_csv(sample_data)
    print(f"   ✓ CSV generated successfully ({len(csv_buffer.getvalue())} bytes)")
    
    # Save test file
    with open('test_export_data.csv', 'wb') as f:
        f.write(csv_buffer.getvalue())
    print("   ✓ Test CSV saved as 'test_export_data.csv'")
except Exception as e:
    print(f"   ✗ CSV export failed: {e}")

# Test PowerPoint Export
if pptx_available:
    print("\n6. Testing PowerPoint export...")
    try:
        ppt_buffer = export_manager.export_to_powerpoint(
            sample_data,
            "Test Policy",
            None
        )
        print(f"   ✓ PowerPoint generated successfully ({len(ppt_buffer.getvalue())} bytes)")
        
        # Save test file
        with open('test_export_presentation.pptx', 'wb') as f:
            f.write(ppt_buffer.getvalue())
        print("   ✓ Test PowerPoint saved as 'test_export_presentation.pptx'")
    except Exception as e:
        print(f"   ✗ PowerPoint export failed: {e}")
else:
    print("\n6. Skipping PowerPoint test (python-pptx not installed)")

# Summary
print("\n" + "=" * 60)
print("EXPORT FUNCTIONALITY TEST COMPLETE")
print("=" * 60)
print("\nGenerated test files:")
print("  - test_export_report.pdf")
print("  - test_export_data.xlsx")
print("  - test_export_data.csv")
if pptx_available:
    print("  - test_export_presentation.pptx")
print("\nYou can open these files to verify the export quality.")
print("\nTo use in web interface:")
print("  1. Start the server: python start_web_interface.py")
print("  2. Generate predictions")
print("  3. Click export buttons at the bottom of results")
