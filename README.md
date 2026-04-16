# 📥 Excel Image Downloader

Excel dosyalarındaki URL linklerinden toplu resim indirme aracı. Modern koyu tema arayüz, paralel indirme, resume desteği ve canlı log ile.

> **TR:** Excel'in içinde URL olarak duran binlerce resim linkini otomatik indirip, istersen her ürün için ayrı klasöre, istersen tek klasöre toplar.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

---

## ✨ Özellikler

- 🌙 **Modern koyu tema** — rahat göz için
- ⚡ **Paralel indirme** — 1-32 thread slider ile ayarlanabilir
- ↷ **Resume (kaldığı yerden devam)** — var olan dosyaları atlar
- 📁 **İki mod:** her ürün ayrı klasöre **veya** hepsi tek klasöre
- ⏹ **Durdur butonu** — istediğin an temiz durur
- 📊 **Canlı hız + ETA** — "15.3/sn • kalan ~2sa 14dk"
- 📝 **Hata raporu** — başarısız URL'ler `hatalar.txt`'ye yazılır
- 🔢 **3'lü canlı sayaç** — OK • ATLANAN • HATA
- 🧵 **Büyük Excel desteği** — 100.000+ satır, `read_only` modla RAM yemez

---

## 🚀 Hızlı Başlangıç

### Seçenek 1: Hazır EXE (Windows)

1. [Releases](../../releases) sayfasından en son `ResimIndirici.exe`'yi indir
2. Çift tıkla, çalıştır
3. Python kurmaya gerek yok ✅

> ⚠️ Windows SmartScreen uyarısı çıkarsa: *"Daha fazla bilgi → Yine de çalıştır"*. İmzalı değil çünkü (false positive).

### Seçenek 2: Kaynak koddan çalıştır

```bash
git clone https://github.com/ayberkbgln/excel-image-downloader.git
cd excel-image-downloader
pip install -r requirements.txt
python app.py
```

### Seçenek 3: Kendi EXE'ni build et

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

---

## 📋 Excel Formatı

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

---

## 🎛️ Kullanım

1. **Excel Dosyası:** `.xlsx` veya `.xlsm` seç
2. **Çıktı Klasörü:** resimlerin ineceği yer (otomatik `indirilen` oluşur)
3. **Paralel İndirme:** 10 thread genelde ideal (sunucuyu bunaltmaz)
4. **Opsiyonlar:**
   - ☑ **Var olan dosyaları atla** — yarıda kalınca tekrar çalıştır, kaldığı yerden devam eder
   - ☐ **Tek klasöre indir** — hepsini çıktı klasörüne atar, alt klasör açmaz
5. **▶ İNDİRMEYİ BAŞLAT**

---

## 🔧 Dosya Adlandırma

URL'deki `Product/` kelimesinden sonraki kısım dosya adı olur:

```
https://cdn.example.com/Uploads/Product/11680150_40400_2.jpg
                               ↓
                       11680150_40400_2.jpg
```

Eğer `Product/` yoksa URL'nin son kısmı alınır.

---

## 📊 Performans

| Resim Sayısı | Thread | Tahmini Süre |
|---|---|---|
| 100 | 10 | ~15 sn |
| 1.000 | 10 | ~2-3 dk |
| 10.000 | 10 | ~20-30 dk |
| 100.000 | 15 | ~3-5 saat |

*Sunucu hızına ve internet bağlantısına göre değişir.*

---

## 🐛 Sık Karşılaşılan Sorunlar

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

## 🛠️ Teknoloji

- **Python 3.8+**
- **Tkinter** — GUI (standart kütüphane)
- **openpyxl** — Excel okuma
- **concurrent.futures** — paralel indirme
- **PyInstaller** — EXE build
- **Pillow** — icon üretimi

---

## 📄 Lisans

MIT — istediğin gibi kullan, değiştir, dağıt. Detay: [LICENSE](LICENSE)

---

## 👤 Geliştirici

**Ayberk Bağlan** — [@ayberkbgln](https://github.com/ayberkbgln)

> Katkı / issue / PR her zaman açık. Yıldız bırakırsan sevinirim ⭐
