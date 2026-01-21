# Export Functionality Guide

## Overview

The Aadhaar Policy Impact Prediction System now includes comprehensive export functionality, allowing you to download prediction results in multiple formats:

- **PDF Report** - Professional formatted report with summary, tables, and visualizations
- **Excel Workbook** - Multi-sheet workbook with summary, regional impact, daily impact, and risk assessment
- **CSV File** - Regional impact data in CSV format for easy data analysis
- **PowerPoint Presentation** - Ready-to-present slides with key findings and visualizations

## Installation

### Install Required Libraries

```bash
pip install reportlab openpyxl python-pptx
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Features

### 1. PDF Report Export
**File**: Professional PDF document with:
- Executive summary with key metrics
- Regional impact analysis table (top 15 states)
- Visual analysis charts
- Risk assessment breakdown
- Professional formatting with headers, colors, and branding

**Use Case**: Share with stakeholders, include in presentations, archive predictions

### 2. Excel Export
**File**: Multi-sheet Excel workbook with:
- **Summary Sheet**: Policy details and key metrics
- **Regional Impact Sheet**: Complete state-wise breakdown
- **Daily Impact Sheet**: Day-by-day predictions
- **Risk Assessment Sheet**: States categorized by risk level

**Use Case**: Further data analysis, pivot tables, custom charts

### 3. CSV Export
**File**: Simple CSV file with regional impact data

**Use Case**: Import into other tools, database loading, quick data sharing

### 4. PowerPoint Export
**File**: Professional presentation with:
- Title slide with policy name and date
- Executive summary slide
- Top 10 affected states table
- Visual analysis slide with charts
- Risk assessment slide

**Use Case**: Board presentations, stakeholder meetings, policy briefings

## How to Use

### From Web Interface

1. **Generate Predictions**
   - Fill in policy parameters
   - Click "Generate Prediction"
   - Wait for results to load

2. **Export Results**
   - Scroll to the "Export Results" section at the bottom
   - Click on any export button:
     - 📄 Download PDF Report
     - 📊 Download Excel
     - 📋 Download CSV
     - 📽️ Download PowerPoint
   - File will download automatically

### From Python Code

```python
from export_utils import export_manager

# After getting prediction results
result_data = predictor.predict_policy_impact(
    policy_date="2025-04-01",
    forecast_days=60
)

# Export to PDF
pdf_buffer = export_manager.export_to_pdf(
    result_data, 
    policy_name="My Policy",
    viz_image_base64=viz_image
)

with open('report.pdf', 'wb') as f:
    f.write(pdf_buffer.read())

# Export to Excel
excel_buffer = export_manager.export_to_excel(
    result_data,
    policy_name="My Policy"
)

with open('data.xlsx', 'wb') as f:
    f.write(excel_buffer.read())

# Export to CSV
csv_buffer = export_manager.export_to_csv(result_data)

with open('data.csv', 'wb') as f:
    f.write(csv_buffer.read())

# Export to PowerPoint
ppt_buffer = export_manager.export_to_powerpoint(
    result_data,
    policy_name="My Policy",
    viz_image_base64=viz_image
)

with open('presentation.pptx', 'wb') as f:
    f.write(ppt_buffer.read())
```

## File Naming Convention

All exported files are automatically named with timestamps:
- `policy_impact_report_YYYYMMDD_HHMMSS.pdf`
- `policy_impact_data_YYYYMMDD_HHMMSS.xlsx`
- `policy_impact_data_YYYYMMDD_HHMMSS.csv`
- `policy_impact_presentation_YYYYMMDD_HHMMSS.pptx`

## Technical Details

### PDF Generation
- **Library**: ReportLab
- **Features**: Custom styling, tables, images, multi-page support
- **Page Size**: Letter (8.5" x 11")
- **Colors**: Professional blue theme matching UI

### Excel Generation
- **Library**: openpyxl
- **Features**: Multiple sheets, auto-column width, formatted headers
- **Format**: .xlsx (Excel 2007+)

### CSV Generation
- **Library**: Pandas
- **Features**: UTF-8 encoding, comma-separated
- **Format**: Standard CSV

### PowerPoint Generation
- **Library**: python-pptx
- **Features**: Custom layouts, tables, images, formatted text
- **Format**: .pptx (PowerPoint 2007+)
- **Slide Size**: 10" x 7.5" (standard)

## Troubleshooting

### "Module not found" Error
```bash
pip install reportlab openpyxl python-pptx
```

### PDF Generation Fails
- Check if ReportLab is installed correctly
- Ensure sufficient disk space
- Check console for detailed error messages

### Excel/PowerPoint Generation Fails
- Verify openpyxl and python-pptx are installed
- Check file permissions in download directory

### Export Button Not Working
- Ensure predictions have been generated first
- Check browser console for JavaScript errors
- Verify Flask server is running

## API Endpoints

### POST /api/export/pdf
**Request Body**:
```json
{
  "result_data": {...},
  "policy_name": "Policy Name",
  "viz_image": "data:image/png;base64,..."
}
```

### POST /api/export/excel
**Request Body**:
```json
{
  "result_data": {...},
  "policy_name": "Policy Name"
}
```

### POST /api/export/csv
**Request Body**:
```json
{
  "result_data": {...}
}
```

### POST /api/export/powerpoint
**Request Body**:
```json
{
  "result_data": {...},
  "policy_name": "Policy Name",
  "viz_image": "data:image/png;base64,..."
}
```

## Customization

### Modify PDF Styling
Edit `export_utils.py` → `_setup_custom_styles()` method

### Change Excel Sheet Names
Edit `export_utils.py` → `export_to_excel()` method

### Customize PowerPoint Layout
Edit `export_utils.py` → `export_to_powerpoint()` method

## Best Practices

1. **Generate predictions first** before attempting to export
2. **Use PDF** for formal reports and documentation
3. **Use Excel** for detailed data analysis
4. **Use CSV** for data integration with other systems
5. **Use PowerPoint** for presentations and meetings
6. **Keep file names** with timestamps for version tracking

## Future Enhancements

Potential additions:
- Email export functionality
- Scheduled automated reports
- Custom report templates
- Batch export for multiple scenarios
- Cloud storage integration (S3, Google Drive)

## Support

For issues or questions:
1. Check console logs for detailed error messages
2. Verify all dependencies are installed
3. Ensure Flask server is running
4. Check file permissions in download directory
