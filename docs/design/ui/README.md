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
| Strateji sayfası | `/stratejiler/altin-bolge` | `strateji-*-f3.png` |

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
