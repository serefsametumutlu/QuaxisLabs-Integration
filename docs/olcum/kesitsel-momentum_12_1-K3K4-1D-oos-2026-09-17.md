# kesitsel-momentum_12_1 — K3 + K4 · 1D

**Tarih:** 2026-09-17 · **Gösterge:** `kesitsel_momentum_12_1`
**Dönem:** 2010-01-01 – 2026-09-11 · **Yön:** yalnız alış

## K3 · Kalibrasyon

| | |
|---|---|
| Evren | 236 sembol |
| Toplam sinyal | 1119 |
| Sıfır sinyal veren sembol | 0 (%0.0) |
| Veri hatası | 23 |
| Sembol başına ortalama | 4.7 |
| Sembol başına ortanca | 4 |

MAKUL: sembol başına ortalama 4.7 aday, sembollerin %0'i sıfır.

> Sinyaller **örtüşmüyor**: bir sembol için yeni sinyal, öncekinin
> 25 barlık tutuşu bitmeden üretilmiyor (Chan s.151).

## K4 · İstatistik

| | |
|---|---|
| **Bağımsız gözlem (sembol)** | **220** |
| Ölçülen sinyal | 920 |
| Pencere | **OOS** (bölme: ilk %70 / son %30) |
| Ufuk | 25 bar (stratejinin kendi tutuş süresi) |
| **Sinyal getirisi** | **%+1.75** |
| **Adil baz** (rastgele sembol) | **%+9.14** |
| **Fark** | **%-7.39** |
| Kazanan sembol | 119/220 |
| Permütasyon p değeri | 1.0000 (2000 tur) |
| **Verdikt** | **kanitlanmadi** |

İşlem maliyeti **dahil**: taraf başına %0.05 komisyon + %0.05 kayma.
Giriş de çıkış da piyasa emri sayıldı — sıralama barının kapanışında
alınıyor, tutuş bitince kapanışta satılıyor.

## Ne çıkarsa o

**"Son ayı atla" varyantı da düzeltilmiş veride kenar üretmedi.**

Akademik literatürün standardı olan 12-1 varyantı (sıralama son ayı
dışlayarak yapılır) farkı −%9.62 yerine **−%7.39**'a çekiyor — yönü
değiştirmiyor, sadece yumuşatıyor. İki varyant da aynı şeyi söylüyor.

| | Düzeltme öncesi (09-13) | Düzeltme sonrası (09-17) |
|---|---|---|
| Sinyal veren sembol | 196 | **236** |
| Bağımsız gözlem | 177 | **220** |
| Sinyal getirisi | %+1.66 | **%+1.75** |
| Adil baz | %+9.62 | **%+9.14** |
| **Fark** | %−7.96 | **%−7.39** |
| p | 1.0000 | **1.0000** |

Fark negatif kaldı; ön kayıt §5'in birinci maddesi sağlanmadı.

**VERDİKT DEĞİŞMEDİ: `kanıtlanmadı`.**

Ayrıntılı yorum ana varyantın dosyasında:
[`kesitsel-momentum-K3K4-1D-oos-2026-09-17.md`](kesitsel-momentum-K3K4-1D-oos-2026-09-17.md).

## Ölçümün sınırları

| | |
|---|---|
| Yalnız alış | Kaynak uzun/kısa kuruyor; yalnız alış piyasa yönünü nötrlemez |
| Portföy etkisi | Sinyal başına ölçüldü; eş zamanlı pozisyon sayısı
ve sermaye dağıtımı modellenmedi |
| Hayatta kalma yanlılığı | Evren bugünkü listeden |
| Momentum çöküşü | Chan s.152: krizden sonra yıllarca kötü. Dönem kırılımı ayrıca ölçülmeli |
