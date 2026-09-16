# Veri denetimi — BIST · 1D

**Tarih:** 2026-09-14

> Bu araç veriyi **düzeltmez**, ölçer. Sessizce temizlenen veri, sessizce bozulmuş veriden daha tehlikelidir: birincisinde neyin atıldığını kimse bilmez.

## 1 · Evren kapsamı

| | |
|---|---|
| Evren dosyasındaki sembol | 648 |
| Verisi olan | **625** |
| Dosyası yok | 23 |
| Dosyası var ama boş | 0 |
| Toplam bar | 1 704 151 |
| Sembol başına bar (medyan) | 3592 |
| En kısa / en uzun | 19 / 4290 |

Dosyası olmayanlar (23): `SNKRN`, `QNBFL`, `PEHOL`, `YGYO`, `EFORC`, `SELGD`, `DAGHL`, `DOBUR`, `IPEKE`, `KOZAA`, `KOZAL`, `ROYAL`, `METUR`, `ALMAD`, `GRTRK`, `IDEAS`, `ITTFH`, `KARYE`, `KERVT`, `MIPAZ`, `QNBFB`, `TETMT`, `UZERB`

**Bu sayı kendi başına bir bulgu.** Evren dosyası bu sembolleri listeliyor ama veri yok — yani her ölçüm, farkında olmadan daha küçük bir evrende koşuyor.

## 2 · Hayatta kalma yanlılığı

Son barın yılı — **listeden düşen sembol varsa burada görünür:**

`2026: 625`

**625 sembolün 625'inin son barı 2026'da.** Listeden düşmüş tek bir şirket yok.

Bu, evren dosyasının **bugünün listesinin anlık görüntüsü** olmasının doğrudan sonucu. 2010–bugün arasında iflas eden, birleşen ya da kottan çıkarılan her şirket veri setinde YOK.

### Bunun ölçüme etkisi

Yanlılık hem stratejiyi hem adil bazı besliyor — ikisi de aynı evrenden çekiliyor — bu yüzden **farkı** ne kadar bozduğu ölçülmeden bilinemez. Ama iki şey kesin:

1. **Mutlak sayılar iyimser.** Sıfıra giden şirketler eksik olduğu için, stop'la çalışan bir stratejinin gerçek hayattaki en kötü senaryoları veri setinde hiç yok.
2. **Adil baz da iyimser.** Rastgele giriş, "16 yıl ayakta kalmış" filtresinden geçmiş bir evrende yapılıyor.

İlk barın yılı (halka arz dağılımının vekili):

`2010: 266 · 2011: 21 · 2012: 33 · 2013: 20 · 2014: 14 · 2015: 8 · 2016: 2 · 2017: 3 · 2018: 10 · 2019: 5 · 2020: 11 · 2021: 52 · 2022: 36 · 2023: 32 · 2024: 61 · 2025: 19 · 2026: 32`

## 3 · OHLC bütünlüğü

İhlal yok — `high ≥ max(açılış, kapanış)`, `low ≤ min(…)`, `high ≥ low`, `kapanış > 0` hepsinde sağlanıyor.

## 4 · Açılış fiyatı gerçek mi

`açılış == kapanış` olan bar, gövdesiz mumdur. Gerçek piyasada nadirdir; **sistematik olarak yüksekse sağlayıcı açılışı uyduruyordur.**

| Yıl | Bar | `açılış == kapanış` | Oran |
|---|---|---|---|
| 2010 | 66419 | 54291 | **%81.7** |
| 2011 | 71884 | 68448 | **%95.2** |
| 2012 | 78099 | 75341 | **%96.5** |
| 2013 | 85296 | 66510 | **%78.0** |
| 2014 | 90161 | 44937 | **%49.8** |
| 2015 | 93662 | 42160 | **%45.0** |
| 2016 | 94659 | 21246 | **%22.4** |
| 2017 | 94984 | 16852 | **%17.7** |
| 2018 | 97721 | 16023 | **%16.4** |
| 2019 | 98394 | 16692 | **%17.0** |
| 2020 | 97536 | 7587 | **%7.8** |
| 2021 | 103212 | 6556 | **%6.4** |
| 2022 | 116810 | 6757 | **%5.8** |
| 2023 | 123964 | 4792 | **%3.9** |
| 2024 | 137543 | 4571 | **%3.3** |
| 2025 | 147052 | 5347 | **%3.6** |
| 2026 | 106755 | 6139 | **%5.8** |

