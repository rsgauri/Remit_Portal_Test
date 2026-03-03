@echo off
echo Creating Flask folder structure...
echo.

:: Create templates folder
if not exist templates mkdir templates
echo [CREATED] templates folder

:: Create static folder
if not exist static mkdir static
echo [CREATED] static folder

:: Create uploads folder
if not exist uploads mkdir uploads
echo [CREATED] uploads folder

echo.
echo Folder structure created successfully!
echo.
echo Next steps:
echo 1. Copy all HTML files to templates\ folder
echo 2. Copy styles.css and script.js to static\ folder
echo 3. Make sure app.py, models.py, pdf_extractor.py are in this root folder
echo 4. Run: python app.py
echo.
pause