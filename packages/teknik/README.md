# quaxis.teknik — tarama motoru altyapısı

Önceki `Teknik Analiz\tlab` çalışmasından **taşınan**, strateji-bağımsız
katmanlar. ADR-001 §2 ve ADR-002 §1'in karşılığıdır.

```
core/      Signal, IndicatorResult, BaseIndicator, Registry, Catalog, params
data/      sağlayıcı, parquet önbelleği, takvim, resample, evren, doğrulama
scanner/   evren × zaman dilimi tarama, EOD akışı, SQLite sonuç deposu, filtre
testing/   repaint testi, statik lookahead lint'i, fikstürler
```

## Neyin taşınmadığı — ve neden

| Katman | Karar | Gerekçe |
|---|---|---|
| `indicators/` (27 gösterge) | **taşınmadı** | ADR-002: sıfırdan yazılacak. Kalibrasyonu ölçümle çürütüldü. |
| `features/` | **taşınmadı** | ADR-002: strateji strateji, pasaportunda gözden geçirilerek gelecek. `build_trendlines`'ın CMT kuralına uymayan aday eşleştirmesi bunun somut gerekçesi. |
| `scanner/confluence.py` | **taşınmadı** | Birden çok göstergenin sinyalini birleştirir — altyapı değil **strateji** katmanı, ayrıca `features`'a bağlı. Ters-dönüş haritası kendi stratejisiyle Bölüm C'de döner. |
| `viz/` | **taşınmadı** | ADR-001: yerine `packages/chart` (ChartSpec) geldi. |
| `cli.py`, `dashboard.py` | **taşınmadı** | Ürün yüzeyi artık `apps/web`; motorun çağrı kapısı `services/api` ile gelecek. |

## Göçte yapılan üç yapısal düzeltme

**1. Tarayıcının gösterge paketine bağımlılığı kesildi.**
Eski depoda `scanner/engine.py` ve `scanner/eod.py` doğrudan
`tlab.indicators.bootstrap`'ten `CATALOG` / `populate_registry` /
`scaled_factory` alıyordu — katman ayrımı kuralının (`Veri → Özellik →
Gösterge → Tarayıcı`) **tersine aktığı tek yer**. Motor o paket olmadan import
bile edilemiyordu.

Artık motor yalnız `core/catalog.py`'deki arayüzü bilir; katalog bir
**argüman**dır:

```python
engine.run(..., catalog="quaxis.teknik.indicators.bootstrap:CATALOG")
```

Katalog nesnesi süreçler arası geçirilmez (fabrikalar closure olabilir, pickle
edilemez) — **adresi** geçer, her işçi süreç kendi içinde çözüp önbelleğe alır.
Sonuç: altyapı, tek bir gösterge yazılmadan uçtan uca test edilebiliyor.

**2. Yol sabitleri tek yere toplandı.**
Her modül kendi `Path(__file__).parents[2]` derinlik sayısını taşıyordu; dosya
bir dizin taşınınca sessizce yanlış klasöre bakıyordu. Artık `yollar.py`:

| Değişken | Ortam değişkeni | Varsayılan |
|---|---|---|
| `CONFIG_KOK` | `QUAXIS_TEKNIK_CONFIG` | `packages/teknik/config` |
| `VERI_KOK` | `QUAXIS_TEKNIK_DATA` | `data/ohlcv` |

`VERI_KOK`'un ortam değişkeni olması kolaylık değil **zorunluluk**: tarama
işçileri ayrı süreçlerde koşar ve `Store`'u kendileri kurar; `monkeypatch`
süreç sınırını geçmez, `os.environ` geçer.

**3. Uçtan uca tarama testi gerçekten koşuyor.**
Eski depoda motorun uçtan uca testi gerçek göstergelere ve `data/ohlcv/`
altındaki gerçek parquet önbelleğine bağlıydı; önbellek yoksa **atlanıyordu** —
temiz bir klonda hiçbir şey kanıtlamıyordu. Artık veri `SentetikSaglayici`'dan,
göstergeler test kataloğundan gelir: **ağ yok, önbellek yok, atlama yok.**

## Koşturma

```bash
# depo kökünden — kurulum gerekmez, conftest.py paketleri sys.path'e koyar
python -m pytest                      # ağ testleri hariç
python -m pytest -m network           # yalnız ağa çıkanlar
python -m ruff check packages/
```

## Paketleme

`packages/*/quaxis/<ad>` altındaki modüller **PEP 420 isim alanı paketi**
olarak birleşir: `quaxis.teknik` ve `quaxis.chart` ayrı klasörlerde yaşar, tek
isim alanını paylaşır. `quaxis/` klasörlerinde bilerek `__init__.py` **yoktur**
— olsaydı iki paket birbirini gölgelerdi.

## Sırada

Göstergeler (Bölüm C) yazılırken her biri kendi kataloğunu kurup motora
verecek. `core/catalog.py::Catalog.populate_registry` repaint kapısını zaten
tutuyor: registry'e kaydedilmemiş bir gösterge taranamaz.
