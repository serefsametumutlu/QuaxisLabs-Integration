# kesitsel-momentum_12_1 — K3 + K4 · 1D

**Tarih:** 2026-09-13 · **Gösterge:** `kesitsel_momentum_12_1`
**Dönem:** 2010-01-01 – 2026-09-11 · **Yön:** yalnız alış

## K3 · Kalibrasyon

| | |
|---|---|
| Evren | 196 sembol |
| Toplam sinyal | 947 |
| Sıfır sinyal veren sembol | 0 (%0.0) |
| Veri hatası | 0 |
| Sembol başına ortalama | 4.8 |
| Sembol başına ortanca | 4 |

MAKUL: sembol başına ortalama 4.8 aday, sembollerin %0'i sıfır.

> Sinyaller **örtüşmüyor**: bir sembol için yeni sinyal, öncekinin
> 25 barlık tutuşu bitmeden üretilmiyor (Chan s.151).

## K4 · İstatistik

| | |
|---|---|
| **Bağımsız gözlem (sembol)** | **177** |
| Ölçülen sinyal | 759 |
| Pencere | ilk %70 IS / son %30 OOS |
| Ufuk | 25 bar (stratejinin kendi tutuş süresi) |
| **Sinyal getirisi** | **%+1.66** |
| **Adil baz** (rastgele sembol) | **%+9.62** |
| **Fark** | **%-7.96** |
| Kazanan sembol | 97/177 |
| Permütasyon p değeri | 1.0000 (2000 tur) |
| **Verdikt** | **kanitlanmadi** |

İşlem maliyeti **dahil**: taraf başına %0.05 komisyon + %0.05 kayma.
Giriş de çıkış da piyasa emri sayıldı — sıralama barının kapanışında
alınıyor, tutuş bitince kapanışta satılıyor.

## Ne çıkarsa o

**Momentum kenar üretmedi — üstelik güçlü biçimde TERS yönde.**

Son 12 ayın en çok kazanan %10'unu alıp 25 gün tutmak, aynı dönemde
**rastgele** bir hisse almaya göre −%7.96 puan geride bıraktı. p=1.0000,
yani gözlenen fark boş dağılımın en alt ucunda: bu "fark bulunamadı"
değil, **ters yönde net bir fark var** demek.

| | Momentum üst %10 | Rastgele hisse |
|---|---|---|
| 25 barlık getiri | **%+1.66** | **%+9.62** |

Adil bazın %+9.62 olması ayrıca önemli bir bilgi: ölçüm penceresinde
(son %30, kabaca 2021 sonrası) BIST'te **rastgele bir hisse almak** 25
barda ortalama bu kadar kazandırmış. Yüksek enflasyon dönemi ve 2021–2024
ralisi bu sayının içinde. Momentum hisseleri o ralinin dışında kalmış.

### Bu ne demek

Kaynağın (Chan s.152) kendi uyarısı burada birebir gerçekleşiyor:

> "Hisselerde kesitsel momentum 2008–2009 borsa çöküşünün ardından
> **kayboldu ve yerini güçlü ortalamaya dönüşe bıraktı.**"

BIST'te ölçtüğümüz şey tam olarak bu: kesitsel **ortalamaya dönüş**.
Geçen yılın kazananları sonraki ayda geri veriyor.

### Son ayı atlamak (12-1) düzeltmiyor

Akademik literatürün standardı olan "son ayı atla" varyantı farkı
−%7.96 yerine −%7.96'ya çekiyor — yönü değiştirmiyor, sadece biraz
yumuşatıyor. İki varyant da aynı şeyi söylüyor.

### Ne YAPILMADI

Bu sonuç "tersini yap" demeyi çağırıyor: en çok kaybedenleri al.
**Ölçmedim.** Sonuca bakıp yön çevirmek, bu projenin önlemek için
kurulduğu şeydir. Ters varyant kendi ön kaydını hak ediyor — ve şansı
var, çünkü ortalamaya dönüş hipotezi sonradan uydurulmuş değil:
Chan'ın 3–5. bölümleri ve De Bondt–Thaler literatürü bunun üstüne kurulu.

## Ölçümün sınırları

| | |
|---|---|
| Yalnız alış | Kaynak uzun/kısa kuruyor; yalnız alış piyasa yönünü nötrlemez |
| Nominal TL | Getiriler enflasyondan arındırılmadı; adil baz aynı enflasyonu taşıdığı için KARŞILAŞTIRMA geçerli, ama mutlak sayılar reel değil |
| Portföy etkisi | Sinyal başına ölçüldü; eş zamanlı pozisyon sayısı ve sermaye dağıtımı modellenmedi |
| Hayatta kalma yanlılığı | Evren bugünkü listeden |
| Dönem | OOS penceresi tek bir rejim (2021 sonrası) olabilir; dönem kırılımı ölçülmedi |
