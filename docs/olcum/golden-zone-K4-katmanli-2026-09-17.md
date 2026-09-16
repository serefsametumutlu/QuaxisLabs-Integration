# golden-zone — K4 Katmanlı Ölçüm

**Tarih:** 2026-09-17 · **Gösterge:** `golden_zone` · **Zaman dilimi:** 1D

Soru katman başına "kenar var mı" değil, **"kenar EKLİYOR mu"**. `ΔR` sütunu
bir önceki katmana göre işlem başına beklenen R değişimidir.

**Pencere:** her iki ölçüm de yalnız **OOS** penceresini sayar (serinin son
%30'i). İki sütun aynı dönemden konuşmazsa tablo sessizce yanıltır.

| Katman | İçerik | İşlem | Sembol | İsabet | Ort. R | Adil baz | ΔR | p (R) | Hedef/Stop/Zaman | İleri getiri | p | Verdikt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | yapı kırılımı + OTE bölgesi | 9909 | 599 | %40.3 | +0.016R | +0.045R | — | 0.9820 | %37 / %57 / %6 | %-0.39 | 0.8851 | kanitlanmadi |
| **B** | A + (FVG veya bölgedeki Order Block) | 7081 | 596 | %39.7 | -0.002R | +0.047R | -0.018R | 0.9975 | %36 / %57 / %7 | %-0.30 | 0.8001 | kanitlanmadi |
| **C** | B + likidite süpürmesi | 1242 | 497 | %39.5 | -0.016R | +0.024R | -0.014R | 0.6062 | %35 / %57 / %8 | %+0.19 | 0.3893 | kanitlanmadi |

## Katman başına aday sayımı (K3)

**A** — MAKUL: sembol başına ortalama 19.3 aday, sembollerin %2'i sıfır.
**B** — MAKUL: sembol başına ortalama 13.8 aday, sembollerin %2'i sıfır.
**C** — MAKUL: sembol başına ortalama 2.4 aday, sembollerin %12'i sıfır.

## Ne çıkarsa o

**Kenar yine bulunamadı. Düzeltilmiş veri verdikti değiştirmedi.**

Bu ölçüm, [`onkayit-veri-duzeltme.md`](onkayit-veri-duzeltme.md) §6 gereği
düzeltilmiş veriyle yapılan **tek** koşudur. Evren büyüdü: A katmanında
518 → **599** sembol, 8432 → **9909** işlem.

Üç katmanın üçünde de sinyal, aynı risk yapısıyla rastgele barlardan
girmekten daha iyi değil — A'da +0.016R'ye karşı adil baz +0.045R. p
değerleri 0.05'in çok uzağında (0.9820 · 0.9975 · 0.6062); bu "ölçüm
kararsız kaldı" değil, "aranan yönde iz yok" demek.

Katman ekledikçe durum yine **kötüleşti**: ΔR B'de −0.018R, C'de −0.014R.
Meta-etiketleme hipotezi (López de Prado s.51–53) düzeltilmiş veride de
doğrulanmadı.

### 09-13 tablosuyla karşılaştırma — dikkat, iki şey birden değişti

13 Eylül'ün katmanlı tablosu **işlem maliyeti ölçüme girmeden önce**
üretildi (maliyet aynı gün, o rapordan sonra `b11de50` ile girdi). Ham `Ort.
R` sütunları bu yüzden yan yana konamaz: aradaki düşüşün ne kadarı veri
düzeltmesi, ne kadarı maliyet — ayrılamaz.

Karşılaştırılabilen tek büyüklük **fark**tır (strateji − adil baz). Maliyet
hem sinyale hem baza neredeyse aynı kadar bindiği için fark maliyete
duyarsız; bu bir varsayım değil, ölçüldü:
[`golden-zone-maliyet-duyarliligi`](golden-zone-maliyet-duyarliligi-2026-09-13.md)
altı maliyet düzeyinde p'yi sabit (0.0093) buldu.

| Katman | fark · 09-13 (maliyetsiz, 543 sembollük evren) | fark · 09-17 (maliyetli, düzeltilmiş evren) |
|---|---|---|
| A | −0.026R | **−0.029R** |
| B | −0.053R | **−0.049R** |
| C | −0.047R | **−0.040R** |

Fark üç katmanda da negatif kaldı. Ön kayıt §5'in **birinci** maddesi
(*fark pozitif*) sağlanmadı; ikinci ve üçüncü maddeye bakmaya gerek yok.

**VERDİKT DEĞİŞMEDİ: `kanıtlanmadı`** — üç katmanda da.

### Sinyal sayısı düşmedi, arttı

Ön kayıt §5 "sinyal sayısı %20'den fazla düşerse sebebi incelenir" diyordu.
Düşmedi: D2 (hacimsiz barda sinyal doğmaz) sinyal keserken D3 (bar atılır,
sembol atılmaz) 81 sembol ekledi ve ikincisi baskın çıktı — ham sinyal
+%17.5. İncelemeyi gerektiren durum oluşmadı.

*(Katman ekledikçe R artıyorsa bu tek başına kanıt DEĞİLDİR: örneklem de
küçülüyor. Artış hem ΔR'de hem p değerinde görünmeli, ve işlem sayısı
30'un üstünde kalmalı. Aksi halde iyileşme kenardan değil
serbestlik derecesinden geliyordur — Pardo s.291-293.)*

## Ölçümün sınırları

| | |
|---|---|
| Dönem | 2010-01-01 – 2026-09-11; ölçüm yalnız **OOS** penceresinde (son %30) |
| Evren | Liste 648 sembol; **625**'inin verisi var, A katmanında **599** sembol ölçüldü. Kalan 23'te sağlayıcı veri döndürmüyor. |
| Veri düzeltmesi | D1–D4 uygulanmış veri ([`onkayit-veri-duzeltme.md`](onkayit-veri-duzeltme.md)): hacimsiz bar ne baza girer ne sinyal doğurur; OHLC ihlalinde **bar** atılır, sembol atılmaz. |
| İşlem maliyeti | **dahil** — taraf başına %0.05 komisyon + çıkışta %0.05
kayma. Giriş limit emir sayıldığı için kayma yemez; çıkış (stop/hedef)
piyasa emri gibi davranır. |
| Hayatta kalma yanlılığı | **VAR ve düzeltilemiyor.** 625/625 sembolün son barı 2026'da; 2010–2026 arasında kottan çıkmış hiçbir şirket evrende yok ([`veri-denetimi-bist-1D.md`](veri-denetimi-bist-1D.md)). |
| Aynı barda stop+hedef | **stop** sayıldı (iyimserliğe karşı) |

> Bağımsız gözlem birimi **sembol**dür, bar değil.
