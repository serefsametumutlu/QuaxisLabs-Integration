# Harmonik (Pesavento) — K4 İstatistik · 1D

**Tarih:** 2026-09-13 · **Evren:** 507 BIST sembolü · **Yön:** hepsi

Ölçüt: **üç bariyerli R** (stop / hedef / zaman). Stop ve hedef stratejinin kendi kuralından geliyor. İşlem maliyeti dahil (taraf başına %0.050 komisyon + %0.050 kayma). **Aynı barda stop ve hedef birlikte vurulduysa STOP sayılır.**

Bağımsız gözlem **sembol**, bar değil. Adil baz: aynı risk yapısıyla rastgele bar/sembol. Aile beş üyeli ve **önceden sabitlendi** — BH-FDR (q=0.05) beşine birden uygulandı.

## OOS — birincil

| formasyon | işlem | sembol | isabet | beklenen R | adil baz | fark | PF | p |
|---|---|---|---|---|---|---|---|---|
| `abcd_stop1272` | 1587 | 435 | %27.4 | **-0.025R** | -0.076R | +0.051R | 0.97 | 0.3578 |
| `abcd_stop1618` | 1587 | 435 | %42.5 | **-0.069R** | -0.104R | +0.035R | 0.87 | 0.3298 |
| `gartley` | 58 | 53 | %36.2 | **+0.071R** | +0.016R | +0.055R | 1.11 | 0.4033 |
| `kelebek` | 51 | 50 | %31.4 | **-0.139R** | -0.027R | -0.112R | 0.79 | 0.6827 |
| `uc_surus` | 71 | 65 | %35.2 | **+0.101R** | +0.023R | +0.078R | 1.15 | 0.2629 |

## IS — tutarlılık

| formasyon | işlem | sembol | isabet | beklenen R | adil baz | fark | PF | p |
|---|---|---|---|---|---|---|---|---|
| `abcd_stop1272` | 4043 | 482 | %28.3 | **+0.020R** | -0.034R | +0.054R | 1.03 | 0.7276 |
| `abcd_stop1618` | 4043 | 482 | %43.2 | **-0.051R** | -0.068R | +0.017R | 0.91 | 0.5102 |
| `gartley` | 176 | 127 | %34.1 | **+0.056R** | -0.015R | +0.071R | 1.08 | 0.4493 |
| `kelebek` | 226 | 167 | %29.6 | **-0.185R** | -0.017R | -0.168R | 0.74 | 0.9275 |
| `uc_surus` | 180 | 148 | %30.6 | **-0.067R** | -0.034R | -0.032R | 0.91 | 0.5882 |

## BH-FDR (q = 0.05) — OOS penceresi

| formasyon | p | FDR eşiğini geçti mi |
|---|---|---|
| `uc_surus` | 0.2629 | ✘ |
| `abcd_stop1618` | 0.3298 | ✘ |
| `abcd_stop1272` | 0.3578 | ✘ |
| `gartley` | 0.4033 | ✘ |
| `kelebek` | 0.6827 | ✘ |

## Çıkış kırılımı

| formasyon | hedef | stop | zaman | ort. kazanç | ort. kayıp |
|---|---|---|---|---|---|
| `abcd_stop1272` | %20 | %71 | %9 | +2.59R | -1.01R |
| `abcd_stop1618` | %29 | %50 | %22 | +1.09R | -0.93R |
| `gartley` | %31 | %64 | %5 | +2.02R | -1.03R |
| `kelebek` | %20 | %63 | %18 | +1.67R | -0.97R |
| `uc_surus` | %35 | %65 | %0 | +2.23R | -1.05R |

## Örneklem yeterli mi

Pardo s.295: 30–50 işlem asgari kabul edilir. **Sembol sayısı 30'un altındaki satırın sayısı yazılır, verdikti yazılmaz.**

| formasyon | OOS sembol | yeterli mi |
|---|---|---|
| `abcd_stop1272` | 435 | ✔ |
| `abcd_stop1618` | 435 | ✔ |
| `gartley` | 53 | ✔ |
| `kelebek` | 50 | ✔ |
| `uc_surus` | 65 | ✔ |

