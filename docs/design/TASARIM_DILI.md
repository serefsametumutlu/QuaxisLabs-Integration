# Tasarım Dili — dört referans sitenin ortak paydası

**Tarih:** 2026-09-12
**Referanslar (kullanıcı tarafından verildi):** dovetail.com · slash.com ·
v7labs.com · luxalgo.com
**Yöntem:** Her site 1440×900 masaüstü genişliğinde gezildi; ekran görüntüsü
alındı **ve** sayfadaki ilk 4000 öğenin `getComputedStyle` değerleri toplanarak
gerçek token dağılımı çıkarıldı (tahmin değil, ölçüm). Ham veri:
[`references/referans_token_olcumleri.json`](../../references/referans_token_olcumleri.json)

> **Yöntem notu — neden bu önemli.** Önceki projede tasarım kararları
> kullanıcının referanslarından değil, "kurumsal broker estetiği" gibi hayali
> bir hedeften geliyordu ve tek tek şikâyet yamalanıyordu. Bu belge dördünü
> **birlikte** okuyup ortak ilkeyi çıkarıyor. Bundan sonraki her görsel karar
> bu belgeye dayanacak.

---

## 1. Ölçülen token'lar

### Tipografi

| Site | Gövde yüzü | İkinci yüz | Baskın boy | Ağırlıklar |
|---|---|---|---|---|
| LuxAlgo | Aeonik (grotesk) | `ui-monospace` | 16 / 14 / 13 px | **400** (2562), 500 (185) |
| Dovetail | Inter | **JetBrains Mono** + PP Mondwest | 20 / 16 / 14 px | **400** (3268), 600 (385) |
| Slash | Inter | **ivyPresto** (serif display) | 16 / 14 px | **400** (1244), 500 (114) |
| V7 Labs | STK Bureau Sans (grotesk) | **Martina Plantijn** (serif, italik) | 12 / 14 / 13 px | **400** (862), 300 (37) |

### Harf aralığı (tracking)

| Site | Başlık | Küçük etiket |
|---|---|---|
| LuxAlgo | −1.3 / −1.4 / −1.9 px | **+2.2 px** |
| Dovetail | **−2 px** | +1 px |
| Slash | −0.8 / −0.36 / −0.32 px | — |
| V7 Labs | −1.44 / −0.72 / −0.64 px | — |

### Zemin ve yüzey

| Site | Sayfa zemini | Yüzeyler | Ayrım yöntemi |
|---|---|---|---|
| LuxAlgo | `#0a0a0a`, `#000` | `#141414`, `#0b0d10`, `#1a1a1c` | beyaz alfa %7–8 |
| Dovetail | `#0a0a0a` | `#212121`, `#141414` | beyaz alfa %8–24 |
| Slash | `#040406`, `#0b0c0e` | `#18181b`, `#121317`, `#1c1d22` | ince alfa kenarlık |
| V7 Labs | siyah | `#292929`, `#1c1c1c` | beyaz alfa %5–11 |

**Gölge:** LuxAlgo'da yalnızca 11 öğede, Dovetail'de **sıfır**. Yüzeyler
gölgeyle değil, **bir tık açık zemin + saç teli inceliğinde beyaz alfa
kenarlıkla** ayrılıyor.

### Metin renk kademesi — dördünde de aynı üç basamak

| Basamak | LuxAlgo | Dovetail | Slash | V7 |
|---|---|---|---|---|
| Birincil | `#ededed` | `#ffffff` | `#ffffff` | `#ffffff` |
| İkincil | `#a0a0a0` | beyaz %64 | `#9194a1` | beyaz %60–71 |
| Üçüncül | `#7d7d7d` / beyaz %25 | beyaz %48 | `#777a88`, `#5e616e` | beyaz %30 |

### Köşe yarıçapı — ikili sistem

| Site | Panel / kart | Düğme |
|---|---|---|
| LuxAlgo | 0 px (2538 öğe), 8 / 12 px | tam hap (`2.68e7px`) |
| Dovetail | 0 px (3769), 8 px | 8 px |
| Slash | **2 px** (121), 10 px | tam hap (9999px) |
| V7 Labs | 0 px (882), 6 px | tam hap (100–160px) |

### Aksan rengi — tek ve seyrek

LuxAlgo mor/cyan (`#9200ff`, `#2ff3ff`) · Dovetail mavi (`#0044ff`) ·
Slash bakır (`#cc9166`) · V7 mavi (`#0000ee`).
Dördünde de aksan **sayfanın %1'inden azında** kullanılıyor.

---

## 2. Ortak dil — dokuz ilke

Bunlar dört sitenin **hepsinde** doğrulanan, QuaxisLabs'a alınacak ilkeler.

1. **Koyu ve düşük doygunluklu zemin.** Sayfa `#0a0a0a` civarı, yüzeyler bir
   tık açık. Renkli koyu tema (lacivert, koyu mor) yok — nötr siyah-gri.
