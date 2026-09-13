# kesitsel-donus — K3 + K4 · 1D

**Tarih:** 2026-09-13 · **Gösterge:** `kesitsel_donus`
**Dönem:** 2010-01-01 – 2026-09-11 · **Yön:** yalnız alış

## K3 · Kalibrasyon

| | |
|---|---|
| Evren | 243 sembol |
| Toplam sinyal | 994 |
| Sıfır sinyal veren sembol | 0 (%0.0) |
| Veri hatası | 0 |
| Sembol başına ortalama | 4.1 |
| Sembol başına ortanca | 3 |

MAKUL: sembol başına ortalama 4.1 aday, sembollerin %0'i sıfır.

> Sinyaller **örtüşmüyor**: bir sembol için yeni sinyal, öncekinin
> 25 barlık tutuşu bitmeden üretilmiyor (Chan s.151).

## K4 · İstatistik

| | |
|---|---|
| **Bağımsız gözlem (sembol)** | **213** |
| Ölçülen sinyal | 832 |
| Pencere | **OOS** (bölme: ilk %70 / son %30) |
| Ufuk | 25 bar (stratejinin kendi tutuş süresi) |
| **Sinyal getirisi** | **%+3.49** |
| **Adil baz** (rastgele sembol) | **%+3.74** |
| **Fark** | **%-0.25** |
| Kazanan sembol | 116/213 |
| Permütasyon p değeri | 0.5142 (2000 tur) |
| **Verdikt** | **kanitlanmadi** |

İşlem maliyeti **dahil**: taraf başına %0.05 komisyon + %0.05 kayma.
Giriş de çıkış da piyasa emri sayıldı — sıralama barının kapanışında
alınıyor, tutuş bitince kapanışta satılıyor.

## Ne çıkarsa o

*(Sonuç olumsuzsa da aynı açıklıkla yazılır.)*

## Ölçümün sınırları

| | |
|---|---|
| Yalnız alış | Kaynak uzun/kısa kuruyor; yalnız alış piyasa yönünü nötrlemez |
| Portföy etkisi | Sinyal başına ölçüldü; eş zamanlı pozisyon sayısı
ve sermaye dağıtımı modellenmedi |
| Hayatta kalma yanlılığı | Evren bugünkü listeden |
| Momentum çöküşü | Chan s.152: krizden sonra yıllarca kötü. Dönem kırılımı ayrıca ölçülmeli |
