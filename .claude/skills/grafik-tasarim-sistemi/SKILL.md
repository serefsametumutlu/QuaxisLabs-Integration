---
name: grafik-tasarim-sistemi
description: QuaxisLabs grafik/çizim tasarım sistemi — ChartSpec rol tablosu, aksan ve yön renklerinin ayrımı, etiket yerleşimi, katman sırası ve ZORUNLU görsel doğrulama döngüsü. Komposer yazarken, SVG overlay'e dokunurken ya da herhangi bir grafik çıktısında kullan.
---

# Grafik tasarım sistemi

Şartname: [`docs/design/TASARIM_DILI.md`](../../../docs/design/TASARIM_DILI.md) §5, §7 ·
Sözleşme: [`packages/chart/README.md`](../../../packages/chart/README.md) ·
Kabul kaydı: [`docs/design/ui/README.md`](../../../docs/design/ui/README.md)

## Akış

```
gösterge → TİPLİ SONUÇ → KOMPOSER → ChartSpec (JSON) → çizici
                         (Python)                       (TS)
```

**Jenerik çizici yok.** Her strateji kendi komposerini alır ve komposer o
stratejinin **referans görselini üretmek üzere bestelenir**. Eski depoda tek
bir 10 475 satırlık çizici 24 stratejiyi aynı primitif torbasıyla basıyordu;
referans görsellerin hiçbiri jenerik bir çizicinin çıktısı değildi.

## Komposer kuralları

- **Renk yok, piksel yok.** Yalnız **rol** ve **değer**. Nasıl görüneceği
  çizicinin işi.
- **Rol kapalı kümededir** (`quaxis/chart/roller.py`). Yeni rol önce oraya,
  sonra `apps/web/components/grafik/roller.ts`'e eklenir. İkisi ayrı düşerse
  `test_ciziciyle_uyum.py` yakalar.
- **Pivotlar ONAY barında çizilir**, kendi barında değil. Non-repaint
  sözleşmesinin çizim tarafındaki karşılığı budur.
- **Eksik sonuçtan grafik uydurulmaz.** Gösterge bir pivot üretmediyse
  komposer onu çizmez, `ValueError` atar.
- **Panel y aralığı** seriden gelir; merdiven seriden taşıyorsa komposer aralığı
  **gerekçesiyle** genişletir ve aralık seriyi **kırpamaz**.

## Aksan ve yön — bağlayıcı ayrım

> **Aksan ASLA mum ölçeğinde dolu bir leke değildir.** Formasyon gövdesi %10
> opaklıkta geniş dolgu, seviyeler 1px çizgi, rozetler hap formu.
> **Yön renkleri her zaman dolu ve mum boyutundadır.**

Bu kural renk körlüğü ve küçük ölçek için ikinci bir ayrım katmanıdır: renk tek
başına yetmez, **şekil ve opaklık** da ayırır.

`0.618` fibo seviyesi **bilinçli olarak aksanın kendisidir** — altın oran zaten
"karara değer" seviye. Çakışma anlama çevrildi.

## Katman sırası

Geniş dolgular altta, ince çizgiler ve metinler üstte:

```
bant → alan → seviye → çizgi → işaret → etiket → rozet → son fiyat
```

Aksan hiçbir zaman en üstteki dolu leke değildir.

## Etiket yerleşimi — en çok hata çıkan yer

1. **Sağ oluk genişliği** en uzun etikete göre (`1.618 (azami risk): 146.00`
   → 186px). Dar tutulursa sağdan kesilir.
2. **Dikey çakışma çözülür** (`components/grafik/yerlesim.ts`): son fiyat
   rozeti **sabit**, fibo etiketleri ondan kaçar, kayan etiket çizgisine ince
   bir bağla bağlanır.
3. **Levhanın üstüne düşen metnin arkasına zemin konur.** `paint-order: stroke`
   **yetmez** — kontur yalnız glif kenarını korur, harflerin *arasından* geçen
   çizgiyi kapatmaz. Metin ölçülüp arkasına gerçek bir dikdörtgen konur.
4. **Yüzen kutu er geç bir şeyin üstüne düşer.** Durum kutusu levhanın üstünde
   yüzerken formasyonun C köşesini ve fibo etiketlerinin yarısını kapatıyordu;
   levhanın **altına** yatay şeride taşındı.
5. **Kısa levhada merdivenin tamamı okunmaz bir yığına döner.** `seviyeler`
   kipi `"vurgulu"` ise yalnız karara değer basamaklar (`0.618` · `0.786` ·
   `1.272`) çizilir.
6. **Tuval, etiket oluğunun altına taşmamalı.** Sarmala `padding-right` vermek
   yetmez: mutlak konumlu çocuk padding kutusunu değil **kenarlık kutusunu**
   doldurur.

## ZORUNLU görsel doğrulama döngüsü

Grafik çizdiysen **bakmadan bitirme.** K5 kapısı bunu ister.

```bash
cd apps/web && npm run build:vitrin
python tools/ekran_goruntusu.py --yol grafik.html --ad grafik --etiket i1 --tema koyu
python tools/kirp.py docs/design/ui/grafik-koyu-1440-i1.png 236 210 1200 600 --olcek 1 --ad bak.png
```

Sonra **Read ile aç ve GÖR**. Referans görseli yanına koy. Kusurları madde
madde yaz, düzelt, tekrarla — **en az 3 iterasyon**. Her turda *ne görüldü, ne
düzeltildi* pasaporta ve `docs/design/ui/README.md`'ye yazılır.

Küçük kusurlar için **yakınlaştır** (`--olcek 2.6`): 9.5px bir etiketin bir
çizgiyle karışması tam sayfa görüntüde görünmez.

## Referanstan sapma

Referansta olup üretmediğin her şey **gerekçesiyle** yazılır. Örnek: Altın
Bölge referansındaki kesik-noktalı mavi trend çizgisi üretilmedi — o çizgi bu
stratejiye değil ayrı bir trendline göstergesine ait; komposerin onu üretmesi
katman ayrımını bozardı.

## Doğrulama

```bash
python -m pytest packages/chart/tests -q
cd apps/web && npm run build && npx eslint
```
