# QuaxisLabs

**Temel analiz ile teknik analizin tek bir tarama ürününde birleştiği yer.**

BIST ve NASDAQ için; veriyi kendimiz çekeriz, sinyali kendimiz üretiriz,
grafiği kendimiz çizeriz. Gösterge kiralamıyoruz.

> **Bu depo, teknik analiz tarafının sıfırdan yeniden inşasıdır.** Motor
> (`packages/teknik`) önceki `Teknik Analiz\tlab` çalışmasından taşınmıştır;
> çizim ve arayüz katmanları tamamen yenidir. Gerekçe:
> [`docs/karar/ADR-001-yeniden-insa.md`](docs/karar/ADR-001-yeniden-insa.md).

---

## Dizin yapısı

```
apps/
  web/          Next.js 16 + React 19 + TypeScript + Tailwind 4 — ana ürün yüzeyi
  mobile/       (Faz 11) Flutter
services/
  api/          FastAPI — teknik + temel için TEK kapı
packages/
  teknik/       Tarama motoru: core, data, scanner, testing (gösterge YOK — Bölüm C)
  temel/        (Faz 10) Bilanço / mercek motoru
  chart/        ChartSpec v1 sözleşmesi + strateji başına komposer (Python)
  ortak/        Paylaşılan tipler, semboller, takvim, Türkçe etiketler
docs/
  karar/        ADR — mimari karar kayıtları
  strateji/     Strateji başına 1 "pasaport" dosyası (7 kapı)
  design/       Tasarım şartnamesi + referans görseller
  olcum/        İstatistiksel doğrulama raporları
references/     Mobbin şemaları, ekran görüntüleri
tools/          Görsel kabul döngüsü, snapshot ve karşılaştırma araçları
```

## Müzakereye kapalı kurallar

1. **Non-repaint sözleşmesi.** `signal(t)` yalnızca `t` ve öncesindeki barların
   verisiyle hesaplanır ve `t` sonrasında hiçbir zaman değişmez. Walk-forward
   eşitlik testi + statik lookahead lint'i geçmeyen gösterge registry'ye
   kaydedilemez.
2. **Katman ayrımı, tek yönlü.** `Veri → Özellik → Gösterge → Tarayıcı → Depo →
   ChartSpec → Görselleştirme`. Görselleştirme hesap yapmaz.
3. **Deterministiklik.** Aynı veri + aynı parametre = bit-bit aynı sonuç.
   Parametreler frozen dataclass, sonuçlar `params_hash` taşır, global durum yok.
4. **Strateji Pasaportu.** Hiçbir strateji 7 kapının tamamından geçmeden
   "bitti" sayılmaz ve sıradakine geçilmez. Bkz. `docs/strateji/_SABLON.md`.
5. **Görsel kabul döngüsü zorunlu.** Her komposer gerçek veriyle render edilir,
   ekran görüntüsü alınır, referans görselle yan yana konur — en az 3 iterasyon.
6. **Dürüstlük.** Ölçülmemiş bir iddia sitede "kanıtlanmış" diye gösterilmez.
   Her stratejinin yanında tarihsel isabet rozeti bulunur: *ölçüldü / ölçülmedi /
   kanıtlanmadı*.
7. **Dil.** Docstring ve kullanıcıya dönen etiketler Türkçe, kod tanımlayıcıları
   İngilizce.

## Durum

Kapsam: **site + teknik analiz.** Temel analiz ve mobil bu yol haritasında yok
(bkz. [ADR-002](docs/karar/ADR-002-strateji-kodlari-sifirdan.md)).

### Bölüm A — Site (senin onayın alınmadan B'ye geçilmez)

| Faz | İş | Durum |
|---|---|---|
| 0 | Kuruluş — depo, iskelet, ADR'ler | ✅ bitti |
| 1 | Tasarım referansları ve ortak tasarım dilinin çıkarılması | ✅ bitti |
| 2 | Tasarım sistemi + bileşen kütüphanesi + `/tasarim` vitrini | ✅ bitti |
| 3 | Uygulama kabuğu ve sayfa iskeletleri | ✅ bitti |
| 4 | `ChartSpec` v1 + grafik motoru; referans grafiklerin birebir üretimi | ✅ bitti |

### Bölüm B — Altyapı

| Faz | İş | Durum |
|---|---|---|
| 5 | Altyapı göçü: `core` + `testing` + `data` + `scanner` (gösterge YOK) | ✅ bitti |
| 6 | Strateji Pasaportu süreci: şablon, agent'lar, skill'ler | **sırada** |

### Bölüm C — Stratejiler (birer birer, **sayı sınırı yok**)

Her strateji kendi fazıdır ve **7 kapının tamamından geçmeden sıradakine
geçilmez**. Kodu kitaptan yeniden türetilir; eski koda referans olarak değil,
yalnızca karşılaştırma için bakılır.

