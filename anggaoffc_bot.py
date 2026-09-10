#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot Tracker K/B (Kecil/Besar)
Fitur: Slot List, Rekap, Alias, Geseran, Pinned, dan lainnya
Kompatibel dengan Termux
Userbot By Angga
"""

import json
import os
import re
from datetime import datetime
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError

# ============ KONFIGURASI ============
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Ganti dengan token bot Anda
DATA_DIR = os.path.expanduser("~/anggaoffc_data")

# ============ SETUP DATA DIRECTORY ============
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# ============ UTILITY FUNCTIONS ============
def get_group_file(group_id):
    """Dapatkan path file data grup"""
    return os.path.join(DATA_DIR, f"group_{group_id}.json")

def load_group_data(group_id):
    """Load data grup dari file"""
    file_path = get_group_file(group_id)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "active": False,
        "slots": {},  # {nama: {"K": total, "B": total}}
        "aliases": {},  # {user_id: nama}
        "pinned": {},  # {nama: saldo}
        "geseran": {},  # {key: {"nominal": N, "max": MAX}}
        "perak": True,  # B1 = 1000 jika True
        "alert": True,
        "owners": [],
        "closed_K": False,
        "closed_B": False,
        "dot_marks": [],  # Tandai pesan dengan titik
        "own_bypass": {}  # {user_id: True} - bypass P marker
    }

def save_group_data(group_id, data):
    """Simpan data grup ke file"""
    file_path = get_group_file(group_id)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def parse_bet(text):
    """Parse bet format: K5, 5K, B10, 10B, K5rb, B1.5, dll"""
    text = text.strip().upper()
    
    # Ganti koma dengan titik untuk desimal
    text = text.replace(',', '.')
    
    if 'K' in text:
        bet_type = 'K'
        nominal_str = text.replace('K', '').strip()
    elif 'B' in text:
        bet_type = 'B'
        nominal_str = text.replace('B', '').strip()
    else:
        return None, None, None
    
    try:
        if 'RB' in nominal_str:
            nominal = float(nominal_str.replace('RB', '').strip()) * 1000
        else:
            nominal = float(nominal_str)
        
        if nominal > 0:
            return bet_type, nominal, text
    except ValueError:
        pass
    
    return None, None, None

def format_nominal(nominal, perak_mode):
    """Format nominal dengan mode perak"""
    if perak_mode:
        if nominal % 1000 == 0:
            return f"{int(nominal // 1000)}rb"
        return str(nominal)
    return str(int(nominal) if nominal % 1 == 0 else nominal)

def get_pinned_message(group_id):
    """Get pinned message (implementation placeholder)"""
    return None

# ============ COMMAND HANDLERS ============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /start"""
    await update.message.reply_text(
        "🎉 Selamat datang di Angga Offc Bot!\n\n"
        "Bot tracker K/B dengan fitur lengkap.\n"
        "Ketik .cmd untuk melihat semua command\n"
        "Ketik .on untuk mengaktifkan bot di grup"
    )

async def cmd_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Aktifkan bot di grup"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("❌ Command ini hanya bisa dipakai di grup!")
        return
    
    group_id = update.message.chat_id
    data = load_group_data(group_id)
    data["active"] = True
    save_group_data(group_id, data)
    
    await update.message.reply_text("✅ Bot DIAKTIFKAN di grup ini!\n.off untuk matikan")

async def cmd_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Matikan bot di grup"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("❌ Command ini hanya bisa dipakai di grup!")
        return
    
    group_id = update.message.chat_id
    data = load_group_data(group_id)
    data["active"] = False
    save_group_data(group_id, data)
    
    await update.message.reply_text("❌ Bot DIMATIKAN di grup ini!\n.on untuk nyalakan")

async def cmd_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tampilkan slot list"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("❌ Command ini hanya bisa dipakai di grup!")
        return
    
    group_id = update.message.chat_id
    data = load_group_data(group_id)
    
    if not data["slots"]:
        await update.message.reply_text("📋 Slot masih kosong!")
        return
    
    perak_mode = data["perak"]
    message = "📋 **SLOT LIST**\n\n"
    total_k = 0
    total_b = 0
    
    for nama, bets in sorted(data["slots"].items()):
        k_total = bets.get("K", 0)
        b_total = bets.get("B", 0)
        total_k += k_total
        total_b += b_total
        
        k_str = format_nominal(k_total, perak_mode) if k_total > 0 else "-"
        b_str = format_nominal(b_total, perak_mode) if b_total > 0 else "-"
        
        marker = "P" if (nama in data["pinned"] or any(uid in data["own_bypass"] for uid in data["aliases"].keys() if data["aliases"][uid] == nama)) else ""
        message += f"👤 {nama} {marker}\n   K: {k_str} | B: {b_str}\n"
    
    message += f"\n📊 Total K: {format_nominal(total_k, perak_mode)} | Total B: {format_nominal(total_b, perak_mode)}"
    await update.message.reply_text(message, parse_mode="Markdown")

