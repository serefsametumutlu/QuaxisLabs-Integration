# Harmonik (Pesavento) — K3 Kalibrasyon · 1D

**Tarih:** 2026-09-13 · **Evren:** 545 BIST sembolü · **1 437 257 bar** (5 703 sembol-yıl)

Karar kuralı sonuçlar görülmeden yazıldı ve commit edildi: [`harmonik-pesavento-K3-karar-kurali.md`](harmonik-pesavento-K3-karar-kurali.md).

> **Bu bir backtest DEĞİLDİR.** Hiçbir işlem simüle edilmedi, getiri hesaplanmadı. Ölçülen tek şey: formasyon gerçek veride kaç kez oluşuyor ve oranları nasıl dağılıyor. Getiri K4'ün işi.

## 1 · Tolerans taraması

Karar kuralı: sembol ≥ 100 **ve** sembol başına yıllık sinyal ≤ 3; kalanlardan **en küçüğü**.

### `abcd`

| tolerans | sinyal | sembol | sinyal/sembol/yıl | ≥100 sembol | ≤3/yıl |
|---|---|---|---|---|---|
| 0.02 | 9573 | 516 | 1.68 | ✔ | ✔ |
| 0.03 | 12858 | 522 | 2.25 | ✔ | ✔ |
| 0.05 | 19850 | 528 | 3.48 | ✔ | ✘ |
| 0.08 | 24162 | 529 | 4.24 | ✔ | ✘ |
| 0.10 | 25232 | 530 | 4.42 | ✔ | ✘ |

**Seçilen: `tolerans = 0.02`**

### `gartley`

| tolerans | sinyal | sembol | sinyal/sembol/yıl | ≥100 sembol | ≤3/yıl |
|---|---|---|---|---|---|
| 0.02 | 354 | 225 | 0.06 | ✔ | ✔ |
| 0.03 | 692 | 322 | 0.12 | ✔ | ✔ |
| 0.05 | 2081 | 430 | 0.36 | ✔ | ✔ |
| 0.08 | 3667 | 474 | 0.64 | ✔ | ✔ |
| 0.10 | 4077 | 477 | 0.71 | ✔ | ✔ |

**Seçilen: `tolerans = 0.02`**

### `kelebek`

| tolerans | sinyal | sembol | sinyal/sembol/yıl | ≥100 sembol | ≤3/yıl |
|---|---|---|---|---|---|
| 0.02 | 353 | 223 | 0.06 | ✔ | ✔ |
| 0.03 | 715 | 319 | 0.13 | ✔ | ✔ |
| 0.05 | 2198 | 426 | 0.39 | ✔ | ✔ |
| 0.08 | 4009 | 479 | 0.70 | ✔ | ✔ |
| 0.10 | 4650 | 485 | 0.82 | ✔ | ✔ |

**Seçilen: `tolerans = 0.02`**

### `uc_surus`

| tolerans | sinyal | sembol | sinyal/sembol/yıl | ≥100 sembol | ≤3/yıl |
|---|---|---|---|---|---|
| 0.02 | 17 | 16 | 0.00 | ✘ | ✔ |
| 0.03 | 95 | 85 | 0.02 | ✘ | ✔ |
| 0.05 | 350 | 243 | 0.06 | ✔ | ✔ |
| 0.08 | 1089 | 384 | 0.19 | ✔ | ✔ |
| 0.10 | 1501 | 421 | 0.26 | ✔ | ✔ |

**Seçilen: `tolerans = 0.05`**

## 2 · Pivot kolu taraması

Karar kuralı: aynı iki sınır; kalanlardan **ortanca**. (En küçük değil — dar pivot kolu gürültüyü salınım sanar.)

