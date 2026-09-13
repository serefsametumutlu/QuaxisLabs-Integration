# golden-zone — Koşul Taraması

**Tarih:** 2026-09-13 · **Gösterge:** `golden_zone`

K4 şunu bulmuştu: Golden Zone **tek başına** kenar üretmiyor. Bu tarama
sorunun devamını yanıtlıyor: *başka bir göstergenin koşuluyla birlikte
tutarlı hâle geliyor mu?*

| | |
|---|---|
| Denenen koşul | 17 |
| Arama penceresi | **IS** (ilk %70) — 1960 işlem, 208 sembol |
| Doğrulama penceresi | **OOS** (son %30) — 8432 işlem |
| Koşulsuz taban (IS) | +0.069R (adil baz +0.058R) |
| Koşulsuz taban (OOS) | +0.018R (adil baz +0.045R) |

## 1. Arama (IS penceresi)

`ΔR` koşulun **eklediği** R: koşullu R eksi koşulsuz taban. ⚠ işareti
30 işlemin altını gösterir — sayı yazılır, verdikt yazılmaz.

| Koşul | Hipotez | İşlem | Ort. R | ΔR | ham p | BH-FDR (q=0.05) |
|---|---|---|---|---|---|---|
| `ema50_uyum` | Fiyat EMA50'nin doğru tarafında — 'trendle işlem yap' | 793 | +0.226R | +0.158R | 0.0350 | — |
| `ema50_ve_egim` | EMA50 hem seviye hem eğim olarak uyumlu | 761 | +0.210R | +0.141R | 0.1024 | — |
| `ema200_uyum` | Fiyat EMA200'ün doğru tarafında — uzun vadeli eğilim | 418 | +0.192R | +0.123R | 0.7216 | — |
| `oynaklik_dusuk` | ATR14/ATR50 < 1 — sakin rejim | 959 | +0.117R | +0.048R | 0.0010 | geçti |
| `hacim_yuksek` | Kırılım hacmi 20 bar ortalamasının 1.5 katı üstünde | 679 | +0.090R | +0.022R | 0.9805 | — |
| `ema_egim_uyum` | EMA50'nin EĞİMİ sinyal yönünde — seviye değil yön | 1232 | +0.083R | +0.015R | 0.8076 | — |
| `rsi_zayif` | RSI 45 altı — derin düzeltme | 402 | +0.079R | +0.011R | 0.8656 | — |
| `donus_hizli` | Kırılımdan bölgeye 5 barda dönülmüş | 784 | +0.076R | +0.007R | 0.5977 | — |
| `bacak_guclu` | Yer değiştirme bacağı 3 ATR'den uzun | 1551 | +0.066R | -0.003R | 0.1919 | — |
| `hacim_cok_yuksek` | Kırılım hacmi 2 kat üstünde | 433 | +0.060R | -0.009R | 0.9840 | — |
| `donus_yavas` | Dönüş 10 bardan uzun sürmüş | 462 | +0.059R | -0.009R | 0.5447 | — |
| `rsi_notr` | RSI 40-60 — düzeltme tükenmemiş | 1670 | +0.053R | -0.015R | 0.6392 | — |
| `oynaklik_yuksek` | ATR14/ATR50 > 1.2 — genişleyen oynaklık | 216 | +0.040R | -0.029R | 0.9970 | — |
| `rsi_guclu` | RSI 55 üstü — momentum sinyal yönünde | 505 | +0.024R | -0.045R | 0.0525 | — |
| `fvg` | Bacakta adil değer boşluğu var | 1206 | +0.007R | -0.062R | 0.7101 | — |
| `supurme` | Kurulum likidite süpürmesiyle başlamış | 362 | -0.010R | -0.079R | 0.7481 | — |
| `derin_giris` | Bölgeye 0.705'in altına kadar girilmiş | 919 | -0.132R | -0.201R | 1.0000 | — |

> **Ham p'ye tek başına bakmak yanıltır.** 17 koşul denendi;
> düzeltme olmadan birinin tesadüfen 0.05'in altına düşmesi neredeyse
> kesindir. Karar sütunu BH-FDR'dir.

## 2. Doğrulama (OOS penceresi)

Yalnız BH-FDR'yi geçen ve örneklemi yeterli olan koşullar buraya iner.
**Rapora giren sayı budur**; arama penceresininki değil.

| Koşul | İşlem | Ort. R | Adil baz | ΔR | p | Verdikt |
|---|---|---|---|---|---|---|
| `oynaklik_dusuk` | 4357 | +0.038R | -0.003R | +0.019R | 0.0095 | **kenar-var** |

## Ne çıkarsa o

*(Hiçbir koşul geçmediyse bu da bir sonuçtur ve öyle yazılır: "Golden Zone,
denenen 17 koşulun hiçbiriyle birlikte kenar üretmedi." Geçen
varsa, OOS sayısı IS sayısından belirgin düşükse bu aşırı uydurmanın
imzasıdır ve belirtilir.)*

## Ölçümün sınırları

| | |
|---|---|
| Çoklu test | BH-FDR uygulandı; yine de OOS doğrulaması TEK bir pencerede |
| Eşikler | Koşul eşikleri (EMA50, RSI 40-60, hacim 1.5×…) **denenmiş
değerlerdir**, optimize EDİLMEDİ — optimize edilseydi aşırı uydurma riski
katlanırdı |
| İşlem maliyeti | **dahil** — taraf başına %0.05 komisyon + çıkışta %0.05 kayma |
| Aynı barda stop+hedef | **stop** sayıldı |

> Bağımsız gözlem birimi **sembol**dür, bar değil.
