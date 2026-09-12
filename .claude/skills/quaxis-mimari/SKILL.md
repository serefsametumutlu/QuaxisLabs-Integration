---
name: quaxis-mimari
description: QuaxisLabs deposunun çekirdek mimarisi — katman ayrımı, non-repaint sözleşmesi, ChartSpec, paket düzeni, yasak desenler. Bu depoda HERHANGİ bir koda dokunmadan önce oku; agent'ların ve oturumların ilk okuyacağı dosya budur.
---

# QuaxisLabs mimarisi

Bu depo, teknik analiz tarafının **sıfırdan yeniden inşasıdır**. Neyin neden
böyle olduğunu bilmeden dokunma: buradaki kuralların çoğu, önceki projede
**ölçülmüş bir hatanın** karşılığıdır.

Karar kayıtları: [`docs/karar/ADR-001`](../../../docs/karar/ADR-001-yeniden-insa.md) ·
[`ADR-002`](../../../docs/karar/ADR-002-strateji-kodlari-sifirdan.md)

## Katman ayrımı — tek yönlü

```
Veri → Özellik → Gösterge → Tarayıcı → Depo → ChartSpec → Görselleştirme
```

Ok yalnız sağa bakar. **Görselleştirme hesap yapmaz; hesap yapan renk seçmez.**

Faz 5'te bu kuralın tersine aktığı tek yer kapatıldı: tarayıcı doğrudan
gösterge paketinden `CATALOG` alıyordu. Artık katalog bir **argüman**
(`core/catalog.py`). Yeni bir katman bağı kurmadan önce bu oku.

## Müzakereye kapalı yedi kural

README'deki liste bağlayıcıdır. En sık ihlal edilen üçü:

1. **Non-repaint.** `signal(t)` yalnız `t` ve öncesinin verisiyle hesaplanır ve
   `t` sonrasında **asla** değişmez. Sinyal, pivotun barını değil **onaylandığı
   barı** taşır (`Signal.detected_at` ≠ `Signal.bar_time`). Walk-forward eşitlik
   testi + lookahead lint'i geçmeyen gösterge registry'ye kaydedilemez.
2. **Deterministiklik.** Aynı veri + aynı parametre = **bit bit** aynı sonuç.
   Parametreler `frozen dataclass`, sonuçlar `params_hash` taşır, global durum
   yok.
3. **Dürüstlük.** Ölçülmemiş bir iddia "kanıtlanmış" diye gösterilmez. Her
   stratejinin yanında verdikt rozeti durur: *ölçüldü / ölçülmedi /
   kanıtlanmadı*.

## Paket düzeni

`packages/*/quaxis/<ad>` → **PEP 420 isim alanı paketi**. `quaxis/`
klasörlerinde bilerek `__init__.py` **yoktur** — olsaydı paketler birbirini
gölgelerdi. Kurulum gerekmez; kökteki `conftest.py` `sys.path`'i kurar.

| Paket | Ne |
|---|---|
| `quaxis.teknik` | Motor altyapısı: core · data · scanner · testing. **Gösterge YOK.** |
| `quaxis.chart` | ChartSpec v1 sözleşmesi + strateji başına komposer |

Yol sabitleri `quaxis/teknik/yollar.py`'de; `QUAXIS_TEKNIK_CONFIG` ve
`QUAXIS_TEKNIK_DATA` ile taşınır. Veri kökünün ortam değişkeni olması
zorunluluktur: tarama işçileri ayrı süreçlerde koşar, `monkeypatch` süreç
sınırını geçmez.

## ChartSpec — çizim sözleşmesi

```
gösterge → TİPLİ SONUÇ → KOMPOSER → ChartSpec (JSON) → çizici
```

Üç yapısal güvence (`packages/chart/README.md`):

1. Roller **kapalı küme** — tanınmayan ad `ValueError` atar, sessizce griye
   düşmez.
2. Panel y aralığı **yalnız o panelin serilerinden** gelir; komposer bilinçli
   genişletirse gerekçesiyle yazar ve aralık seriyi **kırpamaz**.
3. Seriler **tam dizi** taşır; iki uca indirgenemez.

**ChartSpec renk taşımaz.** Rol → token eşlemesi çizici tarafındadır.

**Jenerik çizici yok.** Her strateji kendi komposerini alır. Eski depoda tek
bir 10 475 satırlık çizici 24 stratejiyi aynı primitif torbasıyla basıyordu;
sonuç okunamayan grafiklerdi.

## Yasak desenler

| Desen | Neden yasak |
|---|---|
| `rolling(..., center=True)` | Merkezi pencere geleceğe bakar. Lint yakalar (LA002). |
| `shift(-n)` | Negatif kaydırma geleceği okur. Lint yakalar (LA001). |
| `argrelextrema` / `find_peaks` doğrudan sinyalde | Tepe ancak sağdaki barlar geldiğinde kesinleşir; doğrudan kullanım repaint üretir. |
| Göstergeden renk/piksel döndürmek | Katman ayrımı. Gösterge rol ve değer üretir. |
| Tarayıcıdan somut gösterge paketi import etmek | Faz 5'te kapatıldı; katalog argüman olarak gelir. |
| Ölçülmemiş bir eşiği "genel kabul" diye yazmak | K0 kapısı reddeder (`tools/pasaport.py`). |

## Doğrulama komutları

```bash
python -m pytest                    # 156 test (ağ hariç)
python -m ruff check packages/ tools/
python tools/pasaport.py dogrula    # strateji kapıları tutarlı mı
cd apps/web && npm run build && npx eslint
```

## Dil

Docstring ve kullanıcıya dönen etiketler **Türkçe**. Kod tanımlayıcıları:
`packages/teknik` **İngilizce** (taşınan motor kodu tutarlılığı), `apps/web` ve
`packages/chart` **Türkçe**. Bir dosyaya dokunurken **komşularına uy** — karma
yazma.

## Görsel iş yapıyorsan

`grafik-tasarim-sistemi` (grafik/SVG) ya da `web-tasarim-sistemi` (arayüz)
skill'ini de oku. Görsel kabul döngüsü **zorunludur**: render → ekran görüntüsü
→ referansla karşılaştır → düzelt, **en az 3 iterasyon**.

## Strateji işi yapıyorsan

`strateji-pasaportu` skill'ini oku. Yedi kapı vardır ve kapılar denetlenir.
