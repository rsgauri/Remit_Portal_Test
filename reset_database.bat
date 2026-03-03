@echo off
echo ========================================
echo DATABASE RESET SCRIPT
echo ========================================
echo.
echo This will delete your old database and create a new one
echo with the updated schema (clients, sources, remittance_advice)
echo.
pause

echo.
echo [1/3] Deleting old database...
if exist remittance.db (
    del remittance.db
    echo ✓ Old database deleted
) else (
    echo ℹ No old database found
)

echo.
echo [2/3] Creating new database with updated schema...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✓ New database created')"

echo.
echo [3/3] Seeding database with sample data...
python seed_database.py

echo.
echo ========================================
echo ✓ DATABASE RESET COMPLETE!
echo ========================================
echo.
echo You can now run: python app.py
echo.
pause