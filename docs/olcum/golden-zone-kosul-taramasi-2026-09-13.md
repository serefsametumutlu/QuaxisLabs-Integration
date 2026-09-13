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
| Koşulsuz taban (IS) | +0.094R (adil baz +0.083R) |
| Koşulsuz taban (OOS) | +0.045R (adil baz +0.071R) |

## 1. Arama (IS penceresi)

`ΔR` koşulun **eklediği** R: koşullu R eksi koşulsuz taban. ⚠ işareti
30 işlemin altını gösterir — sayı yazılır, verdikt yazılmaz.

| Koşul | Hipotez | İşlem | Ort. R | ΔR | ham p | BH-FDR (q=0.05) |
|---|---|---|---|---|---|---|
| `ema50_uyum` | Fiyat EMA50'nin doğru tarafında — 'trendle işlem yap' | 793 | +0.253R | +0.159R | 0.0355 | — |
| `ema50_ve_egim` | EMA50 hem seviye hem eğim olarak uyumlu | 761 | +0.236R | +0.143R | 0.1024 | — |
| `ema200_uyum` | Fiyat EMA200'ün doğru tarafında — uzun vadeli eğilim | 418 | +0.216R | +0.122R | 0.7221 | — |
| `oynaklik_dusuk` | ATR14/ATR50 < 1 — sakin rejim | 959 | +0.147R | +0.053R | 0.0010 | geçti |
| `hacim_yuksek` | Kırılım hacmi 20 bar ortalamasının 1.5 katı üstünde | 679 | +0.113R | +0.019R | 0.9810 | — |
| `ema_egim_uyum` | EMA50'nin EĞİMİ sinyal yönünde — seviye değil yön | 1232 | +0.108R | +0.014R | 0.8086 | — |
| `donus_hizli` | Kırılımdan bölgeye 5 barda dönülmüş | 784 | +0.106R | +0.012R | 0.5992 | — |
| `rsi_zayif` | RSI 45 altı — derin düzeltme | 402 | +0.104R | +0.010R | 0.8681 | — |
| `bacak_guclu` | Yer değiştirme bacağı 3 ATR'den uzun | 1551 | +0.087R | -0.007R | 0.1944 | — |
| `hacim_cok_yuksek` | Kırılım hacmi 2 kat üstünde | 433 | +0.081R | -0.013R | 0.9840 | — |
| `rsi_notr` | RSI 40-60 — düzeltme tükenmemiş | 1670 | +0.079R | -0.015R | 0.6412 | — |
| `donus_yavas` | Dönüş 10 bardan uzun sürmüş | 462 | +0.078R | -0.016R | 0.5462 | — |
| `oynaklik_yuksek` | ATR14/ATR50 > 1.2 — genişleyen oynaklık | 216 | +0.056R | -0.038R | 0.9970 | — |
| `rsi_guclu` | RSI 55 üstü — momentum sinyal yönünde | 505 | +0.048R | -0.046R | 0.0515 | — |
| `fvg` | Bacakta adil değer boşluğu var | 1206 | +0.030R | -0.064R | 0.7106 | — |
| `supurme` | Kurulum likidite süpürmesiyle başlamış | 362 | +0.014R | -0.080R | 0.7496 | — |
| `derin_giris` | Bölgeye 0.705'in altına kadar girilmiş | 919 | -0.104R | -0.198R | 1.0000 | — |

> **Ham p'ye tek başına bakmak yanıltır.** 17 koşul denendi;
> düzeltme olmadan birinin tesadüfen 0.05'in altına düşmesi neredeyse
> kesindir. Karar sütunu BH-FDR'dir.

## 2. Doğrulama (OOS penceresi)

Yalnız BH-FDR'yi geçen ve örneklemi yeterli olan koşullar buraya iner.
**Rapora giren sayı budur**; arama penceresininki değil.

| Koşul | İşlem | Ort. R | Adil baz | ΔR | p | Verdikt |
|---|---|---|---|---|---|---|
| `oynaklik_dusuk` | 4357 | +0.069R | +0.028R | +0.024R | 0.0095 | **kenar-var** |

## Ne çıkarsa o

**Bir koşul hayatta kaldı: `oynaklik_dusuk` (ATR14/ATR50 < 1 — sakin rejim).**
17 koşul içinde BH-FDR'yi geçen tek koşul (IS: p=0.0010) ve OOS'ta da aynı
yönde doğrulandı: 4357 işlem, +0.069R, adil baz +0.028R, p=0.0095.

Mekanizma makul: stop mesafesi bölgenin geometrisinden geliyor ve sabit;
oynaklık uzun vadeli ortalamasının altındayken aynı stop gürültüye daha az
takılıyor.

### Üç çekince, üçü de belirleyici

**1. Etki işlem maliyetiyle AYNI büyüklükte.** Medyan risk mesafesi fiyatın
%4.4'ü. Gidiş-dönüş maliyet %0.3 ise bu **0.068R** eder:

| Gidiş-dönüş maliyet | R cinsinden |
|---|---|
| %0.2 | 0.045R |
| %0.3 | 0.068R |
| %0.4 | 0.090R |

Ölçülen mutlak getiri +0.069R; **maliyeti ancak karşılıyor.** Koşulsuz tabana
göre kazanç (+0.024R) ise maliyetin belirgin **altında**. Bu ölçümde komisyon,
spread ve kayma **yok**.

**2. ΔR arama penceresinden doğrulamaya yarıya düştü** (+0.053R → +0.024R).
Aramanın bir kısmı gürültüye uymuş. Yön aynı kaldığı için bulgu tamamen
çürümedi, ama büyüklüğüne güvenilmez.

**3. En büyük ΔR'yi veren koşul geçemedi.** `ema50_uyum` IS'te +0.159R ekledi
(ham p=0.0355) ama 17 testlik ailede BH-FDR'yi geçemedi. Bu **reddedildi
demek değil, kanıtlanmadı demek** — ve tam bu yüzden OOS'ta denenmedi:
FDR'yi geçmeyeni "yine de bir bakalım" diye doğrulama penceresine sokmak,
bu aracın önlemek için yazıldığı şey.

### Ham p ile ΔR neden bazen ters yönde

`rsi_guclu` ham p=0.0515 ama ΔR negatif. İkisi **farklı iki karşılaştırma**:
ham p koşullu işlemleri kendi adil bazına (aynı risk yapısıyla rastgele bar)
karşı ölçer; ΔR ise koşulsuz tabana karşı. Bir koşul piyasayı yenip yine de
koşulsuz hâlden kötü olabilir. Karar için **ikisi birden** okunmalı.

### Sonuç

Golden Zone, denenen 17 koşuldan **biriyle** istatistiksel olarak ayrışıyor —
ama ayrışmanın büyüklüğü işlem maliyetinin altında. *Ölçüm bir sinyal buldu;
o sinyal para kazandıracak büyüklükte değil.*

**Bir sonraki zorunlu adım ölçümde, stratejide değil:** işlem maliyeti
ölçüme girmeden bu tablonun hiçbir satırı karar verdiremez.

## Ölçümün sınırları

| | |
|---|---|
| Çoklu test | BH-FDR uygulandı; yine de OOS doğrulaması TEK bir pencerede |
| Eşikler | Koşul eşikleri (EMA50, RSI 40-60, hacim 1.5×…) **denenmiş
değerlerdir**, optimize EDİLMEDİ — optimize edilseydi aşırı uydurma riski
katlanırdı |
| İşlem maliyeti | yok |
| Aynı barda stop+hedef | **stop** sayıldı |

> Bağımsız gözlem birimi **sembol**dür, bar değil.