async def cmd_rs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reset list (kosongkan semua slot)"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("❌ Command ini hanya bisa dipakai di grup!")
        return
    
    group_id = update.message.chat_id
    data = load_group_data(group_id)
    data["slots"] = {}
    data["closed_K"] = False
    data["closed_B"] = False
    data["dot_marks"] = []
    save_group_data(group_id, data)
    
    await update.message.reply_text("🔄 Slot direset! Siap untuk ronde baru.")

async def cmd_rk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Rekap total K/B"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("❌ Command ini hanya bisa dipakai di grup!")
        return
    
    group_id = update.message.chat_id
    data = load_group_data(group_id)
    perak_mode = data["perak"]
    
    total_k = sum(bets.get("K", 0) for bets in data["slots"].values())
    total_b = sum(bets.get("B", 0) for bets in data["slots"].values())
    selisih = total_k - total_b
    
    k_str = format_nominal(total_k, perak_mode)
    b_str = format_nominal(total_b, perak_mode)
    sel_str = format_nominal(abs(selisih), perak_mode)
    
    message = f"📊 **REKAP RONDE**\n\n"
    message += f"Total K: {k_str}\n"
    message += f"Total B: {b_str}\n"
    message += f"Selisih: {sel_str} "
    message += f"({'K Unggul 🏆' if selisih > 0 else 'B Unggul 🏆' if selisih < 0 else 'Seri 🤝'})\n"
    
    await update.message.reply_text(message, parse_mode="Markdown")

async def cmd_perak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set mode perak (B1 = 1000)"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("❌ Command ini hanya bisa dipakai di grup!")
        return
    
    group_id = update.message.chat_id
    data = load_group_data(group_id)
    data["perak"] = True
    save_group_data(group_id, data)
    
    await update.message.reply_text("💰 Mode PERAK diaktifkan! (B1 = 1000)")

async def cmd_nonperak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set mode non-perak (B1 = 1)"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("❌ Command ini hanya bisa dipakai di grup!")
        return
    
    group_id = update.message.chat_id
    data = load_group_data(group_id)
    data["perak"] = False
    save_group_data(group_id, data)
    
    await update.message.reply_text("💵 Mode NON-PERAK diaktifkan! (B1 = 1)")

async def cmd_ck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tutup bet K"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("❌ Command ini hanya bisa dipakai di grup!")
        return
    
    group_id = update.message.chat_id
    data = load_group_data(group_id)
    data["closed_K"] = True
    save_group_data(group_id, data)
    
    await update.message.reply_text("🚫 Bet K DITUTUP! (.ok untuk buka semua)")

async def cmd_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tutup bet B"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("❌ Command ini hanya bisa dipakai di grup!")
        return
    
    group_id = update.message.chat_id
    data = load_group_data(group_id)
    data["closed_B"] = True
    save_group_data(group_id, data)
    
    await update.message.reply_text("🚫 Bet B DITUTUP! (.ok untuk buka semua)")

async def cmd_ok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buka semua side"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("❌ Command ini hanya bisa dipakai di grup!")
        return
    
    group_id = update.message.chat_id
    data = load_group_data(group_id)
    data["closed_K"] = False
    data["closed_B"] = False
    save_group_data(group_id, data)
    
    await update.message.reply_text("✅ Semua side DIBUKA!")

async def cmd_sv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set alias nama"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("❌ Command ini hanya bisa dipakai di grup!")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply pesan user yang ingin di-set alias!")
        return
    
    group_id = update.message.chat_id
    user_id = update.message.reply_to_message.from_user.id
    args = update.message.text.split()
    
    if len(args) < 2:
        await update.message.reply_text("❌ Format: .sv NAMA")
        return
    
    nama = args[1]
    data = load_group_data(group_id)
    data["aliases"][str(user_id)] = nama
    save_group_data(group_id, data)
    
    await update.message.reply_text(f"✅ Alias set untuk {nama}")

async def cmd_svlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lihat semua alias"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("❌ Command ini hanya bisa dipakai di grup!")
        return
    
    group_id = update.message.chat_id
    data = load_group_data(group_id)
    
    if not data["aliases"]:
        await update.message.reply_text("📋 Belum ada alias")
        return
    
    message = "📋 **DAFTAR ALIAS**\n\n"
    for user_id, nama in data["aliases"].items():
        message += f"👤 {nama} (ID: {user_id})\n"
    
    await update.message.reply_text(message, parse_mode="Markdown")

