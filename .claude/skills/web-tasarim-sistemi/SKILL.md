---
name: web-tasarim-sistemi
description: QuaxisLabs arayüz tasarım sistemi — token'lar, dokuz ilke, bileşen envanteri, yoğun veri tablosu kuralları, erişilebilirlik eşikleri ve ZORUNLU görsel kabul döngüsü. apps/web altında herhangi bir bileşene, sayfaya ya da CSS'e dokunmadan önce oku.
---

# Web tasarım sistemi

Şartname: [`docs/design/TASARIM_DILI.md`](../../../docs/design/TASARIM_DILI.md) ·
Onaylanmış maket: [`docs/design/maket_v1.html`](../../../docs/design/maket_v1.html) ·
Görsel kabul kaydı: [`docs/design/ui/README.md`](../../../docs/design/ui/README.md)

Tasarım dili **ölçümden** çıkarıldı: dovetail · slash · v7labs · luxalgo
1440×900'de gezildi ve ilk 4000 öğenin `getComputedStyle` değerleri toplandı.
Tahmin değil, veri.

## Dokuz ilke — dördünde de doğrulandı

1. Koyu ve düşük doygunluklu zemin; yüzeyler bir tık açık.
2. **Ayrım gölgeyle değil ince alfa ile.** Gölge yok.
3. **Ağırlık kıtlığı.** 400 varsayılan, 500 yalnız vurgu, **700 yok**.
4. **Hiyerarşi boyutla değil OPAKLIKLA**: %100 / %62 / %34.
5. Başlıkta negatif tracking, etikette pozitif.
6. **Yarıçapta ikili sistem**: panel/kart 2px, kontrol tam hap. Ara değer yok.
7. Tek aksan, sayfanın %1'inden azında.
8. İkinci bir yüz karakter taşır (mono).
9. Dar boyut ölçeği + geniş boşluk.

## Bize özgü — bu dördünde olmayan

- **Sayılar birinci sınıf içeriktir.** Her sayısal değer mono +
  `font-variant-numeric: tabular-nums`.
- **Aksan ile yön renkleri ayrı token aileleridir.** Aksan "karara değer"
  demek; yeşil/kırmızı **yön** demek. Karıştırılmaz.
- **Üçüncül kademe (%34) sayıya uygulanmaz** — tarama tablosunda okunabilirlik
  eşiği pazarlama sayfasındakinden yüksektir.
- **Tablo birinci sınıf bileşendir.** Referans sitelerin hiçbirinde `<table>`
  yok; onlar pazarlama sitesi, biz tarama aracıyız.

## Token'lar

`apps/web/app/tokens.css` — maketten **birebir**. Üç durum korunur: bare
`:root` (koyu, varsayılan), `@media (prefers-color-scheme: light)` içinde
`:root:not([data-theme="dark"])`, ve `:root[data-theme="light"]`. Her seçicinin
`:root` olmayan bir eşi var ki temalar **kapsamlanabilsin** (vitrinde üçü yan
yana çizilir).

**Hardcoded renk YASAK.** Her renk token'dan gelir. Rol → token eşlemesi tek
yerde; grafik tarafında `components/grafik/roller.ts`.

Aksan turkuaz `#2ED3C0`. Yükseliş yeşili bilerek yaprak yeşiline kaydırıldı
(`#6CBF4F`, ~100°) — aksanla arası 27°'den **73°**'ye çıktı. Aksanı
değiştirirsen bu mesafe **yeniden ölçülmeli**, gözle onaylanmaz.

## Bileşen envanteri

`apps/web/components/ui/` — 15 bileşen: Eyebrow · Pill · Chip · ChipGroup ·
Button · Card · Panel · StatTile · DataTable · Sparkline · EmptyState ·
Skeleton · ThemeSegment · Seg/Tabs · Faq. Hepsi `/tasarim` vitrininde üç temada
yan yana.

Yeni bir bileşen yazmadan önce vitrine bak: muhtemelen zaten var.

## DataTable — yoğun veri kuralları

Ölçülmüş davranış (`docs/design/ui/README.md`):

- Satır yüksekliği **sabit**; sanallaştırma buna dayanır. 500 satırda DOM'da
  25 satır durur.
- `contain: layout paint style` **zorunlu** — onsuz geçersiz kılma tablonun
  dışına taşıyor ve kare süresi 38 ms'e çıkıyordu.
- `table-layout: fixed` + `<colgroup>`; kolon genişlikleri toplamı levhayı
  aşmamalı (aşarsa K4 çıktısını taşıyan kolon kesiliyor).
- Hücre elemanları satır nesnesine göre **bir kez** üretilir.
- Klavye: ↑ ↓ Home End PageUp PageDown + Enter. Odak pencere dışına çıkarsa
  liste kendini kaydırır.

## Izgara tuzağı

"1px boşluk + çizgi renkli konteyner zemini" numarası, satır dolmadığında boş
gözleri **düz gri blok** olarak boyar. Saç teli ayrım konteyner zemininden
**çocuk kenarlığına + negatif margine** taşınır. `auto-fill` değil
**`auto-fit`**: auto-fill boş kolon rezerve eder.

## Hareket

Kaydırma tetikli açılış animasyonu **YASAK** — sayfa ilk boyamada eksiksiz
okunur. Bir tarama aracında kullanıcı tabloyu görmek için kaydırmayı beklemez.
`prefers-reduced-motion` her zaman saygı görür.

## Erişilebilirlik eşikleri

- Açıklayıcı paragraf **asla** üçüncül kademede olmaz (açık temada %40 siyah,
  12px, üç satır → okunmuyor). Üçüncül kademe etiket/birim/zaman damgası için.
- Odak halkası: `outline: 2px solid var(--accent)`, offset 2px.
- Renk tek başına anlam taşımaz: yön için şekil ve opaklık da ayırır.
- Sıralanabilir kolon `aria-sort` taşır; segment kontrolleri `aria-pressed`,
  gerçek sekmeler `role="tab"` + ok tuşu gezinmesi.

## ZORUNLU görsel kabul döngüsü

Bir şey çizdiysen **bakmadan bitirme.**

```bash
cd apps/web && npm run build:vitrin
python tools/ekran_goruntusu.py --yol tarama.html --ad tarama --etiket i1
python tools/kirp.py <png> x y w h --olcek 2.6 --ad yakin.png   # yakından bak
python tools/gorsel_kucult.py docs/design/ui                    # depoya girmeden
```

Ekran görüntüsünü **Read ile aç ve gör**, kusurları madde madde yaz, düzelt,
tekrarla — **en az 3 iterasyon**. Bulguları `docs/design/ui/README.md`'ye
yaz: "düzeltildi" demek yetmez, neyin nasıl göründüğü yazılır.

Bu döngü olmasaydı bulunamayacak gerçek kusurlara örnek: mutlak konumlu tuval
padding kutusunu değil kenarlık kutusunu doldurduğu için grafiğin son barları
etiket oluğunun altında kalıyordu; `paint-order: stroke` halosu harflerin
arasından geçen çizgiyi kapatmıyordu.

## Doğrulama

```bash
cd apps/web && npm run build && npx eslint
```

İkisi de temiz olmadan iş bitmiş sayılmaz.
