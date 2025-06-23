@echo off
cd /d %~dp0
git add .
git commit -m "🧩 更新 Django 專案與資料庫模型"
git push origin main
pause
