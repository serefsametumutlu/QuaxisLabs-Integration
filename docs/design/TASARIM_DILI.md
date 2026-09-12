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

---

## 5. Aksan kararı — turkuaz (2026-09-12)

**Karar: aksan turkuaz `#2ED3C0`** (açık temada `#0E8C81`), logodan alınmış.
Kullanıcı üç seçeneği maket üzerinde canlı karşılaştırdı ve turkuazı seçti.

### Çözülen gerçek sorun

İlk maket turunda somut bir çakışma vardı: turkuaz (~173°) ile yükseliş yeşili
(`#3DBE74`, ~146°) arasında yalnızca **27° ton farkı** kalıyordu. Bir tarama
aracında bu, marka renginin **yön anlamıyla** karışması demek — ve kullanıcının
kendi eski şartnamesinin "aksan ile semantik yeşil/kırmızı ayrı token aileleri
olmalı" kuralının doğrudan ihlali. (Not: TradingView'in kendi varsayılan
yükseliş rengi `#26A69A`, yani fiilen turkuazdır — çakışmanın tesadüf olmadığının
kanıtı.)

Aksanı bozmak yerine **çevresi** ona göre yeniden kuruldu:

| # | Değişiklik | Gerekçe |
|---|---|---|
| 1 | Yükseliş yeşili yaprak yeşiline kaydırıldı: `#6CBF4F` (~100°), açık temada `#3D8B2A` | Aksanla arası 27° → **73°**. Mumda ve rozette karışması mümkün değil. |
| 2 | `0.618` fibo seviyesi **aksanın kendisi** oldu | Altın oran zaten "karara değer" seviye. Eskiden orada duran ayrı bir teal, aksanla yarışıyordu. Çakışma anlama çevrildi. |
| 3 | `0.786` saf maviye kaydırıldı (`#5B8CFF` / `#2E5BD4`) | 0.618 aksan olunca altın bölgenin iki ucu net ayrılsın. |
| 4 | Nötrler turkuaza doğru hafifçe yanlandı (`#080B0C`, `#0F1315`, `#161B1E`) | Saf gri "seçilmemiş", hafif yanlı gri "seçilmiş" görünür. |

### Renkten bağımsız ikinci ayrım katmanı

Renk tek başına yeterli değil (renk körlüğü, düşük kaliteli ekran, küçük ölçek).
Bu yüzden **şekil ve opaklık** de ayırıyor:

- **Aksan hiçbir zaman mum ölçeğinde dolu bir leke değildir** — formasyon gövdesi
  %10 opaklıkta geniş dolgu, seviyeler 1px çizgi, rozetler hap formu.
- **Yön renkleri her zaman dolu ve mum boyutundadır.**

Bu kural bağlayıcıdır: yeni bir komposer aksanı mum büyüklüğünde dolu bir
işaret olarak kullanamaz.

### Aksan değişirse

Kehribar ya da elektrik mavisine dönülürse **fibo paleti yeniden ölçülmelidir** —
maket bunu zaten yapıyor (mavi seçilince `0.786`, kehribar seçilince `0.500`
kaydırılıyor). Aksan ile yükseliş arasındaki ton farkı her değişiklikte
**yeniden ölçülmeli**, gözle onaylanmamalı.

---

## 6. Derin geçiş — sayfa yapıları (2026-09-12, ikinci tur)

İlk turda yalnızca hero'lar görülebilmişti; derin bölümlerin ekran görüntüsü
kaydırma animasyonları yüzünden boş çıkıyordu. İkinci turda animasyon süreleri
enjekte edilen CSS ile sıfırlandı ve **sayfa yapıları DOM'dan** çıkarıldı
(başlık akışı + y konumu + toplam yükseklik). Ekran görüntüsünden daha
güvenilir ve tasarım kararı için zaten gereken bilgi bu.

### Sayfa uzunlukları — ve ne anlama geliyorlar

| Site | Toplam yükseklik | Başlık sayısı | Karakter |
|---|---:|---:|---|
| Dovetail | **17 443 px** | 16 | H1 y=330, sonraki başlık y=**9635** |
| Slash | 12 142 px | 30 | düzenli ritim, ~600–900 px'de bir H2 |
| LuxAlgo (gösterge sayfası) | 5 057 px | 24 | yoğun, işlevsel |
| V7 Labs | **4 979 px** | 5 | en kısa, en disiplinli |

