# 🔥 BİST OTOMATİK TARAMA SİSTEMİ

Her gün seans kapanışında otomatik olarak 650+ BİST hissesini tarar, güçlü sinyalleri filtreler ve Telegram'a gönderir.

## 📊 ÖZELLİKLER

✅ **Tamamen Ücretsiz** - GitHub Actions (2000 dakika/ay)
✅ **Tam Otomatik** - Her gün 16:15'te çalışır
✅ **Akıllı Filtreleme** - Sadece güçlü hisseler
✅ **PKART Formatı** - Profesyonel raporlar
✅ **Telegram Bildirimi** - Anında telefona

## 🎯 FİLTRE KRİTERLERİ

Sistem sadece şu kriterleri geçen hisseleri raporlar:

- ✅ ADX > 20 (güçlü trend)
- ✅ MFI > 45 (pozitif para akışı)
- ✅ VWAP Breakout > 2% (güçlü momentum)
- ✅ MTF Uyum (haftalık + aylık yükseliş)
- ✅ RSI 40-75 arası (sağlıklı)
- ✅ Stochastic K > D ve K > 40
- ✅ Risk/Ödül < 0.6 (düşük risk)

## 🚀 KURULUM (10 DAKİKA)

### 1️⃣ GitHub Repository Oluştur

1. GitHub'a git: https://github.com
2. "New Repository" tıkla
3. İsim: `bist-tarama`
4. Public seç
5. "Create repository" tıkla

### 2️⃣ Dosyaları Yükle

Repository'de "Add file" → "Upload files" tıkla ve şu dosyaları yükle:

```
bist-tarama/
├── bist_tarama.py          (ana script)
├── requirements.txt        (bağımlılıklar)
└── .github/
    └── workflows/
        └── tarama.yml      (otomatik çalışma)
```

**ÖNEMLİ:** `.github/workflows/` klasör yapısını aynen koru!

### 3️⃣ GitHub Secrets Ekle

Repository'de:
1. "Settings" → "Secrets and variables" → "Actions"
2. "New repository secret" tıkla

**Secret 1:**
- Name: `TELEGRAM_TOKEN`
- Value: `8455173046:AAECKdZcTVnt3naPDzI3udwwfj23nyv4uMs`

**Secret 2:**
- Name: `TELEGRAM_CHAT_ID`
- Value: `-1003670397485`

### 4️⃣ GitHub Actions'ı Aktifleştir

1. Repository'de "Actions" sekmesine git
2. "I understand my workflows, go ahead and enable them" tıkla
3. TAMAM! ✅

## 🧪 TEST (İLK ÇALIŞTIRMA)

Manuel test için:

1. "Actions" → "BİST Günlük Tarama"
2. "Run workflow" → "Run workflow"
3. 10-15 dakika bekle
4. Telegram'dan raporları al! 📱

## ⏰ OTOMATİK ÇALIŞMA

Her iş günü **16:15**'te otomatik çalışır (seans kapanışı sonrası).

Zamanı değiştirmek için `tarama.yml` dosyasında:
```yaml
cron: '15 13 * * 1-5'  # 13:15 UTC = 16:15 TR
```

## 📱 RAPOR FORMATI

```
📊 TEKNİK ANALİZ RAPORU

PKART

Hisse 79.20 TL seviyesinde. ADX 26.6 ile güçlü yükseliş 
trendi ve MFI 64.7 ile pozitif para akışı görülüyor. 
VWAP 76.15 TL üzerinde güçlü bir breakout gerçekleşmiş 
(%4.0). 69.20 TL (5x test) desteği korundukça 81.83 TL 
hedefi hedeflenebilir. MTF güçlü uyum (haftalık+aylık 
yükseliş) ✅ gösterirken, RSI 58.2 ve Stochastic 
K=54.9 / D=37.3 seviyeleri dikkat çekiyor; düşük 
Risk/Ödül oranı (0.23) ise bir risk faktörüdür.

SKOR: 87/100 ⭐⭐⭐⭐
```

## ❓ SORUN GİDERME

### Hata: "Workflow not found"
- `.github/workflows/` klasör yapısını kontrol et
- `tarama.yml` dosya adını kontrol et

### Hata: "Secrets not found"
- Secrets'ı doğru ekledin mi?
- İsimleri tam yazdın mı? (TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)

### Telegram'a mesaj gelmiyor
- Bot token doğru mu?
- Chat ID doğru mu?
- Bot'u gruba ekledin mi?

### "No strong signals found"
- Normal! Bazı günler güçlü hisse olmayabilir
- Filtreyi yumuşatmak için `bist_tarama.py` dosyasında:
  - `adx > 20` → `adx > 15`
  - `mfi > 45` → `mfi > 40`
  - `vwap_breakout > 2.0` → `vwap_breakout > 1.5`

## 📊 İSTATİSTİKLER

- **Toplam hisse:** 650+
- **Tarama süresi:** 10-15 dakika
- **Günlük kullanım:** ~15 dakika
- **Aylık kullanım:** ~300 dakika (2000 limitin %15'i)
- **Ortalama güçlü hisse:** 10-25/gün

## 🔒 GÜVENLİK

- Token'lar GitHub Secrets'ta şifreli
- Public repo olsa bile token'lar görünmez
- Sadece GitHub Actions erişebilir

## 📞 DESTEK

GitHub Issues kullan: https://github.com/[kullanici-adin]/bist-tarama/issues

## 📜 LİSANS

MIT License - Özgürce kullan!

---

**YAPIMCI:** BİST Algo Trading Team 🇹🇷
**VERSİYON:** 1.0.0
**GÜNCELLEME:** 27.02.2026
