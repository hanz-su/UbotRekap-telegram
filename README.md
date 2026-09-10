# 🎉 Angga Offc Bot - Telegram Userbot Tracker K/B

**Angga Offc Bot** adalah Telegram userbot yang dirancang khusus untuk tracking taruhan K (Kecil) dan B (Besar) di grup dengan fitur lengkap dan professional.

## 📚 Fitur Lengkap

### 🎯 Modul: Slot & List
- `K5` / `5K` - Pasang Kecil 5
- `B10` / `10B` - Pasang Besar 10
- `B1.5` / `B1,5` - Desimal (titik/koma sama)
- `K5rb` - Paksa ribuan (5×1000)
- `Ball` / `allB` - Pasang semua saldo dari pinned
- `.list` - Lihat slot ronde ini
- `.rk` - Rekap total K/B + selisih
- `.rs` - Kosongkan semua slot
- `.ck` - Tutup bet K
- `.cb` - Tutup bet B
- `.ok` - Buka semua side
- `.h NAMA` - Hapus slot pemain
- `.tambah NAMA N` - Tambah nominal
- `.kurang NAMA N` - Kurangi nominal
- `.c` - Hapus tanda . (reply bet)
- `.cr` - Hapus SEMUA tanda . di grup

### 📌 Modul: Pinned & Alias
- `.addp` - Tandai saldo cukup dengan P
- `.p` - Reply bet → paksa P
- `.tf` - Ingatkan pemain belum TF
- `.sv NAMA` - Reply user + set nama
- `.depo NAMA` - Reply user + set alias + save contact (silent)
- `.svlist` - Lihat semua alias
- `.svdel` - Hapus alias (reply / ID)
- `.svsync` - Sync semua alias ke contact
- `.svown` - Reply user → bypass P-marker
- `.svdelown` - Cabut bypass P-marker (reply / ID)

### 🎯 Modul: Geseran
- `.geseran KEY N MAX` - Set key preset bet nominal N, max MAX user
- `.geseran` - List key geseran
- `.geseran del KEY` - Hapus key geseran
- `KEY b` / `#KEY k` - Trigger geseran (player)

### ⚙️ Modul: Pengaturan
- `.on` - Nyalakan bot di grup
- `.off` - Matikan bot di grup
- `.perak` - B1 = 1000
- `.nonperak` - B1 = 1
- `.alert on` - Aktifkan konfirmasi bet ✅
- `.alert off` - Matikan konfirmasi bet
- `.akses` - Lihat/beri akses grup
- `.delakses` - Cabut akses grup

## 🚀 Cara Instalasi (Termux)

### 1️⃣ Update & Install Packages
```bash
pkg update && pkg upgrade -y
pkg install -y python pip git
```

### 2️⃣ Clone Repository
```bash
cd ~
git clone https://github.com/hanz-su/UbotRekap-telegram.git
cd UbotRekap-telegram
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

Atau manual:
```bash
pip install python-telegram-bot
```

### 4️⃣ Setup Bot Token

**Dapatkan token bot:**
1. Buka Telegram
2. Chat dengan **@BotFather**
3. Ketik `/newbot`
4. Ikuti instruksi
5. Copy token yang diberikan

**Masukkan token ke script:**
```bash
nano anggaoffc_bot.py
```

Cari baris:
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

Ganti dengan token Anda, lalu save (Ctrl+X → Y → Enter)

### 5️⃣ Jalankan Bot

**Opsi 1: Testing (langsung)**
```bash
python anggaoffc_bot.py
```

**Opsi 2: Background (recommended)**
```bash
chmod +x run_background.sh
./run_background.sh
```

## 📋 Cara Pakai Bot di Grup

### Setup Awal
```
1. Invite bot ke grup Telegram
2. Ketik .on untuk aktifkan bot
3. Bot siap menerima bet
```

### Contoh Penggunaan Lengkap

**Skenario: Bermain Dadu K/B**

```
👤 Admin: .on
🤖 Bot: ✅ Bot DIAKTIFKAN di grup ini!

👤 User1: K5
🤖 Bot: ✅ User1 pasang K5

👤 User2: B10
🤖 Bot: ✅ User2 pasang B10

👤 User3: B1.5
🤖 Bot: ✅ User3 pasang B1.5

👤 Admin: .list
🤖 Bot:
📋 SLOT LIST
👤 User1
   K: 5rb | B: -
👤 User2
   K: - | B: 10rb
👤 User3
   K: - | B: 1.5rb

📊 Total K: 5rb | Total B: 11.5rb