**Dovetail'deki 9 300 px'lik başlıksız boşluk** bir hata değil: sabitlenmiş
(pinned) kaydırmayla ilerleyen sinematik bir ürün anlatımı. Sayfanın yarısından
fazlası tek bir animasyona ayrılmış. Etkileyici bir pazarlama tekniği ama
**bizde karşılığı yok ve olmamalı** — bir tarama aracında kullanıcı veriye
gitmek ister, gösteriye değil.

### Başlık formülü — dördünde de aynı kalıp

İki kısa cümle, nokta ile ayrılmış, ikincisi birinciyi keskinleştiriyor:

- V7: *"Complex workflows. Zero room for error."* · *"Build once. Deploy across teams. Improve over time."*
- Dovetail: *"Build with facts, not vibes"*
- LuxAlgo: *"Trading shouldn't be a guessing game."*

Bizim `"Sinyali de gösteririz, isabetini de."` cümlesi aynı kalıpta — tesadüf
değil, bu kalıp bilinçli seçildi.

### Olgu şeridi — Slash'te de var, doğrulandı

Slash `$35bn+ / 5m+ / 10k+ / $100m+` diye dört büyük sayıyı yan yana koyuyor
(y=4729). Bizim giriş ekranındaki `648 / 4S+1G / 7 / 586` şeridi aynı desen —
farkımız sayıların **ölçülmüş ve doğrulanabilir** olması.

### Tablo kullanımı — sıfır

Slash'te ve V7'de **hiç `<table>` yok**; fiyatlandırma bile kart ızgarası.
Bu bizim için bir uyarı değil bir ayrım: onlar pazarlama sitesi, biz tarama
aracıyız. **Bizde tablo birinci sınıf bir bileşendir** ve öyle kalacak.

---

## 7. Strateji sayfası iskeleti — LuxAlgo gösterge sayfasından

En değerli bulgu bu. `luxalgo.com/library/indicator/<ad>/` sayfasının tam
yapısı (y konumlarıyla):

| y | Öğe |
|---:|---|
| 180 | `H1` — gösterge adı |
| 298 | Sekme: **Chart · Source code** |
| 300–1000 | Büyük **canlı grafik** |
| 1025 | CTA — *"Open on Quant Charts · Add this indicator to a live chart in one click"* |
| 1217 | Açıklayıcı görsel |
| 1400 | `H3` — **"How to Trade the X?"** |
| 1780 | `H3` — **"X Settings"** |
| 1824 / 2064 / 2228 | `H4` parametre **grupları** — her grubun altında düz dille yazılmış madde listesi (*"Wick tolerance (ticks): Sets the maximum allowed distance, in ticks, between the candle body and its high or low"*) |
| 2428 | `H3` — **Sık Sorulan Sorular** (akordeon) |
| 2699 | "Back to top" |
| 3675+ | Footer, 6 kolon grubu |

### Bizim uyarlamamız — ve eklediğimiz bölüm

```
Başlık + paket rozeti + istatistik rozeti
Sekme:  Grafik · Kaynak · Parametreler · Ölçüm
────────────────────────────────────────────
Canlı grafik (ChartSpec ile)
"Nereye bak / Ne ölçer / Sinyal ne zaman doğar / Değerler ne demek"
Parametreler — gruplu, her biri düz Türkçe açıklamalı
KAYNAK — hangi kitap, hangi sayfa, hangi eşik alıntılandı   ← K0 kapısının çıktısı
ÖLÇÜM  — tam evrende aday sayısı (K3) + sembol-kümelenmiş
          OOS testi, p değeri, FDR sonucu (K4)               ← ONLARDA YOK
Sık sorulan sorular
```

İki bölüm bizi ayırıyor: **Kaynak** ("bu eşik nereden geldi?") ve **Ölçüm**
("işe yarıyor mu?"). LuxAlgo 874 gösterge yayınlıyor ve hiçbirinin ileriye
dönük getirisini göstermiyor. Strateji Pasaportu'nun K0 ve K4 kapıları bu
sayfada doğrudan görünür hâle geliyor — süreç, ürünün yüzeyine çıkıyor.