| formasyon | kol=2 | kol=3 | kol=4 | kol=5 | seçilen |
|---|---|---|---|---|---|
| `abcd` | 28878 / 535s ✘ | 19850 / 528s ✘ | 14882 / 525s ✔ | 11566 / 523s ✔ | **5** |
| `gartley` | 3096 / 460s ✔ | 2081 / 430s ✔ | 1519 / 420s ✔ | 1205 / 396s ✔ | **4** |
| `kelebek` | 3472 / 462s ✔ | 2198 / 426s ✔ | 1596 / 401s ✔ | 1160 / 361s ✔ | **4** |
| `uc_surus` | 521 / 283s ✔ | 350 / 243s ✔ | 259 / 194s ✔ | 193 / 160s ✔ | **4** |

Hücreler: `sinyal / sembol`.

## 3 · `donus_max_bar` — taranmadı, DAĞILIMDAN okundu

Pencere 400 bara açıldı ve C'nin onayından D'ye dokunuşa kadar geçen bar sayısı ölçüldü. Karar kuralı: **%90'lık dilim**, en yakın 5'e yuvarlanmış.

> **Bu ölçümün bilinen yanlılığı:** dedektör aynı yönde ikinci bir kurulum açmıyor. Pencere 400'e açılınca uzun bekleyen bir kurulum arkasındaki kısa bekleyenleri BLOKLUYOR, yani dağılım uzun beklemeler lehine hafifçe kayıyor. Yanlılığın yönü bilindiği için 40 barlık (kırpılmış) dağılım da yanına yazıldı: ikisi birbirine yakınsa yanlılık önemsizdir.

| formasyon | n | medyan | %75 | **%90** | %95 | azami | **seçilen** | 40-bar %90 |
|---|---|---|---|---|---|---|---|---|
| `abcd` | 20352 | 12 | 23 | **42** | 59 | 396 | **40** | 28 |
| `gartley` | 2200 | 10 | 17 | **30** | 45 | 247 | **30** | 24 |
| `kelebek` | 2498 | 14 | 28 | **53** | 75 | 302 | **55** | 31 |
| `uc_surus` | 356 | 8 | 12 | **20** | 25 | 138 | **20** | 18 |

## 4 · Oranlar gerçekte nereye düşüyor

Eşik SEÇMEZ (karar kuralı §6) — bulgu olarak yazılır.

### Gartley'in AB bacağı gerçekten dar bir bantta mı

K0 §3.1: kitabın iki kuralı (D = .786 XA **ve** içeride AB=CD) cebirsel olarak `AB = .786 / (2 − BC)` veriyor, yani **AB ≈ .49–.65**. Ölçüm bunu doğruluyor mu:

| formasyon · bacak | n | en düşük | %25 | medyan | %75 | en yüksek |
|---|---|---|---|---|---|---|
| `abcd` · bc | 19850 | 0.382 | 0.500 | 0.618 | 0.786 | 0.786 |
| `abcd` · cd | 19850 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `gartley` · ab | 2081 | 0.382 | 0.500 | 0.500 | 0.618 | 0.618 |
| `gartley` · abcd | 2081 | 1.000 | 1.000 | 1.000 | 1.272 | 2.000 |
| `gartley` · bc | 2081 | 0.382 | 0.618 | 0.618 | 0.786 | 0.786 |
| `gartley` · d | 2081 | 0.786 | 0.786 | 0.786 | 0.786 | 0.786 |
| `kelebek` · ab | 2198 | 0.500 | 0.618 | 0.786 | 0.786 | 0.786 |
| `kelebek` · abcd | 2198 | 1.000 | 1.272 | 1.272 | 1.618 | 2.000 |
| `kelebek` · bc | 2198 | 0.382 | 0.500 | 0.618 | 0.618 | 0.786 |
| `kelebek` · d | 2198 | 1.272 | 1.272 | 1.272 | 1.272 | 1.272 |
| `uc_surus` · a | 350 | 0.382 | 0.500 | 0.618 | 0.618 | 0.786 |
| `uc_surus` · c | 350 | 0.382 | 0.500 | 0.618 | 0.786 | 0.786 |
| `uc_surus` · s2_uzanti | 350 | 1.222 | 1.250 | 1.267 | 1.295 | 1.322 |
| `uc_surus` · s3_uzanti | 350 | 1.272 | 1.272 | 1.272 | 1.272 | 1.272 |