async def cmd_addp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tandai saldo cukup dengan P"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("❌ Command ini hanya bisa dipakai di grup!")
        return
    
    args = update.message.text.split()
    if len(args) < 2:
        await update.message.reply_text("❌ Format: .addp NAMA")
        return
    
    group_id = update.message.chat_id
    nama = args[1]
    data = load_group_data(group_id)
    data["pinned"][nama] = True
    save_group_data(group_id, data)
    
    await update.message.reply_text(f"✅ {nama} ditandai dengan P (saldo cukup)")

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tampilkan bantuan"""
    help_text = """
🎉 **ANGGA OFFC - TUTORIAL BOTLIST**

**🎯 COMMAND UTAMA:**
`.on` - Nyalakan bot
`.off` - Matikan bot
`.list` - Lihat slot
`.rk` - Rekap total K/B
`.rs` - Reset list

**💰 PASANG BET:**
`K5` atau `5K` - Pasang Kecil 5
`B10` atau `10B` - Pasang Besar 10
`K5rb` - Paksa ribuan (5×1000)
`B1.5` - Desimal (titik/koma sama)

**⚙️ PENGATURAN:**
`.perak` - B1 = 1000
`.nonperak` - B1 = 1
`.ck` - Tutup bet K
`.cb` - Tutup bet B
`.ok` - Buka semua side

**👤 ALIAS & PINNED:**
`.sv NAMA` - Set alias (reply user)
`.svlist` - Lihat semua alias
`.addp NAMA` - Tandai saldo cukup

**🎯 SLOT MANAGEMENT:**
`.h NAMA` - Hapus slot pemain
`.tambah NAMA N` - Tambah nominal
`.kurang NAMA N` - Kurangi nominal

Ketik `.cmd` untuk command lengkap!
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pesan dari user"""
    if update.message.chat.type == 'private':
        return
    
    group_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.first_name or f"User{user_id}"
    text = update.message.text.strip()
    
    data = load_group_data(group_id)
    
    # Cek apakah bot aktif
    if not data["active"]:
        return
    
    # Cek apakah ada custom alias
    if str(user_id) in data["aliases"]:
        username = data["aliases"][str(user_id)]
    
    # Parse bet
    bet_type, nominal, original = parse_bet(text)
    
    if bet_type and nominal:
        # Cek apakah side ditutup
        if (bet_type == 'K' and data["closed_K"]) or (bet_type == 'B' and data["closed_B"]):
            await update.message.reply_text(f"❌ Bet {bet_type} sudah ditutup!")
            return
        
        # Tambah ke slot
        if username not in data["slots"]:
            data["slots"][username] = {"K": 0, "B": 0}
        
        data["slots"][username][bet_type] += nominal
        
        # Konversi nominal untuk display
        if data["perak"] and nominal % 1000 == 0:
            display_nominal = f"{int(nominal // 1000)}rb"
        else:
            display_nominal = str(int(nominal) if nominal % 1 == 0 else nominal)
        
        save_group_data(group_id, data)
        
        # Konfirmasi
        if data["alert"]:
            await update.message.reply_text(
                f"✅ {username} pasang {bet_type}{display_nominal}",
                reply_to_message_id=update.message.message_id
            )

async def main():
    """Main function"""
    # Buat aplikasi
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("cmd", cmd_help))
    
    # Dot commands (regex)
    app.add_handler(MessageHandler(filters.Regex(r"^\.on$"), cmd_on))
    app.add_handler(MessageHandler(filters.Regex(r"^\.off$"), cmd_off))
    app.add_handler(MessageHandler(filters.Regex(r"^\.list$"), cmd_list))
    app.add_handler(MessageHandler(filters.Regex(r"^\.rs$"), cmd_rs))
    app.add_handler(MessageHandler(filters.Regex(r"^\.rk$"), cmd_rk))
    app.add_handler(MessageHandler(filters.Regex(r"^\.perak$"), cmd_perak))
    app.add_handler(MessageHandler(filters.Regex(r"^\.nonperak$"), cmd_nonperak))
    app.add_handler(MessageHandler(filters.Regex(r"^\.ck$"), cmd_ck))
    app.add_handler(MessageHandler(filters.Regex(r"^\.cb$"), cmd_cb))
    app.add_handler(MessageHandler(filters.Regex(r"^\.ok$"), cmd_ok))
    app.add_handler(MessageHandler(filters.Regex(r"^\.sv"), cmd_sv))
    app.add_handler(MessageHandler(filters.Regex(r"^\.svlist$"), cmd_svlist))
    app.add_handler(MessageHandler(filters.Regex(r"^\.addp"), cmd_addp))
    
    # Message handler untuk bet
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
        handle_message
    ))
    
    # Jalankan bot
    print("🤖 Angga Offc Bot sedang berjalan...")
    print("Tekan Ctrl+C untuk berhenti")
    
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Ganti BOT_TOKEN dengan token bot Anda!")
        print("Cara mendapat token:")
        print("1. Chat @BotFather di Telegram")
        print("2. Ketik /newbot")
        print("3. Ikuti instruksi")
        exit(1)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Bot dihentikan")