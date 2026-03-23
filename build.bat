@echo off
echo =========================================
echo KMATRIX PRIME - COMPILER INITIATED
echo Building the ultimate executable...
echo =========================================
python -m PyInstaller --noconfirm --onefile --windowed --icon="kmatrix_icon.ico" --add-data="kmatrix_icon.ico;." --add-data="kmatrix_logo.png;." main.py
echo =========================================
echo BUILD COMPLETE. Check the 'dist' folder!
pause