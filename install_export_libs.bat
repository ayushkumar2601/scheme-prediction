@echo off
echo Installing Export Libraries...
echo ================================

echo.
echo Installing reportlab (PDF generation)...
python -m pip install reportlab

echo.
echo Installing openpyxl (Excel generation)...
python -m pip install openpyxl

echo.
echo Installing python-pptx (PowerPoint generation)...
python -m pip install python-pptx

echo.
echo ================================
echo Installation Complete!
echo.
echo You can now use the export functionality.
echo Run: python test_export.py to verify.
pause
