# Golden Zone — Nerede duruyoruz

**Tarih:** 2026-09-13 · **Evren:** 543 BIST sembolü · **Dönem:** 2010–2026
**Ölçüm penceresi:** son %30 (görülmemiş dönem) · **İşlem maliyeti:** dahil

> ⚠ **2026-09-17 · Bu özetin sayıları düzeltme ÖNCESİ evrendendir (543
> sembol).** Veri düzeltmesinden sonra K4 bir kez yeniden koşuldu: evren
> 625 sembol, A katmanı 9909 işlem / 599 sembol, fark −0.029R, p=0.9820.
> **Verdikt değişmedi (`kanıtlanmadı`).** Yeni tablolar:
> [`golden-zone-K4-katmanli-2026-09-17.md`](golden-zone-K4-katmanli-2026-09-17.md) ·
> gerekçe ve karar kuralı:
> [`onkayit-veri-duzeltme.md`](onkayit-veri-duzeltme.md) §8.
> Bu özet, o günkü kararın kaydı olarak **olduğu gibi** bırakıldı.

Bu belge, teknik rapor değil **özet**tir. Sayıların nasıl üretildiği
ayrı dosyalarda; burada ne anlama geldikleri yazıyor.

---

## Tek cümlelik cevap

**Golden Zone tek başına para kazandırmıyor.** Günlükte piyasanın kendi
verdiğinin altında, haftalıkta ise piyasayla neredeyse aynı. Tek bir
sektörde güçlü görünüyor ama o bulgu henüz kanıt değil, aday.

---

## 1. Hangi zaman diliminde kaç sinyal veriyor

| | **Günlük (1G)** | **Haftalık (1H)** |
|---|---|---|
| Toplam sinyal (16 yıl) | 10 417 | 3 764 |
| Ölçülen işlem (son %30) | 8 432 | 1 499 |
| Sembol başına yılda | ~1.2 | ~0.4 |
| **İsabet** | **%40.5** | **%47.0** |
| **Profit factor** | **1.03** | **1.28** |
| Ortalama kazanç | +1.51R | +1.22R |
| Ortalama kayıp | −1.00R | −0.85R |
| Hedefte / stopta / süre dolunca | %37 / %57 / %6 | %29 / %39 / %32 |

