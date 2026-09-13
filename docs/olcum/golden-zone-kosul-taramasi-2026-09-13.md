# golden-zone — Koşul Taraması

**Tarih:** 2026-09-13 · **Gösterge:** `golden_zone`

K4 şunu bulmuştu: Golden Zone **tek başına** kenar üretmiyor. Bu tarama
sorunun devamını yanıtlıyor: *başka bir göstergenin koşuluyla birlikte
tutarlı hâle geliyor mu?*

| | |
|---|---|
| Denenen koşul | 35 |
| Arama | **A grubu sembol + IS penceresi** (ilk %70) —
977 işlem, 103 sembol |
| Doğrulama | **B grubu sembol + OOS penceresi** (son %30) —
4282 işlem, 260 sembol |
| Koşulsuz taban (IS) | +0.071R (adil baz +0.047R) |
| Koşulsuz taban (OOS) | +0.037R (adil baz +0.027R) |

## 1. Arama (IS penceresi)

`ΔR` koşulun **eklediği** R: koşullu R eksi koşulsuz taban. ⚠ işareti
30 işlemin altını gösterir — sayı yazılır, verdikt yazılmaz.

| Koşul | Hipotez | İşlem | Ort. R | ΔR | ham p | BH-FDR (q=0.05) |
|---|---|---|---|---|---|---|
| `ema_uzak` | Fiyat EMA50'den 2 ATR'den uzak | 60 | +0.530R | +0.459R | 0.0160 | — |
| `ema50_uyum` | Fiyat EMA50'nin doğru tarafında — 'trendle işlem yap' | 402 | +0.259R | +0.188R | 0.1344 | — |
| `bb_sikisma` | Bollinger genişliği son 120 barın alt %30'unda | 220 | +0.248R | +0.177R | 0.0310 | — |
| `ema50_ve_egim` | EMA50 hem seviye hem eğim olarak uyumlu | 384 | +0.243R | +0.173R | 0.2294 | — |
| `ema200_uyum` | Fiyat EMA200'ün doğru tarafında — uzun vadeli eğilim | 206 | +0.221R | +0.150R | 0.7716 | — |
| `macd_uyum` | MACD histogramı sinyal yönünde | 447 | +0.204R | +0.133R | 0.0115 | — |
| `hacim_yuksek` | Kırılım hacmi 20 bar ortalamasının 1.5 katı üstünde | 332 | +0.170R | +0.099R | 0.9260 | — |
| `hacim_cok_yuksek` | Kırılım hacmi 2 kat üstünde | 214 | +0.139R | +0.068R | 0.8566 | — |
| `donus_hizli` | Kırılımdan bölgeye 5 barda dönülmüş | 403 | +0.139R | +0.068R | 0.1864 | — |
| `rsi_zayif` | RSI 45 altı — derin düzeltme | 192 | +0.135R | +0.064R | 0.4803 | — |
| `obv_uyum` | OBV eğimi sinyal yönünde — hacim fiyatı teyit ediyor | 496 | +0.134R | +0.063R | 0.4913 | — |
| `oynaklik_dusuk` | ATR14/ATR50 < 1 — sakin rejim | 464 | +0.132R | +0.062R | 0.0055 | — |
| `adx_guclu` | ADX 25 üstü — belirgin trend | 376 | +0.115R | +0.045R | 0.6107 | — |
| `aralik_genis` | Sinyal barının aralığı 1.5 ATR üstü | 369 | +0.097R | +0.027R | 0.5392 | — |
| `ema_yakin` | Fiyat EMA50'ye 1 ATR'den yakın — aşırı uzaklaşmamış | 498 | +0.081R | +0.010R | 0.9645 | — |
| `ema_egim_uyum` | EMA50'nin EĞİMİ sinyal yönünde — seviye değil yön | 616 | +0.076R | +0.005R | 0.9895 | — |
| `endeks_yukselen` | XU100 kendi EMA50'sinin üstünde — piyasa rejimi | 531 | +0.071R | +0.000R | 0.3853 | — |
| `rejim_ve_yon` | Piyasa rejimi sinyal yönüyle uyumlu (yükselen piyasada AL) | 472 | +0.071R | +0.000R | 0.6487 | — |
| `endeks_dusen` | XU100 EMA50'sinin altında | 446 | +0.071R | -0.000R | 0.7836 | — |
| `likit` | Ortalama ciro 20 milyon TL üstü | 884 | +0.063R | -0.007R | 0.5367 | — |
| `ema20_50_uyum` | EMA20/EMA50 dizilimi sinyal yönünde | 558 | +0.063R | -0.008R | 0.9885 | — |
| `rsi_notr` | RSI 40-60 — düzeltme tükenmemiş | 826 | +0.062R | -0.008R | 0.8161 | — |
| `bacak_guclu` | Yer değiştirme bacağı 3 ATR'den uzun | 788 | +0.060R | -0.011R | 0.4428 | — |
| `adx_zayif` | ADX 20 altı — yatay/sıkışık piyasa | 386 | +0.038R | -0.033R | 0.6017 | — |
| `cok_likit` | Ortalama ciro 100 milyon TL üstü | 390 | +0.024R | -0.047R | 0.8906 | — |
| `stok_dusuk` | Stokastik %K 30 altı — düzeltme derinleşmiş | 243 | +0.014R | -0.057R | 0.9990 | — |
| `fvg` | Bacakta adil değer boşluğu var | 603 | +0.002R | -0.068R | 0.5322 | — |
| `rsi_guclu` | RSI 55 üstü — momentum sinyal yönünde | 263 | -0.008R | -0.079R | 0.1819 | — |
| `supurme` | Kurulum likidite süpürmesiyle başlamış | 176 | -0.034R | -0.105R | 0.8736 | — |
| `oynaklik_yuksek` | ATR14/ATR50 > 1.2 — genişleyen oynaklık | 119 | -0.039R | -0.110R | 0.9975 | — |
| `govde_guclu` | Sinyal barının gövdesi aralığın %60'ından büyük | 435 | -0.071R | -0.141R | 0.9925 | — |
| `donus_yavas` | Dönüş 10 bardan uzun sürmüş | 231 | -0.076R | -0.147R | 0.9885 | — |
| `derin_giris` | Bölgeye 0.705'in altına kadar girilmiş | 464 | -0.125R | -0.196R | 0.9985 | — |
| `bb_genis` | Bollinger genişliği üst %30'da | 116 | -0.132R | -0.203R | 0.9930 | — |
| `stok_yuksek` | Stokastik %K 70 üstü | 223 | -0.167R | -0.238R | 0.7811 | — |

