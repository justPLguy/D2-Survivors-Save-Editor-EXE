@echo off
setlocal
cd /d "%~dp0"
python -m pip install --upgrade pyinstaller
if errorlevel 1 goto failed
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist D2SurvivorsSaveEditor.spec del /q D2SurvivorsSaveEditor.spec
python -m PyInstaller --noconfirm --clean --onedir --windowed --noupx --name D2SurvivorsSaveEditor D2_Survivors_Save_Editor.py
if errorlevel 1 goto failed
echo.
echo Build complete: dist\D2SurvivorsSaveEditor\
pause
exit /b 0
:failed
echo Build failed. Read the error above.
pause
exit /b 1