| Faz | Strateji | Durum |
|---|---|---|
| 7.1 | *(sıra Bölüm B bitince belirlenecek)* | bekliyor |

## Web uygulaması

```bash
cd apps/web
npm install
npm run dev            # http://localhost:3000
npm run build          # üretim derlemesi
npm run lint

# görsel kabul döngüsü
npm run build:vitrin                          # statik dışa aktarım -> out/
python ../../tools/ekran_goruntusu.py --etiket i1
python ../../tools/tablo_olcum.py             # DataTable 500 satır ölçümü
```

### Yüzeyler

| Yol | Ne | Durum |
|---|---|---|
| `/` | Giriş ekranı — hero, olgu şeridi, 7 kapı, rozet açıklaması | iskelet ✅ |
| `/tarama` | Tarama tablosu + sağdan açılan grafik çekmecesi | iskelet ✅ |
| `/grafik` | Grafik levhası — `ChartSpec` okuyan gerçek motor | ✅ |
| `/stratejiler` | Strateji kütüphanesi (kart ızgarası) | iskelet ✅ |
| `/stratejiler/<ad>` | Strateji künyesi: parametreler, **Kaynak** (K0), **Ölçüm** (K4), SSS | iskelet ✅ |
| `/tasarim` | Bileşen vitrini — 15 bileşen, üç tema yan yana | ✅ |

Kabuk her yüzeyde ortak: yapışkan üst şerit, `Ctrl+K` hızlı geçiş, sol ray,
tema (sistem/açık/koyu) ve aksan anahtarı. **Veri hâlâ örnektir** ve arayüzde
her yerde öyle etiketlenir.

### Grafik motoru

```
gösterge → TİPLİ SONUÇ → KOMPOSER → ChartSpec (JSON) → web çizici
 (Bölüm C)              (packages/chart, Python)        (apps/web)
```

Mum, hacim, crosshair ve zoom/pan **Lightweight Charts v5**'ten; fibo
merdiveni, dolgulu X-A-B-C-D gövdeleri, köşe rozetleri ve önder çizgili durum
rozeti **bizim SVG overlay**'imizden gelir. Çizici hiçbir seviyeyi kendisi
hesaplamaz ve ChartSpec renk taşımaz — rol → token eşlemesi çizici tarafında.

Sözleşme ve üç yapısal güvencesi: [`packages/chart/README.md`](packages/chart/README.md).

```bash
cd packages/chart
python -m pytest tests -q   # 47 test
python uret.py              # şema + örnek ChartSpec üretir
```

Next.js 16 + React 19 + TypeScript + Tailwind 4. Token sistemi
[`apps/web/app/tokens.css`](apps/web/app/tokens.css)'te ve onaylanmış maketten
**birebir** taşınmıştır. Fontlar (Archivo · Inter · JetBrains Mono)
`next/font/local` ile yereldir; CDN bağımlılığı yoktur. Bileşenler
[`apps/web/components/ui/`](apps/web/components/ui) altında; hepsi
[`/tasarim`](apps/web/app/(uygulama)/tasarim/page.tsx) vitrininde üç temada yan yana
gösterilir. Görsel kabul kaydı:
[`docs/design/ui/README.md`](docs/design/ui/README.md).

## Python tarafı

```bash
# depo kökünden — kurulum gerekmez
python -m pytest              # 140 test (ağ testleri hariç)
python -m pytest -m network   # yalnız ağa çıkanlar
python -m ruff check packages/
```

`packages/*/quaxis/<ad>` altındaki modüller **PEP 420 isim alanı paketi**
olarak birleşir; kökteki `conftest.py` paketleri `sys.path`'e koyar.

| Paket | Ne | Belge |
|---|---|---|
| `quaxis.teknik` | Tarama motoru altyapısı (core · data · scanner · testing) | [`packages/teknik/README.md`](packages/teknik/README.md) |
| `quaxis.chart` | ChartSpec v1 sözleşmesi + strateji komposerleri | [`packages/chart/README.md`](packages/chart/README.md) |

**Gösterge katmanı henüz yok.** ADR-002 gereği sıfırdan yazılacak; motor
bunu bir katalog ARAYÜZÜ üzerinden bekliyor ve tek bir gösterge olmadan da
uçtan uca test ediliyor.

Tam plan: [`docs/00_RAPOR_VE_YOL_HARITASI.md`](docs/00_RAPOR_VE_YOL_HARITASI.md)
Sonraki oturumun promptu: [`docs/SONRAKI_OTURUM_PROMPTU.md`](docs/SONRAKI_OTURUM_PROMPTU.md)
Onaylanmış maket: [`docs/design/maket_v1.html`](docs/design/maket_v1.html)

---

*Bu yazılım yatırım tavsiyesi değildir.*
