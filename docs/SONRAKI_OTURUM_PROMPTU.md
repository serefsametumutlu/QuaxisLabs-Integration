# Sonraki oturum promptu — Faz 7.1 (Golden Zone · K3'ten devam)

Aşağıdaki bloğu **olduğu gibi kopyalayıp** temiz bir oturuma (`/clear` sonrası)
yapıştır. Çalışma dizini `C:\Users\Samet\Desktop\QuaxisLabs` olmalı.

---

```
QuaxisLabs — Faz 7.1 Golden Zone (ICT OTE), K3 kapısından devam ediyoruz.

ÖNCE ŞUNLARI OKU (sırayla, tamamını):
1. docs/strateji/kaynak/golden-zone-K0.md   (kuralın kaynağı — mekanik + yöntem)
2. docs/strateji/golden-zone.md             (pasaport — hangi kapı nerede)
3. packages/teknik/quaxis/teknik/indicators/golden_zone/dedektor.py
4. tools/katmanli_olcum.py                  (katmanlı K3+K4 koşucusu)

DURUM: K0 yazıldı (bilerek AÇIK), K1/K2 bitti ve push edildi.
Sıradaki iş K3: gerçek evrende kalibrasyon + katmanlı K4.

İLK KOMUT (veri indi mi diye bak, eksikse tamamla):
  ls data/ohlcv/bist | wc -l        # 648'e yakın olmalı
  python tools/veri_cek.py --market bist --zaman-dilimi 1D --atla-var-olani

SONRA katmanlı ölçümü koş:
  python tools/katmanli_olcum.py \
    --katalog "quaxis.teknik.indicators.katalog:KATALOG" \
    --gosterge golden_zone --slug golden-zone --zaman-dilimi 1D --ufuk 20

Sonuç ne çıkarsa pasaporta ve rapora O yazılır. "Kenar yok" da bir sonuçtur.
```

---

## Nerede kaldık (2026-09-13 gecesi)

### Bitenler — hepsi commit + push edildi

| Commit | Ne |
|---|---|
| `c4824f9` | **K4'e üç bariyerli R ölçümü** — `olcum/bariyer.py` + 12 test |
| `bc7ba10` | **Adlandırma düzeltmesi** — `altin_bolge` → `swing_fib_abcd` |
| `620c79e` | **K0 kaynak dosyası** + pasaport doğrulayıcısının sıkılaştırılması |
| `e6c66c5` | **K1/K2 dedektör** — `indicators/golden_zone/` + 12 test |
| `eb731bd` | **Araçlar** — `tools/veri_cek.py`, `tools/katmanli_olcum.py` |

Depo durumu: **197 test yeşil**, `ruff` temiz, `npm run build` ve
`npm run lint` temiz.

### Yarım kalan tek şey: veri indirmesi

Oturum kapandığında `data/ohlcv/bist/` altında **267/648** sembol vardı.
`tools/veri_cek.py --atla-var-olani` ile kaldığı yerden devam eder; arttırımlı
çalışır, baştan indirmez. Sembol başına ~2.7 sn, kalan ~20 dakika.

Bazı semboller (ör. `BAKAB`) sağlayıcıdan **OHLC tutarsız** veri geliyor
(`high < close`). Araç bunları sessizce atlamaz, **hata olarak sayar** ve K3
raporunda "veri hatası alan sembol" sütununda görünürler.

### Kapı durumu

| Kapı | Durum | Not |
|---|---|---|
| K0 Kaynak | **bilerek AÇIK** | Karar "eşiklerin tamamı K3'ten türetilsin" olduğu için K0 ancak K3 raporu yazılınca kapanır. `pasaport.py dogrula` şu an temiz çünkü kapı `null`. |
| K1 Sözleşme | kod hazır, kapı işaretlenmedi | `parametreler.py` frozen, `params_hash` deterministik |
| K2 Dedektör | kod hazır, **repaint testi geçti** | walk-forward eşitlik, 260 bar / 35 kesim |
| K3 Kalibrasyon | **SIRADAKİ** | veri tamamlanınca koşulacak |
| K4 İstatistik | katmanlı koşucu hazır | K3'ten sonra |
| K5 Görsel | başlanmadı | Golden Zone kendi komposerini alacak |
| K6 Ürün | başlanmadı | |

### Kararlar (değiştirmeden önce nedenini oku)

* **Bölge:** ICT OTE 0.62–0.79, orta eşik 0.705 — hepsi **geçici**, K3'ten
  türetilecek.
* **Teyit:** BOS + bölge + (FVG veya Order Block) — ama dedektör bunları
  **filtrelemiyor**, payload'a bayrak yazıyor. Katmanlar dedektörde
  sabitlenirse hangisinin kenar *eklediği* ölçülemez.
* **Katmanlar:** A = BOS+OTE · B = A + (FVG veya bölgedeki OB) · C = B + süpürme.
  Soru "kenar var mı" değil **"kenar EKLİYOR mu"**.
* **Örneklem tabanı:** 30 işlemin altındaki katman sayı üretir, **verdikt
  üretmez** (Pardo s.295).
* **Aynı barda stop+hedef → stop.** Bar içi sıralama bilinmiyor; belirsizlikte
  stratejinin lehine varsaymıyoruz.
* **Geçersizlik:** %100 çıpasının ötesinde **gövde** kapanışı. Wick geçebilir.

### İlk koşuda beklenecek şey

2 sembollük deneme koşusunda (ISCTR, TCELL) üç katman da `kanitlanmadi`
verdi — örneklem anlamsız derecede küçüktü, makinenin çalıştığını gösterdi
sadece. Gerçek evrende sonuç ne çıkarsa yazılacak; **olumsuz sonuç da
sonuçtur** ve pasaporta öyle geçer.