> **Ham p'ye tek başına bakmak yanıltır.** 35 koşul denendi;
> düzeltme olmadan birinin tesadüfen 0.05'in altına düşmesi neredeyse
> kesindir. Karar sütunu BH-FDR'dir.

## 2. Doğrulama (OOS penceresi)

Yalnız BH-FDR'yi geçen ve örneklemi yeterli olan koşullar buraya iner.
**Rapora giren sayı budur**; arama penceresininki değil.

| Koşul | İşlem | Ort. R | Adil baz | ΔR | p | Aile FDR | Verdikt |
|---|---|---|---|---|---|---|---|
| `oynaklik_dusuk` | 2228 | +0.046R | -0.009R | +0.009R | 0.0125 | geçti | **kenar-var** |
| `macd_uyum` | 2230 | +0.133R | +0.049R | +0.096R | 0.0025 | geçti | **kenar-var** |

**Ön kayıtlı aile:** `macd_uyum`, `oynaklik_dusuk`. Bu 2 koşul, B grubu / OOS penceresine **BAKILMADAN ÖNCE** sabitlendi; seçim gerekçesi iki bağımsız arama koşusunda da en tutarlı sonucu vermeleriydi. BH-FDR bu küçük aileye uygulanır — 35 koşulluk aileninkinden gevşektir ve bu meşrudur, çünkü aile sonuca bakılarak seçilmedi.

## Ne çıkarsa o

**Bulgu: `macd_uyum` — MACD histogramının sinyal yönünde olması.**

B grubu sembollerde, OOS penceresinde, **işlem maliyeti dahil**:
+0.133R/işlem, koşulsuz taban +0.037R, **ΔR +0.096R**, p=0.0025.
İkinci sırada `oynaklik_dusuk`: +0.046R, ΔR +0.009R, p=0.0125.

Doğrulama penceresi arama sırasında **ne zaman ne sembol olarak görülmedi**.
İki koşul da ön kayıtlı ikili ailede BH-FDR'yi geçti.

### Neden bu sayıya diğerlerinden daha çok güvenilebilir

| | |
|---|---|
| Çift bölme | Farklı semboller **ve** farklı dönem |
| Ön kayıt | Aile, B/OOS'a bakılmadan sabitlendi |
| Maliyet | Ölçümün içinde, baza da uygulanmış |
| Tutarlılık | İki bağımsız arama koşusunda da üst sıralarda |

### Maliyet dayanıklılığı belirleyici farkı yaratıyor

`macd_uyum` gidiş-dönüş **%0.75** maliyette bile pozitif (+0.023R);
`oynaklik_dusuk` **%0.30** civarında sıfırlanıyor. Gerçek bir strateji
adayı olmak için gereken şey tam olarak bu: maliyetin makul aralığının
TAMAMINDA ayakta kalmak.

Ayrıntı: [`golden-zone-macd-maliyet-duyarliligi`](golden-zone-macd-maliyet-duyarliligi-2026-09-13.md)

### İlk turdaki 17 koşulluk aile ile farkı

İlk tarama 17 koşulla, bütün sembollerde koşulmuştu ve `oynaklik_dusuk`
tek geçen koşuldu. Koşul sayısı 35'e çıkıp arama yarım evrene inince
**hiçbiri FDR'yi geçemedi** — eşik sıkıldı, örneklem küçüldü. Bu bir
çelişki değil, çoklu testin fiyatı: aile büyüdükçe kanıt çıtası yükselir.

İkinci turda ön kayıtlı ikili aileyle doğrulama yapılabildi çünkü adaylar
**iki bağımsız arama koşusunda da** üst sıradaydı ve seçim B/OOS'a
bakılmadan yapıldı.

### Hâlâ yapılmamış olan

`macd_uyum` + `oynaklik_dusuk` **birlikte** denenmedi. Bu yeni bir hipotez
ve kendi ön kayıtlı testini hak ediyor — şimdi bakıp "daha da iyi" demek,
bu raporun önlemek için yazıldığı şey olurdu.

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
