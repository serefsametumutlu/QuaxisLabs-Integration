# kesitsel-momentum — K3 + K4 · 1D

**Tarih:** 2026-09-17 · **Gösterge:** `kesitsel_momentum`
**Dönem:** 2010-01-01 – 2026-09-11 · **Yön:** yalnız alış

## K3 · Kalibrasyon

| | |
|---|---|
| Evren | 221 sembol |
| Toplam sinyal | 1094 |
| Sıfır sinyal veren sembol | 0 (%0.0) |
| Veri hatası | 23 |
| Sembol başına ortalama | 5.0 |
| Sembol başına ortanca | 4 |

MAKUL: sembol başına ortalama 5.0 aday, sembollerin %0'i sıfır.

> Sinyaller **örtüşmüyor**: bir sembol için yeni sinyal, öncekinin
> 25 barlık tutuşu bitmeden üretilmiyor (Chan s.151).

## K4 · İstatistik

| | |
|---|---|
| **Bağımsız gözlem (sembol)** | **200** |
| Ölçülen sinyal | 897 |
| Pencere | **OOS** (bölme: ilk %70 / son %30) |
| Ufuk | 25 bar (stratejinin kendi tutuş süresi) |
| **Sinyal getirisi** | **%+0.20** |
| **Adil baz** (rastgele sembol) | **%+9.82** |
| **Fark** | **%-9.62** |
| Kazanan sembol | 109/200 |
| Permütasyon p değeri | 1.0000 (2000 tur) |
| **Verdikt** | **kanitlanmadi** |

İşlem maliyeti **dahil**: taraf başına %0.05 komisyon + %0.05 kayma.
Giriş de çıkış da piyasa emri sayıldı — sıralama barının kapanışında
alınıyor, tutuş bitince kapanışta satılıyor.

## Ne çıkarsa o

**Momentum yine kenar üretmedi — yine güçlü biçimde TERS yönde. Verdikt
değişmedi.**

Bu ölçüm, [`onkayit-veri-duzeltme.md`](onkayit-veri-duzeltme.md) §6 gereği
düzeltilmiş veriyle yapılan **tek** koşudur.

Son 12 ayın en çok kazanan %10'unu alıp 25 gün tutmak, aynı dönemde
**rastgele** bir hisse almaya göre −%9.62 puan geride kaldı. p=1.0000, yani
gözlenen fark boş dağılımın en alt ucunda: bu "fark bulunamadı" değil,
**ters yönde net bir fark var** demek.

| | Momentum üst %10 | Rastgele hisse |
|---|---|---|
| 25 barlık getiri | **%+0.20** | **%+9.82** |

### Düzeltme öncesi/sonrası

Momentum tarafında karşılaştırma temiz: 13 Eylül'ün ölçümü de işlem
maliyetini içeriyordu, araç değişmedi. Değişen tek şey **hangi barların ve
sembollerin gözlem sayıldığı**.

| | Düzeltme öncesi (09-13) | Düzeltme sonrası (09-17) |
|---|---|---|
| Sinyal veren sembol | 186 | **221** |
| Ölçülen sinyal | 737 | **897** |
| Bağımsız gözlem | 163 | **200** |
| Sinyal getirisi | %+0.02 | **%+0.20** |
| Adil baz | %+10.00 | **%+9.82** |
| **Fark** | %−9.98 | **%−9.62** |
| p | 1.0000 | **1.0000** |

Fark 0.36 puan daraldı ve **negatif** kaldı. Ön kayıt §5'in birinci maddesi
(*fark pozitif*) sağlanmadı; ikinci ve üçüncü maddeye bakmaya gerek yok.

**VERDİKT DEĞİŞMEDİ: `kanıtlanmadı`.**

### Ön kaydın tahmini (§4) burada da tutmadı

§4 "adil baz düşecek, fark yükselecek" diyordu. Adil baz gerçekten düştü
(%+10.00 → %+9.82) ama fark yükselmedi — **daha az negatif** oldu, ki bu
verdikti değiştirecek bir yön değil. Harmoniklerde tahmin ters çıkmıştı;
burada yönü tuttu, büyüklüğü anlamsız kaldı.

### Sinyal sayısı düşmedi, arttı

§5 "sinyal sayısı %20'den fazla düşerse sebebi incelenir" diyordu. Ham
sinyal 922 → 1094'e **çıktı**: D2 sinyal keserken D3'ün kurtardığı 81
sembol baskın geldi. İncelemeyi gerektiren durum oluşmadı.

### Bu ne demek

Kaynağın (Chan s.152) kendi uyarısı düzeltilmiş veride de birebir duruyor:
BIST'te ölçtüğümüz şey kesitsel momentum değil, kesitsel **ortalamaya
dönüş**. Geçen yılın kazananları sonraki ayda geri veriyor.

Ters varyant (`kesitsel_donus`) kendi ön kaydıyla ayrıca ölçüldü ve
**reddedildi**: [`onkayit-kesitsel-donus.md`](onkayit-kesitsel-donus.md).
Bu koşuda ona dokunulmadı — ayrı bir hipotez, ayrı bir ön kayıt.

## Ölçümün sınırları

| | |
|---|---|
| Yalnız alış | Kaynak uzun/kısa kuruyor; yalnız alış piyasa yönünü nötrlemez |
| Portföy etkisi | Sinyal başına ölçüldü; eş zamanlı pozisyon sayısı
ve sermaye dağıtımı modellenmedi |
| Hayatta kalma yanlılığı | Evren bugünkü listeden |
| Momentum çöküşü | Chan s.152: krizden sonra yıllarca kötü. Dönem kırılımı ayrıca ölçülmeli |