2. **Ayrım gölgeyle değil, ince alfa ile.** Beyaz %5–11 dolgu, beyaz %8–16
   kenarlık. Gölge katmanı neredeyse hiç kullanılmıyor.
3. **Ağırlık kıtlığı.** Neredeyse her şey **400**. 500/600 yalnızca vurgu için.
   700 yok denecek kadar az. Bu, "kalın yazarak önemli göstermek" alışkanlığının
   tam tersi ve sayfanın sakin görünmesinin ana sebebi.
4. **Üç basamaklı metin hiyerarşisi.** %100 / ~%64 / ~%30. Hiyerarşi **boyutla
   değil opaklıkla** kuruluyor — bu yüzden gövde boyutları 12–16 px dar bir
   bantta kalabiliyor.
5. **Başlıkta negatif tracking, etikette pozitif.** Display −0.8…−2 px;
   eyebrow/section-label +1…+2.2 px ve büyük ihtimalle küçük harf-büyük
   (`uppercase`). Bu zıtlık "profesyonel" hissinin en ucuz kaynağı.
6. **Yarıçapta ikili sistem.** Panel/kart **keskin** (0–2 px), kontrol
   **tam hap**. Ara değer (8–12 px) yalnızca medya/görsel kutularında. Her şeye
   `rounded-lg` vermek bu dilin dışında kalıyor.
7. **Tek aksan, bilinçli kıtlık.** Bir renk, sayfanın %1'inden azında, yalnızca
   "karara değer" öğelerde.
8. **İkinci bir yüz karakter taşır.** Dördünün de nötr gövde yüzünün yanında
   karakterli bir ikinci yüzü var: mono (Dovetail, LuxAlgo) ya da serif
   (Slash, V7 — ikisi de italik display olarak). Tek yüzle kurulan sayfa
   jenerik görünüyor.
9. **Dar boyut ölçeği + geniş boşluk.** Gövde 12/13/14/16; sonra doğrudan
   44–76 px display. Aradaki boşluk **beyaz alanla** dolduruluyor.

---

## 3. QuaxisLabs'a ne alınıyor, ne alınmıyor

### Alınıyor
Yukarıdaki dokuz ilkenin tamamı.

### Alınmıyor — ve neden

**Görsel kimliğin kendisi.** Renk paleti, logo dili, font seçimleri bizim.
Hem hukuken doğru hem gereksiz: `docs/design/` altında kendi üç temamız
(Terminal Koyu / Klasik Beyaz Rapor / Kağıt Rapor) zaten tanımlı ve karakterli.

**Kaydırma animasyonları — kesinlikle hayır.** Dovetail ve Slash'in bölümleri
kaydırmaya bağlı "reveal" animasyonlarıyla açılıyor; bu sitelerin ekran
görüntüsünü almaya çalışırken **bölümler boş çıktı** çünkü içerik henüz
çizilmemişti. Pazarlama sitesinde bu bir efekt; **bir tarama aracında bu bir
kusur.** Kullanıcı tabloyu görmek için kaydırmayı beklemez. Kuralımız: sayfa
ilk boyamada eksiksiz okunur, `prefers-reduced-motion` her zaman saygı görür.

**Pazarlama boy ölçeği.** Bu dördü pazarlama sitesi; gövde boyları 16–20 px.
Bizim ürünümüz yoğun bir tarama aracı — baskın boy **13–14 px** olacak,
V7'nin 12 px'lik yoğunluğu bize en yakın olanı.

### Eklenen — bu dördünde olmayan ama bizde zorunlu

**Sayılar birinci sınıf içeriktir.** Bu dört sitede sayı bir süstür; bizde
sayı **ürünün kendisi**. Bu yüzden:
- Her sayısal değer mono yüzle ve `font-variant-numeric: tabular-nums` ile
  dizilir — kolonlar birbirini tutar.
- Aksan rengi ile **semantik yeşil/kırmızı ayrı token aileleridir**. Aksan
  "karara değer" demek; yeşil/kırmızı **yön** demek. Karıştırılmaz.
- Üçüncül metin kademesi (%30) bizde **sayıya uygulanmaz** — okunabilirlik
  eşiği bir tarama tablosunda pazarlama sayfasındakinden yüksektir.

**Üç tema, tek koyu tema değil.** Dördü de tek koyu temada. Bizde koyu tema
varsayılan, ama rapor/paylaşım için iki açık tema korunur. Dokuz ilke açık
temaya çevrilirken şu eşleşme geçerlidir: "beyaz alfa" → "siyah alfa",
metin kademeleri ters çevrilir, ağırlık kıtlığı ve yarıçap ikiliği **aynen**
kalır.

---

## 4. Sonraki adım

Bu belge **Faz 2'nin girdisidir.** Faz 2'de önce bir Artifact maketi üretilip
onaya sunulacak, sonra `apps/web` token seti ve bileşen kütüphanesi bu dokuz
ilkeye göre kodlanacak. Kod yazılmadan önce maket onaylanmazsa kod yazılmaz.
