#!/bin/bash
# Setup Angga Offc Bot untuk Termux

echo "🔧 Setup Angga Offc Bot untuk Termux..."

# Update packages
pkg update -y
pkg upgrade -y

# Install Python dan dependencies
pkg install -y python pip

# Install required Python packages
pip install python-telegram-bot

# Buat direktori
mkdir -p ~/anggaoffc_data
mkdir -p ~/anggaoffc_bot

echo "✅ Setup selesai!"
echo ""
echo "📝 LANGKAH SELANJUTNYA:"
echo "1. Edit anggaoffc_bot.py"
echo "2. Ganti 'YOUR_BOT_TOKEN_HERE' dengan token bot Anda"
echo "3. Jalankan: python anggaoffc_bot.py"
echo ""
echo "💡 Cara mendapat token bot:"
echo "   - Chat @BotFather di Telegram"
echo "   - Ketik /newbot"
echo "   - Ikuti instruksi"