### Hangi Fibonacci oranı kaç kez tuttu

* `abcd` · **bc** — 0.382: %19 · 0.5: %25 · 0.618: %29 · 0.786: %28
* `abcd` · **cd** — 1.0: %100
* `gartley` · **ab** — 0.382: %18 · 0.5: %44 · 0.618: %38
* `gartley` · **abcd** — 1.0: %53 · 1.272: %30 · 1.618: %13 · 2.0: %4
* `gartley` · **bc** — 0.382: %7 · 0.5: %15 · 0.618: %32 · 0.786: %46
* `gartley` · **d** — 0.786: %100
* `kelebek` · **ab** — 0.5: %9 · 0.618: %33 · 0.786: %58
* `kelebek` · **abcd** — 1.0: %20 · 1.272: %39 · 1.618: %26 · 2.0: %15
* `kelebek` · **bc** — 0.382: %17 · 0.5: %22 · 0.618: %36 · 0.786: %24
* `kelebek` · **d** — 1.272: %100
* `uc_surus` · **a** — 0.382: %19 · 0.5: %29 · 0.618: %30 · 0.786: %22
* `uc_surus` · **c** — 0.382: %10 · 0.5: %25 · 0.618: %32 · 0.786: %33
* `uc_surus` · **s3_uzanti** — 1.272: %100

## 5 · Boğa / ayı asimetrisi

| formasyon | toplam | boğa | ayı | boğa oranı |
|---|---|---|---|---|
| `abcd` | 19850 | 8103 | 11747 | %41 |
| `gartley` | 2081 | 874 | 1207 | %42 |
| `kelebek` | 2198 | 1014 | 1184 | %46 |
| `uc_surus` | 350 | 197 | 153 | %56 |

## 6 · Uygulanacak eşikler

| formasyon | tolerans | pivot kolu | donus_max_bar |
|---|---|---|---|
| `abcd` | 0.02 | 5 | 40 |
| `gartley` | 0.02 | 4 | 30 |
| `kelebek` | 0.02 | 4 | 55 |
| `uc_surus` | 0.05 | 4 | 20 |

`stop_orani` (AB=CD) **kapatılmadı** — karar kuralı §5: hangi stop mesafesinin doğru olduğu bir getiri sorusudur ve getiriye bakarak eşik seçmek yasaklandı. K4'te iki ayrı künye olarak ölçülecek.


## 7 · Seçilen birleşimin doğrulaması

İki tarama **ayrı ayrı** koştu (tolerans taraması pivot=3 ile, pivot taraması tolerans=0.05 ile). Seçilen birleşimler böylece hiç ölçülmemiş oluyordu. Burada ölçülüyorlar; iki sınırı sağlamayan formasyon karar kuralı §7 gereği **K4'e girmez**.

| formasyon | tolerans | pivot | sinyal | sembol | /sembol/yıl | ≥100 | ≤3/yıl | **donus_max_bar** |
|---|---|---|---|---|---|---|---|---|
| `abcd` | 0.02 | 5 | 6009 | 506 | 1.05 | ✔ | ✔ | **55** |
| `gartley` | 0.02 | 4 | 262 | 185 | 0.05 | ✔ | ✔ | **35** |
| `kelebek` | 0.02 | 4 | 304 | 207 | 0.05 | ✔ | ✔ | **60** |
| `uc_surus` | 0.05 | 4 | 267 | 199 | 0.05 | ✔ | ✔ | **25** |

`donus_max_bar` burada YENİDEN okundu: tolerans ve pivot değişince dokunuş süresi dağılımı da kayar. Eski dağılımdan okunan sayıyı yeni ayarlara taşımak, ölçülmemiş bir eşiği ölçülmüş gibi göstermek olurdu.

