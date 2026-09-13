# Görsel kabul döngüsü

**Kural:** README madde 5 — her görsel iş ekran görüntüsüyle doğrulanır,
**en az 3 iterasyon**.

Bu dosya iki turu kaydeder: **Faz 2** (`/tasarim` vitrini, `*-i5.png`) ve
**Faz 3** (beş ürün yüzeyi, `*-f3.png`).

## Nasıl üretilir

```bash
cd apps/web && npm run build:vitrin      # statik dışa aktarım -> apps/web/out

# tek yüzey, üç tema × iki genişlik
python tools/ekran_goruntusu.py --yol tarama.html --ad tarama --etiket f3

# yalnız bir tema
python tools/ekran_goruntusu.py --yol index.html --ad giris --etiket f3 --tema koyu

python tools/tablo_olcum.py              # DataTable kabul ölçümü
python tools/kirp.py <png> x y w h --olcek 2.6 --ad yakin.png   # yakından bak
python tools/gorsel_kucult.py docs/design/ui
```

`tools/ekran_goruntusu.py`, `out/` klasörünü kendi içinde servis eder — ayrıca
bir geliştirme sunucusu açmaya gerek yoktur. Üç tema × iki genişlik = altı kare.
`?tema=koyu|acik|sistem` sorgusu depolanan tercihi ezer; "sistem" karesi
`prefers-color-scheme: light` dayatılarak alınır, böylece sistem temasının
gerçekten sistemi izlediği görülür.

## Depodaki kareler

Ara turlar (i2–i4) silindi; **başlangıç (i1)** ve **son (i5)** durum yan yana
karşılaştırılabilsin diye duruyor.

| Dosya | Tema | Genişlik |
|---|---|---|
| `tasarim-koyu-1440-*.png` | koyu (varsayılan) | 1440 |
| `tasarim-acik-1440-*.png` | açık | 1440 |
| `tasarim-sistem-1440-*.png` | sistem (OS açık) | 1440 |
| …`-768-*.png` | aynı üçü | 768 |

## İterasyonlar — ne görüldü, ne düzeltildi

### i1 → i2
1. **Boş ızgara gözleri düz gri blok olarak boyanıyordu.** "1px boşluk + çizgi
   renkli konteyner zemini" numarası, satır dolmadığında boşluğu çizgi rengiyle
   dolduruyordu; açık temada Bölüm 03'te iki, Bölüm 04'te bir blok. Saç teli
   ayrım konteyner zemininden **çocuk kenarlığına + negatif margine** taşındı
   (`.tiles`, `.cards`, `.specgrid`, `.tokenlar`).
2. **Kart altlıkları hizasızdı.** Künye bir kartta tek, diğerinde iki satır
   olunca "Stratejiyi aç →" farklı yüksekliklerde duruyordu → `.card .foot`
   `margin-top: auto`.
3. **İskelet çubukları farklı parlaklıktaydı** — `background-size` yüzdeydi,
   sabit px'e çevrildi.

### i2 → i3
4. **Üçüncül metin kademesi paragrafta okunmuyordu.** Açık temada %40 siyah,
   12px, üç satır. Tasarım dili üçüncül kademeyi *etiket / birim / zaman
   damgası* için tanımlıyor; açıklayıcı cümleler ikincile alındı.
5. **Vitrin ızgarasının son satırı yarım kalıyordu** — altı kart için sütun
   sayısı 6'yı bölen değerlerde sabitlendi (3 / 2 / 1).

### i3 → i4 — DataTable kabul ölçümü
6. **`End` tuşundan sonra odaklı satır pencerenin dışında kalıyordu.**
   Yapışkan `<thead>` hesaba katılmıyordu; satır konumu ve görünür bölge
   başlık yüksekliği kadar kaydırıldı.
7. **500 satırda kaydırma 34 fps.** Üç adımda çözüldü:
   `contain: layout paint style` (asıl darboğaz — geçersiz kılma tablonun
   dışına taşıyordu), `table-layout: fixed`, hücre elemanlarının satır nesnesine
   göre bir kez üretilip yeniden kullanılması, dinleyicilerin satırlardan
   `<tbody>`'ye devredilmesi.

### i4 → i5
8. **Dört kart 1440'ta sağda boş şerit bırakıyordu** — `auto-fill` boş kolon
   rezerve ediyor; `auto-fit`'e çevrildi, kartlar genişledi.
9. **Künye yüksekliği** iki satıra sabitlendi ki başlıklar kart genişliğinden
   bağımsız hizalansın.

