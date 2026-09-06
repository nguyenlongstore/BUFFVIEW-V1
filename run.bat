@echo off
title NGLONG DEV - TIKTOK VIEW BOT v5.0
color 0F
mode con: cols=90 lines=50
echo ==============================================
echo     NGLONG DEV - TIKTOK VIEW BOT v5.0
echo     MAX SPEED EDITION
echo ==============================================
echo.
echo [*] Kiem tra va cai dat thu vien...
pip install requests fake-useragent -q
echo.
echo [*] Khoi dong bot...
python bot.py
pause
