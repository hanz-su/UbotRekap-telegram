#!/bin/bash
# Jalankan bot di background dengan nohup

cd ~/anggaoffc_bot

# Buat log file
mkdir -p logs

# Jalankan dengan nohup
nohup python anggaoffc_bot.py > logs/bot.log 2>&1 &

echo "✅ Bot berjalan di background!"
echo "PID: $!"
echo "Log: ~/anggaoffc_bot/logs/bot.log"
echo ""
echo "Untuk stop bot:"
echo "  pkill -f anggaoffc_bot.py"
echo ""
echo "Untuk lihat log:"
echo "  tail -f ~/anggaoffc_bot/logs/bot.log"