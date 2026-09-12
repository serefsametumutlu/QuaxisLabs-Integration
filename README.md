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
  teknik/       Tarama motoru: core, data, features, indicators, scanner, testing
  temel/        (Faz 10) Bilanço / mercek motoru
  chart/        ChartSpec üreticileri (strateji başına komposer)
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

| Faz | İş | Durum |
|---|---|---|
| 0 | Kuruluş — depo, iskelet, ADR | **devam ediyor** |
| 1 | Sözleşmeler — ChartSpec, pasaport şablonu, skill'ler | bekliyor |
| 2 | Tasarım sistemi ve uygulama kabuğu | bekliyor |
| 3 | Motor göçü (`packages/teknik`) | bekliyor |
| 4 | İlk strateji uçtan uca — `structure.golden_zone` | bekliyor |
| 5–8 | Strateji strateji (2→9) | bekliyor |
| 9 | Tarama / alarm / evren yüzeyleri | bekliyor |
| 10 | Temel analiz entegrasyonu | bekliyor |
| 11 | Mobil | bekliyor |

Tam plan: [`docs/00_RAPOR_VE_YOL_HARITASI.md`](docs/00_RAPOR_VE_YOL_HARITASI.md)

---

*Bu yazılım yatırım tavsiyesi değildir.*
