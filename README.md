# 📥 Excel Image Downloader

**[🇹🇷 Türkçe](#-türkçe)** • **[🇬🇧 English](#-english)**

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

<p align="center">
  <img src="docs/screenshot.png" alt="Excel Image Downloader" width="620">
</p>

---

## 🇹🇷 Türkçe

Excel dosyalarındaki URL linklerinden toplu resim indirme aracı. Modern koyu tema arayüz, paralel indirme, resume desteği ve canlı log ile.

> Excel'in içinde URL olarak duran binlerce resim linkini otomatik indirip, istersen her ürün için ayrı klasöre, istersen tek klasöre toplar.

### ✨ Özellikler

- 🌙 **Modern koyu tema** — rahat göz için
- ⚡ **Paralel indirme** — 1-32 thread slider ile ayarlanabilir
- ↷ **Resume (kaldığı yerden devam)** — var olan dosyaları atlar
- 📁 **İki mod:** her ürün ayrı klasöre **veya** hepsi tek klasöre
- ⏹ **Durdur butonu** — istediğin an temiz durur
- 📊 **Canlı hız + ETA** — "15.3/sn • kalan ~2sa 14dk"
- 📝 **Hata raporu** — başarısız URL'ler `hatalar.txt`'ye yazılır
- 🔢 **3'lü canlı sayaç** — OK • ATLANAN • HATA
- 🧵 **Büyük Excel desteği** — 100.000+ satır, `read_only` modla RAM yemez

### 🚀 Hızlı Başlangıç

#### Seçenek 1: Hazır EXE (Windows)

1. [Releases](../../releases) sayfasından en son `ResimIndirici.exe`'yi indir
2. Çift tıkla, çalıştır
3. Python kurmaya gerek yok ✅

> ⚠️ Windows SmartScreen uyarısı çıkarsa: *"Daha fazla bilgi → Yine de çalıştır"*. İmzalı değil çünkü (false positive).

#### Seçenek 2: Kaynak koddan çalıştır

```bash
git clone https://github.com/ayberkbgln/excel-image-downloader.git
cd excel-image-downloader
pip install -r requirements.txt
python app.py
```

#### Seçenek 3: Kendi EXE'ni build et

```bash
pip install -r requirements.txt
python make_icon.py
pyinstaller --noconfirm --onefile --windowed ^
    --name "ResimIndirici" ^
    --icon=icon.ico ^
    --add-data "icon.ico;." ^
    app.py
```

EXE → `dist/ResimIndirici.exe`

### 📋 Excel Formatı

| A sütunu | B, C, D, ... sütunları |
|---|---|
| Ürün kodu (klasör adı olacak) | Resim URL'leri |

**Örnek:**

| Malzeme Kodu | Foto 1 | Foto 2 | Foto 3 |
|---|---|---|---|
| 11680150005 | https://cdn.../11680150_1.jpg | https://cdn.../11680150_2.jpg | https://cdn.../11680150_3.jpg |
| 11657262006 | https://cdn.../11657262_1.jpg | https://cdn.../11657262_2.jpg | |

- İlk satır başlık olarak kabul edilir (atlanır)
- A sütunu = klasör adı
- 2. sütundan itibaren `http` ile başlayan her hücre indirilir
- Boş hücreler atlanır

### 🎛️ Kullanım

1. **Excel Dosyası:** `.xlsx` veya `.xlsm` seç
2. **Çıktı Klasörü:** resimlerin ineceği yer (otomatik `indirilen` oluşur)
3. **Paralel İndirme:** 10 thread genelde ideal (sunucuyu bunaltmaz)
4. **Opsiyonlar:**
   - ☑ **Var olan dosyaları atla** — yarıda kalınca tekrar çalıştır, kaldığı yerden devam eder
   - ☐ **Tek klasöre indir** — hepsini çıktı klasörüne atar, alt klasör açmaz
5. **▶ İNDİRMEYİ BAŞLAT**

### 🔧 Dosya Adlandırma

URL'deki `Product/` kelimesinden sonraki kısım dosya adı olur:

```
https://cdn.example.com/Uploads/Product/11680150_40400_2.jpg
                               ↓
                       11680150_40400_2.jpg
```

Eğer `Product/` yoksa URL'nin son kısmı alınır.

### 📊 Performans

| Resim Sayısı | Thread | Tahmini Süre |
|---|---|---|
| 100 | 10 | ~15 sn |
| 1.000 | 10 | ~2-3 dk |
| 10.000 | 10 | ~20-30 dk |
| 100.000 | 15 | ~3-5 saat |

*Sunucu hızına ve internet bağlantısına göre değişir.*

### 🐛 Sık Karşılaşılan Sorunlar

<details>
<summary><b>"Windows SmartScreen bunu engelledi"</b></summary>
EXE dijital imzalı değil. "Daha fazla bilgi" → "Yine de çalıştır" de. Kod açık, inceleyebilirsin.
</details>

<details>
<summary><b>Antivirüs yanlış alarm veriyor</b></summary>
PyInstaller ile build edilen EXE'lerde false positive normaldir. İstisna ekleyebilirsin veya kaynak koddan kendin build et.
</details>

<details>
<summary><b>Tek klasör modunda resim sayısı az geliyor</b></summary>
Aynı isimli dosyalar birbirinin üzerine yazıyor olabilir. "Tek klasör" kapalı, ürün koduyla klasörleme açık kalsın.
</details>

<details>
<summary><b>Çok fazla hata alıyorum</b></summary>
Thread sayısını düşür (10 → 5). Sunucu rate-limit uyguluyor olabilir.
</details>

---

## 🇬🇧 English

A bulk image downloader that extracts URLs from Excel files and downloads them. Modern dark UI, parallel downloads, resume support, and live logging.

> Automatically downloads thousands of image URLs stored in Excel cells — either into per-product subfolders or a single folder.

### ✨ Features

- 🌙 **Modern dark theme** — easy on the eyes
- ⚡ **Parallel downloads** — adjustable 1-32 threads via slider
- ↷ **Resume support** — skips already-downloaded files
- 📁 **Two modes:** per-product subfolders **or** single flat folder
- ⏹ **Stop button** — clean cancellation anytime
- 📊 **Live speed + ETA** — "15.3/sec • ETA ~2h 14m"
- 📝 **Error report** — failed URLs written to `hatalar.txt`
- 🔢 **Triple live counter** — OK • SKIPPED • FAILED
- 🧵 **Large Excel support** — 100,000+ rows, `read_only` mode (low RAM)

### 🚀 Quick Start

#### Option 1: Prebuilt EXE (Windows)

1. Download the latest `ResimIndirici.exe` from [Releases](../../releases)
2. Double-click to run
3. No Python installation required ✅

> ⚠️ If Windows SmartScreen warns you: *"More info → Run anyway"*. The EXE isn't code-signed (false positive).

#### Option 2: Run from source

```bash
git clone https://github.com/ayberkbgln/excel-image-downloader.git
cd excel-image-downloader
pip install -r requirements.txt
python app.py
```

#### Option 3: Build your own EXE

```bash
pip install -r requirements.txt
python make_icon.py
pyinstaller --noconfirm --onefile --windowed ^
    --name "ResimIndirici" ^
    --icon=icon.ico ^
    --add-data "icon.ico;." ^
    app.py
```

EXE → `dist/ResimIndirici.exe`

### 📋 Excel Format

| Column A | Columns B, C, D, ... |
|---|---|
| Product code (becomes folder name) | Image URLs |

**Example:**

| Product Code | Photo 1 | Photo 2 | Photo 3 |
|---|---|---|---|
| 11680150005 | https://cdn.../11680150_1.jpg | https://cdn.../11680150_2.jpg | https://cdn.../11680150_3.jpg |
| 11657262006 | https://cdn.../11657262_1.jpg | https://cdn.../11657262_2.jpg | |

- First row is treated as header (skipped)
- Column A = folder name
- Any cell starting with `http` from column B onward is downloaded
- Empty cells are ignored

### 🎛️ Usage

1. **Excel File:** select a `.xlsx` or `.xlsm`
2. **Output Folder:** destination (auto-creates `indirilen` if empty)
3. **Parallel Downloads:** 10 threads is a good default (won't overload servers)
4. **Options:**
   - ☑ **Skip existing files** — rerun after interruption, resumes where it left off
   - ☐ **Single folder mode** — all images into the output folder, no subfolders
5. **▶ START DOWNLOAD**

### 🔧 File Naming

The part after `Product/` in the URL becomes the filename:

```
https://cdn.example.com/Uploads/Product/11680150_40400_2.jpg
                               ↓
                       11680150_40400_2.jpg
```

If `Product/` isn't in the URL, the last path segment is used.

### 📊 Performance

| Image Count | Threads | Estimated Time |
|---|---|---|
| 100 | 10 | ~15 sec |
| 1,000 | 10 | ~2-3 min |
| 10,000 | 10 | ~20-30 min |
| 100,000 | 15 | ~3-5 hours |

*Depends on server speed and your internet connection.*

### 🐛 Troubleshooting

<details>
<summary><b>"Windows SmartScreen blocked this"</b></summary>
The EXE isn't digitally signed. Click "More info" → "Run anyway". The source is open — feel free to review it.
</details>

<details>
<summary><b>Antivirus false positive</b></summary>
PyInstaller-built EXEs are commonly flagged. Add an exception or build the EXE yourself from source.
</details>

<details>
<summary><b>Fewer images in single-folder mode</b></summary>
Same-named files overwrite each other. Keep "Single folder" unchecked to use per-product subfolders.
</details>

<details>
<summary><b>Too many errors</b></summary>
Lower the thread count (10 → 5). The server might be rate-limiting.
</details>

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Tkinter** — GUI (stdlib)
- **openpyxl** — Excel parsing
- **concurrent.futures** — parallel downloads
- **PyInstaller** — EXE build
- **Pillow** — icon generation

## 📄 License

MIT — use it, modify it, distribute it. See [LICENSE](LICENSE).

## 👤 Author

**Ayberk Bağlan** — [@ayberkbgln](https://github.com/ayberkbgln)

> Contributions, issues, and PRs are welcome. Leave a ⭐ if it helped you!
