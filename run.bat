@echo off
setlocal
cls
echo ==========================================
echo    FOREX ANALYSIS TERMINAL - LAUNCHER
echo ==========================================
echo.
echo  [1] Launch Rust Backend (Axum)
echo      - High performance, serves premium UI
echo      - Default at http://127.0.0.1:8080
echo.
echo  [2] Launch Python Dashboard (Streamlit)
echo      - Responsive dashboard version
echo      - Requires streamlit (pip install -r requirements.txt)
echo.
echo  [3] Exit
echo.
set /p choice="Select an option (1-3): "

if "%choice%"=="1" goto rust
if "%choice%"=="2" goto python
if "%choice%"=="3" goto end
goto exit

:rust
echo.
echo Starting Rust Backend...
cargo run --release
pause
goto end

:python
echo.
echo Starting Streamlit Dashboard...
streamlit run app.py
pause
goto end

:end
exit

