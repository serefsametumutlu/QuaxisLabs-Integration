# Görsel kabul döngüsü — `/tasarim` vitrini (Faz 2)

**Tarih:** 2026-09-12
**Kural:** README madde 5 — her görsel iş ekran görüntüsüyle doğrulanır,
**en az 3 iterasyon**.

## Nasıl üretilir

```bash
cd apps/web && npm run build:vitrin      # statik dışa aktarım -> apps/web/out
python tools/ekran_goruntusu.py --etiket i5
python tools/tablo_olcum.py              # DataTable kabul ölçümü
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