### Doğrulanıp kusur bulunmayanlar
- **Türkçe glifler üç yüzde de tam** (İ ı Ğ ğ Ş ş Ç ç Ö ö Ü ü) — 3× büyütmeyle
  gözle kontrol edildi: Archivo, Inter, JetBrains Mono. Eksik glif yok.
- **Sistem teması gerçekten sistemi izliyor** — `prefers-color-scheme: light`
  dayatıldığında hem sayfa hem kapsamlanmış "sistem" sütunu açığa geçiyor.
- **768'de** üç tema sütunu alt alta yığılıyor, tablo kendi içinde yatay
  kayıyor, hiçbir ızgarada yarım satır kalmıyor.

> Bilinen sınır: JetBrains Mono'da **₺ (U+20BA)** yok — kaynak fontta da yok.
> Mono yüzde lira işareti gerekirse yedek yüze düşer. BIST fiyatları şu an
> işaretsiz gösteriliyor.

## DataTable kabul ölçümü — 500 satır

`python tools/tablo_olcum.py`, 1440×900, başsız Chromium (yazılım boyama).

| Ölçüt | Sonuç |
|---|---|
| Satır sayısı | 500 |
| **DOM'daki satır** | **25** (görünen 13 + taşma payı 12) |
| Dolgu satırı | 1–2 (`tr.pad`, yükseklik taşır) |
| Boş sayfa taban çizgisi | 60 fps · 16.67 ms |
| **Kaydırma (en kötü hâl: 2 sn'de tüm liste ileri-geri)** | **56 fps · ort. 17.85 ms · en kötü kare 33.4 ms** |
| Gerçekçi kaydırma hızında | 60 fps · 16.67 ms |
| Sıralama | artan → azalan → sırasız; `aria-sort` üç durumda doğru |
| Klavye: 40× ↓ | satır 40 |
| Klavye: End | satır 499, **pencere içinde görünür** |
| Klavye: Home | satır 0 |

Ölçüm sentetik bir sayı değil: sayfanın kendi `requestAnimationFrame` kare
aralıkları. "2 sn kaydır ve ölç" düğmesiyle vitrinde de tekrarlanabilir.

---

# Faz 3 — beş ürün yüzeyi (`*-f3.png`)

**Tarih:** 2026-09-12

| Yüzey | Yol | Dosya |
|---|---|---|
| Giriş ekranı | `/` | `giris-*-f3.png` |
| Tarama | `/tarama` | `tarama-*-f3.png` |
| Grafik | `/grafik` | `grafik-*-f3.png` |
| Strateji kütüphanesi | `/stratejiler` | `kutuphane-*-f3.png` |
| Strateji sayfası | `/stratejiler/swing-fib-abcd` | `strateji-*-f3.png` |

Her yüzey için koyu 1440 + açık 1440 + koyu 768 saklandı. Sistem teması Faz
2'de doğrulandı (`tasarim-sistem-*`), tema kapsamlaması değişmedi.

## İterasyonlar — ne görüldü, ne düzeltildi

### f3i1 → f3i2 (on kusur)
1. **Fiyat paneli neredeyse boştu.** Örnek seri sabit bir eksene çiziliyordu;
   rastgele yürüyüş panelin ortasında ince bir şerit olarak kalıyor, levhanın
   yarısı boş duruyordu. Eksen artık seriye OTURUR (min/max + %6 pay).
2. **Hacim şeridi levhanın yarısını yiyordu** — yükseklikten türetilen sabit
   oran (%24).
3. **Son fiyat rozetinin rengi sayfadaki yön rozetiyle çelişiyordu.** Giriş
   ekranı "SAT" diyor, grafikteki rozet yeşil çıkıyordu. Yön artık ÇAĞIRANDAN
   gelir; bir tarama aracında rozetin rengi rastgele bir serinin son barına
   bırakılamaz.
4. **"ChartSpec katmanı · Faz 4" bindirmesi mumları kapatıyordu** → levha
   çubuğuna kesikli hap olarak taşındı.
5. **Durum kutusu son fiyat rozetinin üstüne biniyordu** → sağ konum fiyat
   oluğunun dışına alındı.
6. **Pazarlama başlıklarının satır aralığı gövde metninden miras kalmıştı**
   (1.5) → 1.12.
7. **Yedi kapı 6 + 1 diziliyordu** → sütun eşiği düşürüldü, `auto-fit` boş izi
   topluyor, yedisi tek satırda.
8. **Tarama tablosunun "Tarihsel isabet" kolonu 1440'ta kesiliyordu** — kolon
   genişlikleri toplamı levhadan genişti. K4 çıktısını taşıyan kolonun
   görünmesi için toplam daraltıldı.
9. **Filtre şeridinde "Bugünü tara" tek başına alt satıra düşüyordu** → iki
   eylem tek gruba alındı.
10. **Yön çipleri "Yön: Tümü / Yön: AL / Yön: SAT"** — grup etiketi zaten "YÖN"
    diyordu; çipler sadeleşti.

### f3i2 → f3i3
11. **Durum kutusu ve HUD son barların üstüne biniyordu.** Bir tarama aracında
    en önemli barlar tam da onlar. Levhaya üst ve sağ pay eklendi
    (`padUst` / `padSag`); katmanlar artık boş alanı kaplıyor.
12. **Kaynak kutusunda dosya yolu cümlenin başına düşüyordu** ("…10_pesavento…
    Larry Pesavento — …") → kod, cümlenin doğal yerine alındı.

### f3i3 → f3i4
13. **Makette olan hero arama kutusu atlanmıştı** → geri kondu ve gerçek bir
    davranışa bağlandı (girilen metin taramaya sorgu olarak taşınır). Altındaki
    iki CTA maketteki hâline döndü.

### Doğrulanıp kusur bulunmayanlar
- Sol rayda yalnız bulunulan yüzey vurgulu (2.6× büyütmeyle bakıldı).
- Açık/koyu temada beş yüzeyin tamamı; 768'de ray gizleniyor, tablo kendi
  içinde yatay kayıyor, hiçbir ızgarada yarım satır kalmıyor.
- Duyuru şeridi geri sayımı sunucuda boş, istemcide dönüyor — hidrasyon
  uyuşmazlığı yok.

---

# Faz 4 — ChartSpec v1 + grafik motoru (`*-f4.png`)

**Tarih:** 2026-09-12
**Referans:** [`references/HRhIeAdbcAAL2_B.png`](../../../references/HRhIeAdbcAAL2_B.png)

Levha artık örnek çizim değil, gerçek bir motor: mum/hacim/crosshair/zoom-pan
Lightweight Charts v5'ten, fibo merdiveni ve formasyon çizimleri bizim SVG
overlay'imizden. İkisini besleyen tek kaynak Python komposerinin ürettiği
`ChartSpec` JSON'u.

| Yüzey | Dosya |
|---|---|
| Grafik yüzeyi (tam merdiven) | `grafik-*-f4.png` |
| Giriş ekranı önizlemesi (seyrek merdiven) | `giris-*-f4.png` |
| Strateji sayfası | `strateji-*-f4.png` |

## İterasyonlar — ne görüldü, ne düzeltildi

### f4i1 → f4i2
1. **Durum kutusu grafiğin üstünde yüzüyordu ve formasyonun C köşesini,
   sağ oluktaki fibo etiketlerinin yarısını kapatıyordu.** Makette bu bir
   çizimdi; gerçek grafikte fiyat her yere gidebilir ve yüzen bir kutu er geç
   bir şeyin üstüne düşer. Kutu levhanın **altına**, yatay şeride taşındı.
   Yan kazanç: 820px altında gizlenmek zorunda değil, dar ekranda da okunuyor.
2. **Son fiyat rozeti ile `1.272` etiketi üst üste biniyordu** → sağ oluk için
   dikey çakışma çözücü yazıldı (`yerlesim.ts`): sabit öğe (son fiyat) yerinde
   kalır, etiketler ondan kaçar, kayan etiket çizgisine ince bir bağla bağlanır.
3. **Durum rozeti sağ oluğa taşıyordu** → kutu çizim alanının içine sınırlandı.

### f4i2 → f4i3
4. **`1.618 (azami risk): 146.00` etiketi sağdan kesiliyordu** → oluk 168 →
   **186px** (maketin `PAD.r` değeriyle aynı).
5. **`0.5` / `0.236` biçim tutarsızlığı** → referanstaki gibi `0.500`.
6. **`TAMAMLANDİ`** → veri `tamamlandı` yapıldı, Türkçe büyütme doğru çalıştı.

### f4i3 → f4i4 — en önemli bulgu
7. **Grafik tuvali etiket oluğunun ALTINA taşıyordu.** Sarmala `padding-right`
   vermek yetmiyordu: mutlak konumlu çocuk padding kutusunu değil kenarlık
   kutusunu doldurur. Son barlar ve `D` köşesi oluğun altında kalıp fibo
   etiketleriyle çakışıyordu. Tuvalin sağ kenarı doğrudan oluk kadar içeri
   alındı.

### f4i4 → f4i6
8. **Giriş ekranı önizlemesinde dokuz basamak okunmaz bir yığına dönüyordu**
   (250px levhada 10 etiket). Çizici `seviyeler="vurgulu"` kipi aldı: kısa
   levhalarda yalnız karara değer basamaklar (`0.618`, `0.786`, `1.272`) —
   maketin giriş ekranında yaptığının aynısı.
9. **Bant etiketi ince bantta alt çizginin üstüne biniyordu** → bant 24px'ten
   inceyse etiket bandın üstüne yazılıyor.
10. **Salınım etiketleri (`LH`/`HL`) yatay fibo çizgilerinin üstüne düşünce
    okunmaz oluyordu.** Önce `paint-order: stroke` denendi — **yetmedi**:
    kontur yalnız glif kenarını korur, harflerin *arasından* geçen çizgiyi
    kapatmaz. Metin ölçülüp arkasına gerçek bir zemin dikdörtgeni kondu.

### Doğrulanıp kusur bulunmayanlar
- Açık/koyu tema geçişi: token'lar `MutationObserver` ile yeniden okunuyor,
  mum renkleri ve overlay birlikte dönüyor.
- Sol rayda yalnız bulunulan yüzey vurgulu (2.6× büyütmeyle bakıldı).
- Pivot işaretleri **onay barında** duruyor, kendi barında değil — non-repaint
  sözleşmesinin çizim tarafındaki karşılığı (`test_komposer.py` bunu sabitler).

## Referanstan bilinçli sapma

Referanstaki **kesik-noktalı mavi trend çizgisi** üretilmedi: o çizgi Altın
Bölge stratejisine değil ayrı bir trendline göstergesine ait. Her komposer
yalnız kendi stratejisinin çizimini üretir; aksi hâlde jenerik çiziciye geri
dönülmüş olurdu. `CizgiRol.TREND` rolü sözleşmede hazır bekliyor.

---

# Faz 7.1 · K5 — Golden Zone komposeri (2026-09-13)

Görüntüler: `gz-{koyu,acik,sistem}-{1440,768}-i11.png` (ara turlar: i1–i10).
**11 iterasyon** yapıldı; asgari 3.

Girdi **fikstür değil gerçek veri**: `tools/golden_zone_spec.py` gerçek THYAO
serisini dedektörden geçirip spec üretiyor. Elle kurulmuş bir fikstür
dedektörün gerçekte ne ürettiğini gizleyebilirdi — Faz 4'te tam olarak bu
olmuştu (komposer güzel bir formasyon çiziyordu ama adı yanlıştı).

## Görerek bulunan kusurlar

1. **`süpürme` ile `%100` işaretleri TAM aynı noktaya çiziliyordu** (i1) —
   iki etiket üst üste binip okunmaz bir yığın oluyordu. Kök sebep dedektörde:
   payload süpürmenin kendi barını/fiyatını taşımıyordu, araç da çaresizce
   `%100` çıpasının değerlerini kopyalıyordu. `supurme_bar` ve `supurme_fiyat`
   payload'a eklendi; komposer ayrıca iki çıpa çakışıyorsa süpürmeyi çizmiyor.

2. **"BOS" çizgisi yanlış sayıyı gösteriyordu** (i1) — kırılan salınım
   seviyesi yerine kırılım barının KAPANIŞI. Etiket doğru, sayı yanlıştı;
   bu en sinsi kusur türü. `kirilan_seviye` payload'a eklendi.

3. **Bant ve seviyeler farklı barlardan başlıyordu** (i2) — seviyeler bacağın
   başından, bant bacağın ucundan. İkisi de bacak TAMAMLANINCA doğar;
   `capa0.onay_t`'de birleştirildi.

4. **Sonuçlanmış kurulumun bölgesi levhanın sonuna kadar uzuyordu** (i2) —
   artık geçerli olmayan bir bölgeyi hâlâ varmış gibi gösteriyordu. `Bant` ve
   `Seviye`'ye `bitis` alanı eklendi; araç `barrier_outcome` ile (K4'ün
   kullandığı AYNI mantık) çıkışı hesaplıyor. Seviyeler bitişten sonra **%22
   opaklıkla hayalet** devam eder: tamamen kesilse sağ oluktaki etiket
   sahipsiz kalırdı.

5. **Çıkış işareti hiç görünmüyordu** (i3) — `IsaretRol.TEMAS` rolünde
   `hap: false` olduğu için çizici metni **sessizce düşürüyordu**; geriye
   3 piksellik bir nokta kalıyordu. Hapsız roller de artık yazıyor.

6. **Bant etiketi giriş rozetiyle çakışıyordu** (i3) — "OTE 0.62–0.79" hem
   HUD'da hem sağ olukta zaten yazıyordu. Üçüncü kez yazmak bilgi eklemiyor,
   sadece çakışma üretiyordu; bant etiketsiz bırakıldı.

7. **Çıkış aksan renginde çizilmişti** (i3) — "hedefe ulaştı" ile "stop oldu"
   aynı renge boyanıyordu. Sonuç YÖN bilgisidir: `IsaretRol.CIKIS_KAZANC` /
   `CIKIS_KAYIP` rolleri eklendi (`--up` / `--down`).

8. **En ciddisi — mum tuvali SVG katmanının ÜSTÜNDEYDİ** (i4–i7).
   Lightweight Charts kendi tuvallerine `z-index: 1` ve `2` veriyor;
   `.qgrafik-tuval` bir yığınlama bağlamı KURMADIĞI için o sayılar dışarı
   taşıyor ve mumlar bizim çizimlerimizin üstüne çıkıyordu. Kusur **Faz 4'ten
   beri vardı ama görünmüyordu**: o güne kadar çizilen her şey mumların
   olmadığı boşluklara düşüyordu. Çıkış işareti mumun üstüne düşen ilk şey
   oldu ve "stop ✕ 288.75" metnini mum gövdesi kesti.
   Çözüm: `.qgrafik-tuval { z-index: 0; isolation: isolate }` +
   `.qgrafik-overlay { z-index: 1 }` + `.qgrafik-hud { z-index: 2 }`.
   *Teşhis göz kararıyla yapılmadı:* overlay DOM'u gerçek 1440 viewport'ta
   playwright ile okundu, zemin dikdörtgeninin VAR olduğu ama tuvalin üstte
   olduğu ölçülerek görüldü.

9. **`getBBox()` yerleşim yapılmamış ağaçta 0 dönünce zemin sessizce
   çizilmiyordu** (i4) — metin monospace olduğu için ölçü kestirimi
   (karakter genişliği = punto × 0.6) yedek yol olarak eklendi.

10. **HUD metni 0.0 seviyesinin çizgisiyle kesişiyordu** (i7) — tasarım
    dilinin kendi kuralının ihlali. Satırların arkasına levhanın zemini
    kondu (gölge değil, dolgu).

11. **Zemin `inline-block` ile verilince iki HUD satırı yan yana gelip dar
    levhada sağ oluğa taşıdı** (i8, 768) → `display: block; width: fit-content`.

12. **"hedef" ile sayısı ayrı satıra düşüp sayı sahipsiz kalıyordu** (i10,
    768) → çift `white-space: nowrap` ile bölünmez yapıldı.

### Doğrulanıp kusur bulunmayanlar
- Üç tema × iki genişlik: bant, hayalet uzantı, çıpalar ve çıkış işareti
  hepsinde okunuyor.
- Çıpalar **onay barında** duruyor (non-repaint sözleşmesinin çizim karşılığı).
- Ödül/risk sayfada iki seviyeden TÜRETİLİYOR, elle yazılmıyor.

## Referanstan bilinçli sapma

`references/G8es0m9W4AAiTAK.png` ve `G8j_KYOX0AEb8l-.png` **anlamak için**
verilmişti, kopyalamak için değil — kullanıcının kendi ifadesiyle. Bu yüzden
komposer o görsellerin düzenini taklit etmiyor; K0'daki mekanik kuralı
çiziyor. Referanslardaki çok zaman dilimli paneller ve el yazısı notlar
üretilmedi.

**Merdivenin tamamı çizilmiyor:** bandın kenarları zaten 0.62 ve 0.79;
ayrıca çizgi olarak koymak dar bandın içinde üç çizgi = okunmaz yığın
demekti.

---

# Faz 7 · Arayüz — aralık seçici, PNG indirme, okunabilirlik (2026-09-13)

Görüntüler: `ui-{koyu,acik,sistem}-{1440,768}-i4.png`. **4 iterasyon.**

Üç eksik birlikte ele alındı çünkü üçü de aynı soruna bakıyordu: levha
neyi, ne kadarını ve nasıl gösteriyor.

## 1. Görünür aralık seçici

`Kurulum · 1A · 3A · 6A · 1Y`. **Varsayılan `Kurulum`** (spec'in tamamını
sığdır), sabit takvim aralığı değil.

Sebep: bir spec yalnız kurulumun etrafındaki barları taşır (Golden Zone'da
~100 bar). O levhada "son 1 yıl" demek çoğu zaman "hepsi" demektir. Önce
kurulum çerçevelenir; kullanıcı isterse daraltır.

**Mum okunabilirliği sorununu çözen şey bu oldu.** `1A` seçilince ~28 bar
kalıyor ve mumlar fibo çizgileri arasında kaybolmuyor. Y ekseni merdivene
göre açıldığı için dikeyde sıkışma sürüyor; yatayda daralmak yeterli geldi.

İstenen pencere serinin başından geriye taşıyorsa **tamamı gösterilir**:
olmayan barlara doğru boş alan açmak levhayı yalancı yapardı.

Aralık değişince grafik **yeniden kurulmaz**, yalnız görünür pencere
güncellenir — yeniden kurmak zoom/pan durumunu ve tüm aboneleri çöpe atardı.

## 2. PNG indirme

Levha iki katmandan oluşuyor: mumlar bir `<canvas>`'ta (Lightweight Charts),
seviyeler ve rozetler bizim SVG'mizde. **Tek başına hiçbiri grafiğin
tamamı değil.** `pngIndir` ikisini tek tuvalde birleştiriyor; sıra ekrandaki
yığınlama sırasıyla aynı (zemin → tuval → SVG).

SVG'yi resme çevirmek onun **kendi kendine yeter** olmasını gerektiriyor.
Overlay zaten token'ları gerçek renk değerlerine çözüp yazdığı için
(`roller.ts::tokenRengi`) bu çalışıyor — CSS değişkeni yazsaydı indirilen
görüntü renksiz çıkardı.

Dosya adı: `thyao-golden-zone-1d-2026-09-13.png`.

## Görerek bulunan kusurlar

1. **Araç şeridi sağ oluktaki fiyat etiketlerini kapatıyordu** (i1) —
   `0.0 (hedef): 335.00` düğmelerin altında kayboluyordu. Şerit levhanın
   İÇİNDEN çıkarılıp ÜSTÜNE alındı. Yan fayda: PNG'ye de girmiyor,
   indirilen görüntüde arayüz düğmesi işi yok.

2. **İndirilen PNG neyin grafiği olduğunu söylemiyordu** (i2) — ekrandaki
   künye bir HTML katmanı (HUD), ne tuvale ne SVG'ye giriyor. Künye
   tuvale ayrıca yazıldı. **Verdikt de yazılıyor ve bu zorunluluk:**
   verdikti taşımayan bir grafik paylaşıldığında "kanıtlandı" ima eder.

3. **Künye levhanın İÇİNE yazılınca yine fiyat etiketiyle çakıştı** (i3) —
   ekrandaki şeritte yaşanan sorunun birebir aynısı. Künye levhanın
   ÜSTÜNE 26px'lik kendi bandına alındı, altına ince ayraç kondu.

4. **Görünür alan dışındaki rozet kenara sıkışıyordu** (i2, `1A`
   aralığında) — çapası ekran dışında kalan "giriş 306.32" rozeti sol
   kenarda kırpık duruyordu. Kenara sıkıştırmak onu ait olmadığı bir bara
   bağlarmış gibi gösterirdi; çapası görünür alanın dışındaysa rozet
   artık **çizilmiyor**.

### Doğrulanıp kusur bulunmayanlar
- Üç tema × iki genişlik: şerit 768'de de taşmıyor.
- Etkin aralık **aksanla değil opaklıkla** ayrılıyor — aksan bu levhada
  0.618 seviyesinin ve OTE bandının rengi, bir düğmeye harcanmaz.
- Klavye: düğmeler gerçek `<button>`, `aria-pressed` taşıyor, odak halkası
  aksanlı.

### Görsel değil İŞLEVSEL doğrulama da yapıldı

Ekran görüntüsü tıklamayı göstermez. Playwright ile her aralık düğmesine
tıklanıp levha yeniden çekildi ve PNG indirme **gerçekten dosya üretiyor
mu** diye indirme olayı yakalandı (`thyao-golden-zone-1d-2026-09-13.png`,
53 KB). Bir düğmenin "var olması" çalıştığı anlamına gelmez.

---

## Harmonik komposer — K5 görsel kabul (2026-09-14)

Dört Pesavento formasyonu, **gerçek BIST verisinden** üretilmiş specler:
`rtalb-abcd` · `dogub-gartley` · `srvgy-kelebek` · `burva-uc_surus`.

Örnekleri seçen ölçüt **getiri değil okunaklılık** (`tools/harmonik_spec.py`
içindeki `_okunaklilik`). Sonuç kendiliğinden karışık çıktı: biri hedefe
ulaştı, ikisi stop oldu, biri süre doldurdu. Kârlı örnek seçmek verdikti
gizlemenin görsel hâli olurdu.

Ekran görüntüleri: `harmonik-<formasyon>-koyu-1440-son.png` ve `-768-`.
Her formasyon `?f=harmonik-<ad>` bağlantısıyla ayrı ayrı yakalandı.

### İterasyon kaydı — ne görüldü, ne düzeltildi

| Tur | Görülen kusur | Düzeltme |
|---|---|---|
| i1 | Köşe etiketlerinden yalnız `X` okunuyordu | DOM ölçümü: hepsi VARDI, üst üste biniyordu. `B` ile `C` aynı barda, `D` ile "GİRİŞ" 5px arayla, `0.618` tam `B`'nin üstünde |
| i1 | Oran etiketi yanlış bacakta | `ab` oranı (A−B)/(A−X) hesaplanır ama **A→B bacağını** anlatır; etiket X→A'ya konuyordu. `_ORAN_BACAK` düzeltildi |
| i1 | Formasyon levhanın %55'ine sıkışıyordu | Pencere çıkış barına göre daraltıldı; `i + pencere` terimi kaldırıldı |
| i2 | `D`'ye hem köşe rozeti hem "GİRİŞ" teması | Giriş fiyatı zaten sağ olukta yazılı; temas işareti kaldırıldı |
| i2 | Durum rozeti `D`'nin üstünde, formasyon adını TEKRAR ediyordu | Ad künyede ve HUD'da zaten var; rozet çıkış barına taşındı |
| i2 | Oran etiketleri hiç çizilmiyordu | **Sessiz kaybolma:** etiket iki barın epoch ORTALAMASINA konuyordu ve o an çoğu zaman hiçbir barın zamanı değil (hafta sonu). Çizici böyle bir zamanı çeviremeyince katmanı sessizce atıyordu. Ortası artık bar İNDEKSİNDEN alınıyor |
| i2 | Kısa bacakta oran etiketi köşe rozetinin üstüne oturuyordu | `ASGARI_BACAK_BAR = 4`: kısa bacağın "ortası" yoktur, oran payload'da kalır |
| i3 | 768'de çıkış rozeti `B` köşesini tamamen kapatıyordu | Rozet çapasının SOLUNA oturur; çıkış sağda olduğu için kutu formasyonun üstüne düşüyordu. İşaretin kendi metni (kompakt, zeminli) kullanıldı |
| i3 | "DÖNÜŞ BÖLGESİ" etiketi bandın dışına taşıyordu | Çizici artık bant DARSA etiketi yazmıyor |
| i4 | Aynı etiket `D` köşe rozetinin İÇİNDEN geçiyordu | `D` rozeti artık **riskin olduğu tarafa** konmuyor: boğada üste, ayıda alta |
| i5 | Strateji değişince formasyon levhanın solunda, EKSİ koordinatlarda kalıyordu | `fitContent()` `barSpacing: 6` sabitini aşamıyor; 174 barlık Kelebek spec'i maskeyi kaldırdı. `setVisibleLogicalRange` ile değiştirildi |
| i6–i7 | `?f=` derin bağlantısı sayfaya ulaşmıyordu | `useSyncExternalStore` hidrasyonda sunucu anlık görüntüsünü kullanır ve mağaza haber vermezse istemci değerini HİÇ okumaz. Abone artık bir kez bildiriyor |
| i12 | Three Drives'ın `O` köşesi HUD metninin içine düşüyordu | HUD bir HTML katmanı, SVG onu göremez. Çizici sol üst köşeyi dışlama bölgesi sayıyor; ayrıca spec penceresi 22 bar sol pay bırakıyor |

### Ölçek hatası — ÇÖZÜLDÜ (i13)

**Belirti:** fiyat aralığının UCUNDAKİ köşe, mumlarından ~43 piksel uzağa
düşüyordu (Kelebek'te `A`, serinin en yüksek fiyatı). Ortadaki köşeler
doğru görünüyordu, çünkü iki ölçek arasındaki fark DOĞRUSAL: ortada
neredeyse sıfır, uçta en büyük.

**Nasıl bulundu.** Gözle değil. Önce `autoscaleInfoProvider` açık/kapalı
iki ekran görüntüsü alınıp piksel taramasıyla karşılaştırıldı; sonra
kesin ölçüm için spec'e **kalibrasyon çizgileri** enjekte edildi — mum
verisinin tam en yüksek ve en düşük değerine oturan iki `Seviye`. Sonuç:

| | |
|---|---|
| Overlay, `0.0719`'u (serinin en yükseği) | y = **342** |
| Mumlar aynı fiyatı | y ≈ **390** |

Yani overlay ile çizici AYRI aralıklar kullanıyordu.

**Sebep.** `autoscaleInfoProvider` ile fiyat ölçeği ChartSpec'in panel
aralığına göre genişletiliyordu (mum aralığının dışında kalan stop/hedef
çizgileri sığsın diye). Sağlayıcı devredeyken mumlar genişletilmiş
aralıkla çiziliyor ama `priceToCoordinate` mum verisinin kendi aralığını
kullanmaya devam ediyor.

**Denenip GERİ ALINAN iki çözüm:**

1. Görünmez bir çıpa serisiyle ölçeği genişletmek — hiç etki etmedi
   (piksel ölçümü sağlayıcılı hâlle birebir aynı çıktı).
2. Overlay'in y'sini elle hesaplamak — Kelebek'i düzeltirken AB=CD'de
   işareti levhanın tamamen DIŞINA çıkardı.

Kütüphanenin ölçek anlamını tahmin ederek yazılan düzeltme, düzelttiğinden
fazlasını bozdu.

**Uygulanan çözüm: sağlayıcı kaldırıldı.** Levha artık mumların kendi
aralığına ölçekleniyor; overlay ile çizici aynı aralığı kullanıyor.
Ölçülen fark **43 piksel → 2 piksel**.

Takas açık ve bilinçli: aralık dışında kalan bir seviye artık levhanın
kenarına **sabitleniyor**, daha soluk ve seyrek kesikli çiziliyor,
etiketine yönünü gösteren bir ok (`↑` / `↓`) ekleniyor. **Köşeleri
mumlarına oturmayan bir formasyon, kenara sabitlenmiş bir çizgiden daha
kötüdür:** birincisi yanlış bilgi verir, ikincisi eksik bilgiyi açıkça
söyler.

Pratikte sabitleme nadir: `scaleMargins` zaten mumların altında/üstünde
pay bırakıyor ve Kelebek'in stop'u (mum aralığının altında) o payın içine
sığdı.

**Bu kusur Golden Zone ve Salınım Fibo ABCD grafiklerinde DE vardı**;
oradaki köşeler fiyat aralığının ucunda olmadığı için görünmüyordu.

### Doğrulama

| formasyon | köşe kümesi (piksel sayımı) | beklenen |
|---|---|---|
| `abcd` | 4 | ≥4 (A·B·C·D) |
| `gartley` | 5 | ≥5 (X·A·B·C·D) |
| `kelebek` | 10 | ≥5 |
| `uc_surus` | 7 | ≥6 (O·S1·A·S2·C·D) |

Kelebek'te `A` köşesi ile mumunun tepesi arasındaki fark: **2 piksel.**

### Veri kusuru — Three Drives örneği neden mum grafiği gibi görünmüyordu

Kullanıcı sordu ve ölçüldü: örnek (BURVA **2011**) 106 barın **106'sında**
`açılış == kapanış` taşıyor. Gövdesi olmayan mum çizgi gibi görünür.

Sebep çizici değil **veri**: kaynak BIST için 2014 öncesinde gerçek açılış
fiyatı vermiyor, `open` alanını `close` ile dolduruyor. THYAO'da
`açılış == kapanış` oranı 2011'de %99, 2012'de %99, 2013'te %66; 2015
sonrasında %2–5.

Vitrin örnekleri artık **2014 sonrasından** seçiliyor (`EN_ERKEN`). Yeni
Three Drives örneğinde (EMKEL 2026) doji oranı %5.

**Ölçüme dokunan tarafı ayrıca kontrol edildi:** KURAL-30 teyit kuralı
`close > open` şartı arıyor ve bozuk dönemde bu neredeyse hiç sağlanamaz.
Ama K4'ün verdikti OOS penceresine dayanıyor ve **507 sembolün OOS
pencereleri en erken 2020-08-31'de başlıyor** — hiçbiri bozuk döneme
değmiyor. Verdikt etkilenmedi; etkilenen IS penceresi, yani zaten
güvenilmez bulunan +0.582R.

### Doğrulanıp kusur bulunmayanlar

- Dört formasyonun dördü de köşelerini (X/A/B/C/D, O/S1/A/S2/C) çiziyor;
  piksel sayımıyla doğrulandı.
- Son bacak (→D) **kesik çizgi**: D gerçekleşmiş bir salınım ucu değil,
  hesaplanmış bir hedef. Bu ayrım grafiğin taşıdığı en önemli bilgi.
- Sağ olukta üç seviye (hedef · giriş · stop) ve ödül/risk; hepsi spec'in
  kendi etiketlerinden üretiliyor, elle yazılan sayı yok.
- Verdikt künyede: **"tarihsel isabet · kanıtlanmadı"** beş stratejinin
  beşinde de görünüyor.
