@echo off
chcp 65001 > nul

REM 切換到專案資料夾
cd /d C:\Users\peter\myproject\ytstreamsite

REM 執行 Django 指令
python manage.py daily_update >> logs\daily_update.log 2>&1

pause
