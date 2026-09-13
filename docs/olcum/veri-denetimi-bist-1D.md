# Veri denetimi — BIST · 1D

**Tarih:** 2026-09-14

> Bu araç veriyi **düzeltmez**, ölçer. Sessizce temizlenen veri, sessizce bozulmuş veriden daha tehlikelidir: birincisinde neyin atıldığını kimse bilmez.

## 1 · Evren kapsamı

| | |
|---|---|
| Evren dosyasındaki sembol | 648 |
| Verisi olan | **544** |
| Dosyası yok | 104 |
| Dosyası var ama boş | 0 |
| Toplam bar | 1 433 075 |
| Sembol başına bar (medyan) | 3349 |
| En kısa / en uzun | 19 / 4290 |

Dosyası olmayanlar (104): `KRPLS`, `BMSTL`, `ERCB`, `GEDIK`, `OSMEN`, `OYYAT`, `ISBTR`, `QNBTR`, `SKBNK`, `EDATA`, `INTEK`, `LOGO`, `MIATK`, `MTRKS`, `BIGTK`, `PCILT`, `SNKRN`, `BASGZ`, `BIOEN`, `LYDYE`, `MANAS`, `NTGAZ`, `QNBFK`, `QNBFL`, `ADESE`, `AKFGY`, `ATAGY`, `ISGYO`, `KUYAS`, `PEHOL`, `PSGYO`, `RYGYO`, `YGYO`, `HUBVC`, `MGROS`, `CCOLA`, `DARDL`, `DUNYH`, `EFORC`, `ELITE` …

**Bu sayı kendi başına bir bulgu.** Evren dosyası bu sembolleri listeliyor ama veri yok — yani her ölçüm, farkında olmadan daha küçük bir evrende koşuyor.

## 2 · Hayatta kalma yanlılığı

Son barın yılı — **listeden düşen sembol varsa burada görünür:**

`2026: 544`

**544 sembolün 544'inin son barı 2026'da.** Listeden düşmüş tek bir şirket yok.

Bu, evren dosyasının **bugünün listesinin anlık görüntüsü** olmasının doğrudan sonucu. 2010–bugün arasında iflas eden, birleşen ya da kottan çıkarılan her şirket veri setinde YOK.

### Bunun ölçüme etkisi

Yanlılık hem stratejiyi hem adil bazı besliyor — ikisi de aynı evrenden çekiliyor — bu yüzden **farkı** ne kadar bozduğu ölçülmeden bilinemez. Ama iki şey kesin:

1. **Mutlak sayılar iyimser.** Sıfıra giden şirketler eksik olduğu için, stop'la çalışan bir stratejinin gerçek hayattaki en kötü senaryoları veri setinde hiç yok.
2. **Adil baz da iyimser.** Rastgele giriş, "16 yıl ayakta kalmış" filtresinden geçmiş bir evrende yapılıyor.

İlk barın yılı (halka arz dağılımının vekili):

`2010: 223 · 2011: 17 · 2012: 22 · 2013: 19 · 2014: 13 · 2015: 8 · 2016: 2 · 2017: 3 · 2018: 10 · 2019: 5 · 2020: 9 · 2021: 37 · 2022: 32 · 2023: 32 · 2024: 61 · 2025: 19 · 2026: 32`

## 3 · OHLC bütünlüğü

İhlal yok — `high ≥ max(açılış, kapanış)`, `low ≤ min(…)`, `high ≥ low`, `kapanış > 0` hepsinde sağlanıyor.

## 4 · Açılış fiyatı gerçek mi

`açılış == kapanış` olan bar, gövdesiz mumdur. Gerçek piyasada nadirdir; **sistematik olarak yüksekse sağlayıcı açılışı uyduruyordur.**

| Yıl | Bar | `açılış == kapanış` | Oran |
|---|---|---|---|
| 2010 | 55767 | 45502 | **%81.6** |
| 2011 | 60081 | 57198 | **%95.2** |
| 2012 | 65231 | 62916 | **%96.5** |
| 2013 | 70371 | 54597 | **%77.6** |
| 2014 | 74625 | 36705 | **%49.2** |
| 2015 | 78002 | 34202 | **%43.8** |
| 2016 | 79003 | 16171 | **%20.5** |
| 2017 | 79384 | 12963 | **%16.3** |
| 2018 | 82061 | 12555 | **%15.3** |
| 2019 | 82794 | 13805 | **%16.7** |
| 2020 | 82311 | 6096 | **%7.4** |
| 2021 | 86215 | 5509 | **%6.4** |
| 2022 | 96807 | 5692 | **%5.9** |
| 2023 | 103797 | 3934 | **%3.8** |
| 2024 | 117343 | 3802 | **%3.2** |
| 2025 | 126721 | 4400 | **%3.5** |
| 2026 | 92562 | 5117 | **%5.5** |

## 5 · Diğer kusurlar

| Kusur | Sayı | Ne demek |
|---|---|---|
| Hacimsiz bar | 40 889 | O gün işlem görmemiş; fiyat gerçek bir gözlem değil |
| Donuk bar (≥5 bar aynı kapanış) | 17 470 | Sağlayıcı son fiyatı tekrar ediyor olabilir |
| Marjı aşan günlük getiri (>%20) | 1 021 bar / 289 sembol | Çoğu GERÇEK (devre kesici, sermaye olayı). Yalnız %17'i hacimsiz barın ardından |

En büyük tek günlük sıçramalar:

| sembol | aşan bar | en büyük |
|---|---|---|
| `ISATR` | 16 | **%8781** |
| `KSTUR` | 23 | **%2525** |
| `KGYO` | 4 | **%952** |
| `CRFSA` | 3 | **%459** |
| `ISGSY` | 9 | **%401** |
| `POLHO` | 4 | **%319** |
| `UMPAS` | 6 | **%301** |
| `LYDHO` | 6 | **%271** |
| `EMNIS` | 10 | **%215** |
| `YYAPI` | 14 | **%184** |

## 6 · Bayat bar testi — bu denetimin en önemli ölçümü

Hacimsiz bir barın fiyatı, **kimsenin işlem yapmadığı** bir fiyattır: sağlayıcı son fiyatı tekrar eder. İşlem yeniden başlayınca fiyat gerçek seviyesine sıçrar. O bardan girmek, kimsenin giremeyeceği bir fiyattan girmektir.

**40 bar ileri getiri — giriş barının hacmine göre:**

| giriş barı | n | ortalama | medyan |
|---|---|---|---|
| **hacimsiz** | 40 779 | **%15.31** | %0.00 |
| normal | 1 370 593 | %6.93 | %1.42 |
| **fark** | | **%+8.37** | |

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