## 5 · Diğer kusurlar

| Kusur | Sayı | Ne demek |
|---|---|---|
| Hacimsiz bar | 51 456 | O gün işlem görmemiş; fiyat gerçek bir gözlem değil |
| Donuk bar (≥5 bar aynı kapanış) | 22 005 | Sağlayıcı son fiyatı tekrar ediyor olabilir |
| Marjı aşan günlük getiri (>%20) | 1 345 bar / 341 sembol | Çoğu GERÇEK (devre kesici, sermaye olayı). Yalnız %16'i hacimsiz barın ardından |

En büyük tek günlük sıçramalar:

| sembol | aşan bar | en büyük |
|---|---|---|
| `TRHOL` | 5 | **%10124** |
| `ISATR` | 16 | **%8781** |
| `KSTUR` | 23 | **%2525** |
| `KGYO` | 4 | **%952** |
| `CRFSA` | 3 | **%459** |
| `ISBTR` | 16 | **%447** |
| `ISGSY` | 9 | **%401** |
| `FRIGO` | 11 | **%386** |
| `POLHO` | 4 | **%319** |
| `UMPAS` | 6 | **%301** |

## 6 · Bayat bar testi — bu denetimin en önemli ölçümü

Hacimsiz bir barın fiyatı, **kimsenin işlem yapmadığı** bir fiyattır: sağlayıcı son fiyatı tekrar eder. İşlem yeniden başlayınca fiyat gerçek seviyesine sıçrar. O bardan girmek, kimsenin giremeyeceği bir fiyattan girmektir.

**40 bar ileri getiri — giriş barının hacmine göre:**

| giriş barı | n | ortalama | medyan |
|---|---|---|---|
| **hacimsiz** | 51 304 | **%13.46** | %0.00 |
| normal | 1 627 904 | %7.13 | %1.41 |
| **fark** | | **%+6.33** | |

Medyanın hacimsiz tarafta **%0.00** olması deseni ele veriyor: barların çoğu düz, ama bir kuyruk büyük sıçramalarla ortalamayı yukarı çekiyor. Bayat fiyatın imzası tam olarak budur.

### Ölçüme etkisi — doğrudan

`olcum/bariyer.py::_bos_havuzu` adil bazı RASTGELE barlardan kuruyor ve **hacimsiz barları dışlamıyor.** Yani bazın bir bölümü, kimsenin giremeyeceği fiyatlardan alınmış hayalet işlemlerden oluşuyor ve o işlemler ortalamada kazanıyor.

Dedektörler de aynı barlarda sinyal üretebiliyor: hacimsiz barın açılış/yüksek/düşük/kapanışı aynı sayıdır, yani bir seviyeye "dokunmuş" sayılabilir.

**İki taraf da kirli olduğu için net etkinin yönü ölçülmeden bilinemez.** Ama düzeltilmesi gerektiği açık.

## 7 · Ne yapılmalı

Bu bölüm **karar değil, seçenek** listesidir; karar ölçüm görülünce ayrıca verilir.

1. **Hayatta kalma yanlılığı** tam düzeltilemez (listeden düşen şirketlerin fiyat verisi sağlayıcıda yok). Ama büyüklüğü SINIRLANABİLİR: 2010–bugün arası BIST şirket listesiyle karşılaştırıp kaç sembolün eksik olduğu sayılabilir. Bilinen bir yanlılık, bilinmeyen bir yanlılıktan iyidir.
2. **2014 öncesi** açılış fiyatı güvenilmezse, gövde tabanlı her kural (KURAL-30 teyidi gibi) o dönemde ölçülemez. Ölçümlerin başlangıç tarihi buna göre seçilmeli.
3. **Hacimsiz ve donuk barlar** gözlem sayılmamalı; sinyal o barlarda üretilmemeli.
4. **Marjı aşan barlar** tek tek incelenmeli: gerçek bir olay mı (sermaye artırımı, birleşme) yoksa düzeltme hatası mı.
