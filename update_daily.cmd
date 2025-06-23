@echo off
cd /d C:\Users\peter\myproject\ytstreamsite\
python manage.py daily_update >> logs\daily_update.log 2>&1
pause
