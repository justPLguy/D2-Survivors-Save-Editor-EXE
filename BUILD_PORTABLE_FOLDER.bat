
@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo D2 Survivors Save Editor - Portable Build
echo ==========================================
echo.

python -m pip install --upgrade pyinstaller
if errorlevel 1 goto failed

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist D2SurvivorsSaveEditor.spec del /q D2SurvivorsSaveEditor.spec

python -m PyInstaller --noconfirm --clean --onedir --windowed --noupx --name D2SurvivorsSaveEditor D2_Survivors_Save_Editor.py
if errorlevel 1 goto failed

if exist README.md copy /y README.md dist\D2SurvivorsSaveEditor\README.md >nul
if exist RELEASE_NOTES_v6.5.md copy /y RELEASE_NOTES_v6.5.md dist\D2SurvivorsSaveEditor\RELEASE_NOTES_v6.5.md >nul

echo.
echo ==========================================
echo Build completed successfully!
echo Output: dist\D2SurvivorsSaveEditor\
echo ==========================================
echo.
pause
exit /b 0

:failed
echo.
echo ==========================================
echo BUILD FAILED!
echo Read the error messages above.
echo ==========================================
echo.
pause
exit /b 1
