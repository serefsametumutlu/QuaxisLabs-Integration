# golden-zone-r2 — K4 Katmanlı Ölçüm

**Tarih:** 2026-09-17 · **Gösterge:** `golden_zone_r2` · **Zaman dilimi:** 1D

Soru katman başına "kenar var mı" değil, **"kenar EKLİYOR mu"**. `ΔR` sütunu
bir önceki katmana göre işlem başına beklenen R değişimidir.

**Pencere:** her iki ölçüm de yalnız **OOS** penceresini sayar (serinin son
%30'i). İki sütun aynı dönemden konuşmazsa tablo sessizce yanıltır.

| Katman | İçerik | İşlem | Sembol | İsabet | Ort. R | Adil baz | ΔR | p (R) | Hedef/Stop/Zaman | İleri getiri | p | Verdikt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | yapı kırılımı + OTE bölgesi | 9909 | 599 | %36.9 | +0.032R | +0.055R | — | 0.9565 | %31 / %60 / %9 | %-0.39 | 0.8851 | kanitlanmadi |
| **B** | A + (FVG veya bölgedeki Order Block) | 7081 | 596 | %36.6 | +0.016R | +0.056R | -0.015R | 0.9955 | %30 / %60 / %10 | %-0.30 | 0.8001 | kanitlanmadi |
| **C** | B + likidite süpürmesi | 1242 | 497 | %37.0 | +0.024R | +0.031R | +0.008R | 0.2679 | %30 / %60 / %10 | %+0.19 | 0.3893 | kanitlanmadi |

## Katman başına aday sayımı (K3)

**A** — MAKUL: sembol başına ortalama 19.3 aday, sembollerin %2'i sıfır.
**B** — MAKUL: sembol başına ortalama 13.8 aday, sembollerin %2'i sıfır.
**C** — MAKUL: sembol başına ortalama 2.4 aday, sembollerin %12'i sıfır.

## Ne çıkarsa o

**Sabit 2R hedefle de kenar yok. Düzeltilmiş veri verdikti değiştirmedi.**

Bu, `golden_zone` künyesinin ikinci hedef modudur: bölge aynı, hedef sabit
2R. [`onkayit-veri-duzeltme.md`](onkayit-veri-duzeltme.md) §6 gereği
düzeltilmiş veriyle **bir kez** koşuldu.

Üç katmanın üçünde de sinyal adil bazın altında: A'da +0.032R'ye karşı
+0.055R. p değerleri 0.9565 · 0.9955 · 0.2679.

C katmanının p'si (0.2679) diğerlerinden düşük ama hâlâ eşiğin beş katı —
üstelik tek başına bakılmış bir p. Üç katman × iki hedef modu = altı testin
içinden seçilseydi çoklu test düzeltmesi onu daha da yukarı iterdi.

### 09-13 tablosuyla karşılaştırma

Ham `Ort. R` sütunları karşılaştırılamaz: 13 Eylül'ün tablosu işlem maliyeti
ölçüme girmeden önce üretildi (`b11de50`). Karşılaştırılabilen büyüklük
**fark**tır (strateji − adil baz); fark maliyete neredeyse duyarsızdır
([`golden-zone-maliyet-duyarliligi`](golden-zone-maliyet-duyarliligi-2026-09-13.md)).

| Katman | fark · 09-13 (maliyetsiz, 543 sembol) | fark · 09-17 (maliyetli, düzeltilmiş evren) |
|---|---|---|
| A | −0.022R | **−0.023R** |
| B | −0.046R | **−0.040R** |
| C | −0.018R | **−0.007R** |

C'de fark −0.018R'den −0.007R'ye çıktı ama hâlâ **negatif**, üstelik p 0.2679.
Ön kayıt §5'in birinci maddesi (fark pozitif) üç katmanda da sağlanmadı.

**VERDİKT DEĞİŞMEDİ: `kanıtlanmadı`** — üç katmanda da.

*(Katman ekledikçe R artıyorsa bu tek başına kanıt DEĞİLDİR: örneklem de
küçülüyor. Artış hem ΔR'de hem p değerinde görünmeli, ve işlem sayısı
30'un üstünde kalmalı. Aksi halde iyileşme kenardan değil
serbestlik derecesinden geliyordur — Pardo s.291-293.)*

## Ölçümün sınırları

| | |
|---|---|
| Dönem | 2010-01-01 – 2026-09-11; ölçüm yalnız **OOS** penceresinde (son %30) |
| Evren | Liste 648 sembol; **625**'inin verisi var, A katmanında **599** sembol ölçüldü. Kalan 23'te sağlayıcı veri döndürmüyor. |
| Veri düzeltmesi | D1–D4 uygulanmış veri ([`onkayit-veri-duzeltme.md`](onkayit-veri-duzeltme.md)) |
| İşlem maliyeti | **dahil** — taraf başına %0.05 komisyon + çıkışta %0.05
kayma. Giriş limit emir sayıldığı için kayma yemez; çıkış (stop/hedef)
piyasa emri gibi davranır. |
| Hayatta kalma yanlılığı | **VAR ve düzeltilemiyor** — evren bugünkü listeden ([`veri-denetimi-bist-1D.md`](veri-denetimi-bist-1D.md)) |
| Aynı barda stop+hedef | **stop** sayıldı (iyimserliğe karşı) |

> Bağımsız gözlem birimi **sembol**dür, bar değil.