👤 Admin: .rk
🤖 Bot:
📊 REKAP RONDE
Total K: 5rb
Total B: 11.5rb
Selisih: 6.5rb (B Unggul 🏆)

👤 Admin: .rs
🤖 Bot: 🔄 Slot direset! Siap untuk ronde baru.
```

### Contoh Alias

```
👤 Admin: (reply pesan User1) .sv Ahmad
🤖 Bot: ✅ Alias set untuk Ahmad

👤 Ahmad: K5
🤖 Bot: ✅ Ahmad pasang K5

👤 Admin: .svlist
🤖 Bot:
📋 DAFTAR ALIAS
👤 Ahmad (ID: 123456789)
```

### Contoh Pinned

```
👤 Admin: .addp Ahmad
🤖 Bot: ✅ Ahmad ditandai dengan P (saldo cukup)

👤 Admin: .list
🤖 Bot:
📋 SLOT LIST
👤 Ahmad P
   K: 5rb | B: -
```

### Tutup Side

```
👤 Admin: .ck
🤖 Bot: 🚫 Bet K DITUTUP! (.ok untuk buka semua)

👤 User: K5
🤖 Bot: ❌ Bet K sudah ditutup!

👤 User: B10
🤖 Bot: ✅ User pasang B10

👤 Admin: .ok
🤖 Bot: ✅ Semua side DIBUKA!
```

## 📊 Data Storage

Data grup disimpan di: `~/anggaoffc_data/group_{GROUP_ID}.json`

Format data:
```json
{
  "active": true,
  "slots": {
    "User1": {"K": 5000, "B": 0},
    "User2": {"K": 0, "B": 10000}
  },
  "aliases": {"123456789": "Ahmad"},
  "pinned": {"Ahmad": true},
  "geseran": {
    "gede": {"nominal": 10000, "max": 5}
  },
  "perak": true,
  "alert": true,
  "closed_K": false,
  "closed_B": false,
  "own_bypass": {}
}
```

## 🛑 Stop Bot

**Jika menjalankan langsung (Ctrl+C):**
```bash
Ctrl + C
```

**Jika menjalankan di background:**
```bash
pkill -f anggaoffc_bot.py
```

## 📝 Lihat Log Bot

```bash
tail -f ~/anggaoffc_bot/logs/bot.log
```

## 🐛 Troubleshooting

### Bot tidak merespons
- Pastikan bot sudah di-invite ke grup
- Pastikan `.on` sudah diketik
- Cek token bot di `anggaoffc_bot.py`

### Error "No module named 'telegram'"
```bash
pip install python-telegram-bot
```

### Permission denied saat run script
```bash
chmod +x anggaoffc_bot.py
chmod +x setup.sh
chmod +x run_background.sh
```

### Bot crash/berhenti
Cek log:
```bash
tail -f ~/anggaoffc_bot/logs/bot.log
```

## 📝 Catatan Penting

- ✅ Bot harus aktif dengan `.on` di setiap grup
- ✅ Data setiap grup disimpan terpisah
- ✅ Mode perak = B1 setara dengan 1000 (nominal)
- ✅ Mode non-perak = B1 setara dengan 1 (nominal)
- ✅ Desimal bisa pakai titik (.) atau koma (,)
- ✅ Alias memudahkan tracking pemain
- ✅ Pinned marker (P) menandakan saldo cukup
- ✅ Close side (K/B) untuk kontrol taruhan

## 🌟 Fitur Unggulan

✨ **Tracking Real-time** - Pencatatan otomatis setiap taruhan
✨ **Alias Support** - Satu user bisa punya nama alias
✨ **Pinned Marker** - Tandai pemain dengan saldo cukup
✨ **Close Side** - Kontrol pembukaan sisi K atau B
✨ **Rekap Otomatis** - Kalkulasi total dan selisih
✨ **Multi-Grup** - Support multiple group sekaligus
✨ **Desimal Support** - Dukung nominal dengan desimal
✨ **Mode Perak** - Fleksibel dalam penulisan nominal

## 📞 Support & Kontribusi

Jika ada bug atau fitur yang ingin ditambahkan:
- Buat issue di GitHub
- Submit pull request
- Chat langsung di Telegram

## 📄 Lisensi

MIT License - Bebas digunakan dan dimodifikasi

## 👨‍💻 Dibuat oleh

**Userbot By Angga** - Modified for Telegram Bot Framework
**Maintained by Hanz-su** - [GitHub Profile](https://github.com/hanz-su)

---

**⭐ Jika membantu, jangan lupa kasih star di GitHub!**

🤖 **Angga Offc Bot** - Solusi tracking taruhan terbaik untuk grup Telegram Anda!