**4 saatlik ölçülemedi.** Veri sağlayıcı saatlik veriyi yalnız **son 2 yıl**
için veriyor (ölçtüm: 2024-09-13'ten bugüne, 4360 bar). Günlükte 16 yıllık
geçmiş varken 4S'te 2 yıl olur; bu kadar kısa pencerede çıkan sonuç
güvenilir olmaz. İstersen indirebiliriz ama sınırı bilerek.

---

## 2. Rakamların yanıltıcı kısmı

Yukarıdaki tabloya bakıp "haftalık çok daha iyi" demek doğal. **Ama eksik
bir sütun var:** aynı riskle *rastgele* bir barda girseydik ne olurdu?

| | Strateji | Rastgele giriş | **Fark** |
|---|---|---|---|
| Günlük | +0.018R | +0.044R | **−0.026R** |
| Haftalık | +0.124R | +0.111R | **+0.013R** |

Haftalıktaki +0.124R'nin neredeyse tamamı **piyasanın kendisinden** geliyor,
stratejiden değil. Aynı dönemde rastgele girip aynı stop/hedef yapısını
kullanan biri +0.111R alıyordu.

> **Profit factor 1.28 kulağa iyi geliyor ama tek başına yanıltır.** O
> dönemde piyasa yükseliyorsa rastgele girişin profit factor'ü de 1'in
> üstündedir. Karşılaştırma olmadan hiçbir orana anlam yüklenemez.

Günlükte durum daha net: strateji rastgele girişin **altında**.

---

## 3. Hangi sembollerde işe yarıyor

### Likidite ve fiyat: anlamlı bir ayrım yok

| Günlük | İşlem | İsabet | PF | Ort. R | Rastgele |
|---|---|---|---|---|---|
| En ince hisseler | 2 662 | %41.4 | 1.08 | +0.046R | — |
| En kalın hisseler | 1 673 | %38.1 | 0.93 | −0.044R | — |

Hafif bir eğilim var (ince hisselerde biraz daha iyi) ama istatistiksel
olarak ayırt edilemiyor. Fiyat ölçeğinde de fark yok.

### Sektörde iki uç var

**En iyi — ve tek istatistiksel olarak ayrışan:**

| Sektör | Sembol | İşlem | İsabet | PF | Ort. R | Rastgele | p |
|---|---|---|---|---|---|---|---|
| **Toptan ve Perakende Ticaret** | 9 | 134 | **%51.5** | **1.55** | **+0.259R** | −0.024R | **0.0013** |

**En kötü:**

| Sektör | Sembol | İşlem | İsabet | PF | Ort. R | Rastgele | p |
|---|---|---|---|---|---|---|---|
| **Bankacılık** | 12 | 213 | %28.2 | 0.59 | **−0.296R** | +0.054R | 1.0000 |

Aradaki fark çok büyük: perakendede 100 TL risk edip 26 TL kazanırken,
bankacılıkta 30 TL kaybediyorsun.

### Ama perakende bulgusuna henüz güvenme

Üç sebep:

1. **9 sembol, 134 işlem.** İstatistik için alt sınırın (30 işlem) üstünde
   ama rahat değil.
2. **22 sektör denendi.** 22 kutudan birinin tesadüfen parlaması beklenir.
   Çoklu test düzeltmesi uygulandı ve bu sektör geçti — ama düzeltme
   "tesadüf değil" garantisi vermez, ihtimalini düşürür.
3. **Bu bir keşif, doğrulama değil.** Sektörü *sonuca bakarak* seçtim. Onu
   gerçekten doğrulamak için: sektörü önceden ilan edip, dokunulmamış bir
   pencerede yeniden ölçmek gerekir.

Bankacılığın kötülüğü ise ters yönden aynı derecede ilginç: bankalar
BIST'in en likit, en çok takip edilen hisseleri. Bu tür kurulumların orada
çalışmaması, "herkesin baktığı yerde kenar kalmaz" fikriyle tutarlı.

---

## 4. Daha önce bulduğum şeye ne oldu

Geçen turda "MACD uyumu kenar üretiyor" demiştim (bir sembol grubunda
p=0.0025). **Onu geri çektim:** diğer sembol grubunda p=0.8166 çıktı. Aynı
dönem, aynı yöntem, farklı semboller — ve etki kayboldu.

Kombinasyon testi de (MACD + sakin oynaklık) önceden yazılmış kuralı
geçemedi. Kural önceden yazılmasaydı geçirirdim; en büyük ΔR'yi veriyordu.

---

## 5. Bundan sonra ne yapılabilir — üç seçenek

**A. Perakende bulgusunu düzgün sına.**
Sektörü önceden ilan et, dokunulmamış bir pencerede ölç. Tutarsa elimizde
dar ama gerçek bir şey olur: "Golden Zone, perakende hisselerinde haftalık".
Tutmazsa 22 kutudan biri tesadüfen parlamıştı demektir ve kapanır.

**B. Bankacılığı ters yönde kullan.**
Kenar simetrik olmak zorunda değil. "Bankalarda bu kurulumu alma" kuralı,
tek başına bir stratejiden çok bir **filtre** olarak değerlidir.

**C. Golden Zone'u bırak, ölçüm altyapısını başka stratejide kullan.**
Bu turda kurulan şey aslında strateji değil, **strateji sınama makinesi**:
üç bariyerli R, adil baz, IS/OOS + sembol bölmesi, çoklu test düzeltmesi,
işlem maliyeti, ön kayıt disiplini. Golden Zone bu makineden geçen ilk
strateji oldu ve geçemedi — makine çalışıyor demektir.

---

## Kaynak dosyalar

| Ne | Nerede |
|---|---|
| Günlük segment analizi | [`golden-zone-segment-1D-2026-09-13.md`](golden-zone-segment-1D-2026-09-13.md) |
| Haftalık segment analizi | [`golden-zone-segment-1W-2026-09-13.md`](golden-zone-segment-1W-2026-09-13.md) |
| 35 koşulluk tarama | [`golden-zone-kosul-taramasi-2026-09-13.md`](golden-zone-kosul-taramasi-2026-09-13.md) |
| Ön kayıtlı kombinasyon testi | [`onkayit-macd-oynaklik.md`](onkayit-macd-oynaklik.md) |
| Maliyet duyarlılığı | [`golden-zone-macd-maliyet-duyarliligi-2026-09-13.md`](golden-zone-macd-maliyet-duyarliligi-2026-09-13.md) |
| Veri kalitesi | [`veri-bist-1D-2026-09-13.md`](veri-bist-1D-2026-09-13.md) |
| Strateji pasaportu | [`../strateji/golden-zone.md`](../strateji/golden-zone.md) |

## Neyin ölçülmediği

| | |
|---|---|
| 4 saatlik | Saatlik veri yalnız 2 yıl geriye gidiyor |
| Kotasyondan çıkmış hisseler | Evren bugünkü listeden; hayatta kalma yanlılığı **var** |
| Vergi / stopaj | yok |
| Emrin dolmama riski | Giriş limit emir varsayıldı; dolmazsa işlem hiç açılmaz |
| Pozisyon büyüklüğü | Her işlem 1R risk varsayıldı; portföy etkisi modellenmedi |
