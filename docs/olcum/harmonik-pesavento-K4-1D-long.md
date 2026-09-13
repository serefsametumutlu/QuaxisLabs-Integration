# Harmonik (Pesavento) — K4 İstatistik · 1D

**Tarih:** 2026-09-13 · **Evren:** 507 BIST sembolü · **Yön:** long

Ölçüt: **üç bariyerli R** (stop / hedef / zaman). Stop ve hedef stratejinin kendi kuralından geliyor. İşlem maliyeti dahil (taraf başına %0.050 komisyon + %0.050 kayma). **Aynı barda stop ve hedef birlikte vurulduysa STOP sayılır.**

Bağımsız gözlem **sembol**, bar değil. Adil baz: aynı risk yapısıyla rastgele bar/sembol. Aile beş üyeli ve **önceden sabitlendi** — BH-FDR (q=0.05) beşine birden uygulandı.

## OOS — birincil

| formasyon | işlem | sembol | isabet | beklenen R | adil baz | fark | PF | p |
|---|---|---|---|---|---|---|---|---|
| `abcd_stop1272` | 622 | 325 | %41.6 | **+0.459R** | +0.367R | +0.092R | 1.80 | 0.5612 |
| `abcd_stop1618` | 622 | 325 | %59.3 | **+0.317R** | +0.225R | +0.093R | 2.02 | 0.2619 |
| `gartley` | 29 | 27 | %41.4 | **+0.218R** | +0.318R | -0.100R | 1.36 | 0.5332 |
| `kelebek` | 21 | 21 | %33.3 | **-0.112R** | +0.348R | -0.461R | 0.81 | 0.9240 |
| `uc_surus` | 46 | 43 | %32.6 | **+0.016R** | +0.192R | -0.175R | 1.02 | 0.7051 |

## IS — tutarlılık

| formasyon | işlem | sembol | isabet | beklenen R | adil baz | fark | PF | p |
|---|---|---|---|---|---|---|---|---|
| `abcd_stop1272` | 1791 | 425 | %33.4 | **+0.183R** | +0.297R | -0.114R | 1.27 | 0.9900 |
| `abcd_stop1618` | 1791 | 425 | %51.6 | **+0.133R** | +0.161R | -0.028R | 1.31 | 0.8141 |
| `gartley` | 79 | 68 | %36.7 | **+0.117R** | +0.214R | -0.097R | 1.18 | 0.8006 |
| `kelebek` | 117 | 98 | %34.2 | **-0.071R** | +0.162R | -0.233R | 0.89 | 0.9745 |
| `uc_surus` | 96 | 85 | %32.3 | **-0.013R** | +0.124R | -0.137R | 0.98 | 0.7716 |

## BH-FDR (q = 0.05) — OOS penceresi

| formasyon | p | FDR eşiğini geçti mi |
|---|---|---|
| `abcd_stop1618` | 0.2619 | ✘ |
| `gartley` | 0.5332 | ✘ |
| `abcd_stop1272` | 0.5612 | ✘ |
| `uc_surus` | 0.7051 | ✘ |
| `kelebek` | 0.9240 | ✘ |

## Çıkış kırılımı

| formasyon | hedef | stop | zaman | ort. kazanç | ort. kayıp |
|---|---|---|---|---|---|
| `abcd_stop1272` | %29 | %54 | %17 | +2.47R | -0.98R |
| `abcd_stop1618` | %39 | %24 | %36 | +1.06R | -0.77R |
| `gartley` | %34 | %59 | %7 | +1.98R | -1.03R |
| `kelebek` | %19 | %52 | %29 | +1.42R | -0.88R |
| `uc_surus` | %33 | %67 | %0 | +2.22R | -1.05R |

## Örneklem yeterli mi

Pardo s.295: 30–50 işlem asgari kabul edilir. **Sembol sayısı 30'un altındaki satırın sayısı yazılır, verdikti yazılmaz.**

| formasyon | OOS sembol | yeterli mi |
|---|---|---|
| `abcd_stop1272` | 325 | ✔ |
| `abcd_stop1618` | 325 | ✔ |
| `gartley` | 27 | ✘ verdikt yazılmaz |
| `kelebek` | 21 | ✘ verdikt yazılmaz |
| `uc_surus` | 43 | ✔ |

