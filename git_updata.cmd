@echo off
cd /d %~dp0
git add .
git commit -m "updata_20250623"
git push origin main
pause
